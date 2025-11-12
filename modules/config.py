from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# ========== REQUIRED FOR GEMINI! ==========
# Gemini API Key -- hardcoded or from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyAc6u9MpLih9DS6lig15CQhlcMR16G-qB8"
# ==========================================

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Directory for uploaded files
UPLOAD_DIR = BASE_DIR / "data" / "uploads"

# Directory to store FAISS vector index
FAISS_DIR = BASE_DIR / "data" / "faiss_index"

# FAISS index filename prefix
INDEX_NAME = "index"

# Optional: keep OpenAI key for other modules if needed
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
