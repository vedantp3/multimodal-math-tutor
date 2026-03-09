"""FAISS-based retriever with Google Generative AI embeddings."""
import os
import json
import numpy as np
import faiss
import google.generativeai as genai
from pathlib import Path

from config import GOOGLE_API_KEY, EMBEDDING_MODEL, FAISS_INDEX_PATH, TOP_K_RETRIEVAL
from rag.knowledge_loader import load_knowledge_base


class RAGRetriever:
    """Retriever that embeds documents and performs similarity search with FAISS."""
    
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.embedding_model = EMBEDDING_MODEL
        self.index = None
        self.documents = []
        self.index_path = FAISS_INDEX_PATH
        self._initialize()
    
    def _initialize(self):
        """Load or build the FAISS index."""
        docs_path = os.path.join(self.index_path, "documents.json")
        index_file = os.path.join(self.index_path, "index.faiss")
        
        if os.path.exists(index_file) and os.path.exists(docs_path):
            # Load existing index
            self.index = faiss.read_index(index_file)
            with open(docs_path, "r", encoding="utf-8") as f:
                self.documents = json.load(f)
            print(f"Loaded existing FAISS index with {len(self.documents)} documents.")
        else:
            # DO NOT build here synchronously, it causes a 60-second timeout on Streamlit Cloud
            print("No FAISS index found. It will be built lazily on first retrieval.")
            self.index = None
    
    def _build_index(self):
        """Build FAISS index from knowledge base documents."""
        self.documents = load_knowledge_base()
        
        if not self.documents:
            print("Warning: No documents to index.")
            return
        
        # Get embeddings for all document chunks
        texts = [doc["content"] for doc in self.documents]
        embeddings = self._get_embeddings(texts)
        
        if embeddings is None or len(embeddings) == 0:
            print("Warning: Failed to generate embeddings.")
            return
        
        # Build FAISS index
        dimension = len(embeddings[0])
        self.index = faiss.IndexFlatL2(dimension)
        embeddings_array = np.array(embeddings, dtype="float32")
        self.index.add(embeddings_array)
        
        # Save index and documents
        os.makedirs(self.index_path, exist_ok=True)
        faiss.write_index(self.index, os.path.join(self.index_path, "index.faiss"))
        with open(os.path.join(self.index_path, "documents.json"), "w", encoding="utf-8") as f:
            json.dump(self.documents, f, indent=2)
        
        print(f"Built FAISS index with {len(self.documents)} chunks (dim={dimension}).")
    
    def _get_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Get embeddings for a list of texts using Gemini embedding model."""
        all_embeddings = []
        dim = None  # Discovered from the first successful batch
        failed_ranges = []  # Track which ranges failed so we can back-fill
        batch_size = 20

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            try:
                result = genai.embed_content(
                    model=self.embedding_model,
                    content=batch,
                    task_type="retrieval_document"
                )
                vecs = result["embedding"]
                if dim is None and vecs:
                    dim = len(vecs[0])
                all_embeddings.extend(vecs)
            except Exception as e:
                print(f"Embedding error for batch {i}: {e}")
                # Mark these positions for back-fill
                failed_ranges.append((len(all_embeddings), len(batch)))
                all_embeddings.extend([None] * len(batch))

        # Back-fill any failed embeddings with zero vectors
        if dim is None:
            print("Warning: All embeddings failed. Cannot build index.")
            return []

        for start, count in failed_ranges:
            for j in range(start, start + count):
                all_embeddings[j] = [0.0] * dim

        return all_embeddings
    
    def _get_query_embedding(self, query: str) -> list[float]:
        """Get embedding for a single query."""
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=query,
                task_type="retrieval_query"
            )
            return result["embedding"]
        except Exception as e:
            print(f"Query embedding error: {e}")
            return None
    
    def retrieve(self, query: str, k: int = None) -> list[dict]:
        """Retrieve top-k relevant documents for a query.
        
        Returns list of dicts with 'content', 'metadata', and 'score' keys.
        Returns empty list with informative message if retrieval fails.
        """
        if k is None:
            k = TOP_K_RETRIEVAL
            
        if self.index is None or len(self.documents) == 0:
            print("FAISS index not loaded. Attempting to build or load now...")
            self._build_index()
            
            # If it's still None after trying to build, then knowledge base is empty
            if self.index is None:
                return [{
                    "content": "No relevant context found. Knowledge base is empty or could not be generated.",
                    "metadata": {"source": "system"},
                    "score": 0.0
                }]
        
        query_embedding = self._get_query_embedding(query)
        if query_embedding is None:
            return [{
                "content": "No relevant context found. Embedding generation failed.",
                "metadata": {"source": "system"},
                "score": 0.0
            }]
        
        # Search FAISS index
        query_array = np.array([query_embedding], dtype="float32")
        k = min(k, len(self.documents))
        distances, indices = self.index.search(query_array, k)
        
        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.documents):
                doc = self.documents[idx]
                results.append({
                    "content": doc["content"],
                    "metadata": doc["metadata"],
                    "score": float(1 / (1 + dist))  # Convert distance to similarity score
                })
        
        if not results:
            return [{
                "content": "No relevant context found for this query.",
                "metadata": {"source": "system"},
                "score": 0.0
            }]
        
        return results
    
    def rebuild_index(self):
        """Force rebuild the FAISS index from knowledge base."""
        # Clear existing index files
        index_file = os.path.join(self.index_path, "index.faiss")
        docs_path = os.path.join(self.index_path, "documents.json")
        if os.path.exists(index_file):
            os.remove(index_file)
        if os.path.exists(docs_path):
            os.remove(docs_path)
        self._build_index()
