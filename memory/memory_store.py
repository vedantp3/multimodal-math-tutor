"""Memory store — JSON-based persistent storage with similarity search."""
import os
import json
import time
import numpy as np
import google.generativeai as genai
from config import GOOGLE_API_KEY, EMBEDDING_MODEL, MEMORY_FILE, SIMILARITY_THRESHOLD


class MemoryStore:
    """Stores and retrieves past problem-solving interactions for self-learning."""
    
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.embedding_model = EMBEDDING_MODEL
        self.memory_file = MEMORY_FILE
        self.entries = []
        self._load()
    
    def _load(self):
        """Load memory entries from disk."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    self.entries = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.entries = []
        else:
            self.entries = []
    
    def _save(self):
        """Save memory entries to disk."""
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.entries, f, indent=2, default=str)
    
    def store(self, entry: dict):
        """Store a complete interaction in memory.
        
        Expected entry keys:
            input_type, original_input, parsed_question, retrieved_context,
            route_info, solution, verification, explanation, feedback
        """
        memory_entry = {
            "id": len(self.entries) + 1,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "input_type": entry.get("input_type", "text"),
            "original_input": entry.get("original_input", ""),
            "parsed_question": entry.get("parsed_question", {}),
            "retrieved_context": entry.get("retrieved_context", ""),
            "route_info": entry.get("route_info", {}),
            "solution": entry.get("solution", ""),
            "verification": entry.get("verification", {}),
            "explanation": entry.get("explanation", ""),
            "feedback": entry.get("feedback", None),
            "embedding": None  # Will be set below
        }
        
        # Generate embedding for the problem text
        problem_text = entry.get("original_input", "")
        if entry.get("parsed_question", {}).get("problem_text"):
            problem_text = entry["parsed_question"]["problem_text"]
        
        embedding = self._get_embedding(problem_text)
        if embedding:
            memory_entry["embedding"] = embedding
        
        self.entries.append(memory_entry)
        self._save()
        return memory_entry["id"]
    
    def find_similar(self, problem_text: str, threshold: float = None) -> list[dict]:
        """Find similar previously-solved problems.
        
        Args:
            problem_text: The current problem text.
            threshold: Similarity threshold (0-1). Defaults to config value.
        
        Returns:
            List of similar entries with similarity scores, sorted by similarity.
        """
        if threshold is None:
            threshold = SIMILARITY_THRESHOLD
        
        if not self.entries:
            return []
        
        query_embedding = self._get_embedding(problem_text)
        if not query_embedding:
            return []
        
        similar = []
        for entry in self.entries:
            if entry.get("embedding"):
                similarity = self._cosine_similarity(query_embedding, entry["embedding"])
                if similarity >= threshold:
                    # Create a clean copy without the embedding
                    clean_entry = {k: v for k, v in entry.items() if k != "embedding"}
                    clean_entry["similarity_score"] = round(similarity, 3)
                    similar.append(clean_entry)
        
        # Sort by similarity (highest first)
        similar.sort(key=lambda x: x["similarity_score"], reverse=True)
        return similar[:3]  # Return top 3
    
    def update_feedback(self, entry_id: int, feedback: str, comment: str = ""):
        """Update feedback for a stored entry.
        
        Args:
            entry_id: ID of the memory entry.
            feedback: 'correct' or 'incorrect'.
            comment: Optional user comment.
        """
        for entry in self.entries:
            if entry["id"] == entry_id:
                entry["feedback"] = {
                    "status": feedback,
                    "comment": comment,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                break
        self._save()
    
    def get_correction_patterns(self) -> list[dict]:
        """Get patterns from corrected entries for learning.
        
        Returns entries where user provided corrections (incorrect + comment).
        """
        patterns = []
        for entry in self.entries:
            fb = entry.get("feedback")
            if fb and isinstance(fb, dict) and fb.get("status") == "incorrect" and fb.get("comment"):
                patterns.append({
                    "original_input": entry.get("original_input", ""),
                    "parsed_question": entry.get("parsed_question", {}),
                    "correction_comment": fb["comment"]
                })
        return patterns
    
    def get_memory_context(self, problem_text: str) -> str:
        """Get formatted context from similar problems for the solver.
        
        Returns a string ready to be injected into the solver prompt.
        """
        similar = self.find_similar(problem_text)
        if not similar:
            return ""
        
        context_parts = []
        for i, entry in enumerate(similar, 1):
            feedback_str = ""
            if entry.get("feedback"):
                fb = entry["feedback"]
                if isinstance(fb, dict):
                    feedback_str = f"Feedback: {fb.get('status', 'none')}"
                    if fb.get("comment"):
                        feedback_str += f" — {fb['comment']}"
                else:
                    feedback_str = f"Feedback: {fb}"
            
            context_parts.append(
                f"### Similar Problem {i} (similarity: {entry['similarity_score']:.1%})\n"
                f"**Problem**: {entry.get('parsed_question', {}).get('problem_text', entry.get('original_input', 'N/A'))}\n"
                f"**Topic**: {entry.get('parsed_question', {}).get('topic', 'unknown')}\n"
                f"**Solution snippet**: {str(entry.get('solution', ''))[:300]}...\n"
                f"{feedback_str}\n"
            )
        
        return "\n".join(context_parts)
    
    def get_stats(self) -> dict:
        """Get memory statistics."""
        total = len(self.entries)
        correct = sum(1 for e in self.entries 
                      if isinstance(e.get("feedback"), dict) and e["feedback"].get("status") == "correct")
        incorrect = sum(1 for e in self.entries 
                        if isinstance(e.get("feedback"), dict) and e["feedback"].get("status") == "incorrect")
        
        topics = {}
        for e in self.entries:
            topic = e.get("parsed_question", {}).get("topic", "unknown")
            topics[topic] = topics.get(topic, 0) + 1
        
        return {
            "total_problems": total,
            "correct": correct,
            "incorrect": incorrect,
            "no_feedback": total - correct - incorrect,
            "topics": topics
        }
    
    def _get_embedding(self, text: str) -> list[float] | None:
        """Get embedding for a text string."""
        if not text:
            return None
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_document"
            )
            return result["embedding"]
        except Exception as e:
            print(f"Memory embedding error: {e}")
            return None
    
    @staticmethod
    def _cosine_similarity(a: list[float], b: list[float]) -> float:
        """Compute cosine similarity between two vectors."""
        a = np.array(a)
        b = np.array(b)
        dot = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(dot / (norm_a * norm_b))
