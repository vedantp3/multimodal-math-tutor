"""Knowledge base document loader with chunking."""
import os
from pathlib import Path


def load_knowledge_base(kb_dir: str = "knowledge_base") -> list[dict]:
    """Load all markdown files from the knowledge base directory.
    
    Returns a list of dicts with 'content' and 'metadata' keys.
    Each dict represents a chunk of text ready for embedding.
    """
    documents = []
    kb_path = Path(kb_dir)
    
    if not kb_path.exists():
        print(f"Warning: Knowledge base directory '{kb_dir}' not found.")
        return documents
    
    for filepath in sorted(kb_path.glob("*.md")):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        source_name = filepath.stem.replace("_", " ").title()
        
        # Chunk the document by sections (split on ## headers)
        chunks = _chunk_by_sections(content, source_name, str(filepath.name))
        documents.extend(chunks)
    
    print(f"Loaded {len(documents)} chunks from {len(list(kb_path.glob('*.md')))} documents.")
    return documents


def _chunk_by_sections(content: str, source_name: str, filename: str) -> list[dict]:
    """Split document content into chunks by section headers.
    
    Uses ## headers as split points, keeping each section as a chunk.
    If a section is too large, it's further split by paragraphs.
    """
    chunks = []
    max_chunk_size = 500
    
    # Split by ## headers
    sections = []
    current_section = ""
    
    for line in content.split("\n"):
        if line.startswith("## ") and current_section.strip():
            sections.append(current_section.strip())
            current_section = line + "\n"
        else:
            current_section += line + "\n"
    
    if current_section.strip():
        sections.append(current_section.strip())
    
    # Process each section
    for section in sections:
        if len(section) <= max_chunk_size:
            chunks.append({
                "content": section,
                "metadata": {
                    "source": filename,
                    "source_name": source_name
                }
            })
        else:
            # Split large sections into smaller paragraphs
            paragraphs = section.split("\n\n")
            current_chunk = ""
            
            for para in paragraphs:
                if len(current_chunk) + len(para) + 2 > max_chunk_size and current_chunk:
                    chunks.append({
                        "content": current_chunk.strip(),
                        "metadata": {
                            "source": filename,
                            "source_name": source_name
                        }
                    })
                    current_chunk = para + "\n\n"
                else:
                    current_chunk += para + "\n\n"
            
            if current_chunk.strip():
                chunks.append({
                    "content": current_chunk.strip(),
                    "metadata": {
                        "source": filename,
                        "source_name": source_name
                    }
                })
    
    return chunks
