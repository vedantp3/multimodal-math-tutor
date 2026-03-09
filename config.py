"""Configuration module for Math Mentor application."""
import os
from dotenv import load_dotenv

load_dotenv(override=True)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Model settings
GEMINI_MODEL = "gemini-2.0-flash"
EMBEDDING_MODEL = "models/gemini-embedding-001"

# RAG settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K_RETRIEVAL = 5
FAISS_INDEX_PATH = "faiss_index"

# Memory settings
MEMORY_FILE = "memory/memory_data.json"
SIMILARITY_THRESHOLD = 0.7

# Confidence thresholds
OCR_CONFIDENCE_THRESHOLD = 7
ASR_CONFIDENCE_THRESHOLD = 7
VERIFIER_CONFIDENCE_THRESHOLD = 70

# Knowledge base
KNOWLEDGE_BASE_DIR = "knowledge_base"
