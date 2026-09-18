import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "local").lower()
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", str(BASE_DIR / "chroma_db"))
DATA_DIR = os.getenv("DATA_DIR", str(BASE_DIR / "data"))

raw_demo = str(os.getenv("DEMO_MODE", "true")).strip().lower()
DEMO_MODE = raw_demo in ("true", "1", "yes", "on")
DEMO_COLLECTION_NAME = "citizen_assistance_demo"
PROD_COLLECTION_NAME = "citizen_assistance_knowledge_base"
CHROMA_COLLECTION_NAME = DEMO_COLLECTION_NAME if DEMO_MODE else PROD_COLLECTION_NAME

if os.getenv("RAG_DEBUG", "true").lower() == "true":
    print(f"[CONFIG DEBUG] DEMO_MODE = {DEMO_MODE} (raw='{os.getenv('DEMO_MODE')}') | Active Collection: {CHROMA_COLLECTION_NAME}")

# Auth & Admin Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "citizen_assistance_rag_secret_key_2026_safe")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "1440")) # 24 Hours

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "chintaladileep968@gmail.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "9381887173@0000")

# CORS & Security Settings
CORS_ORIGINS_RAW = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173")
CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS_RAW.split(",") if origin.strip()]

RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
CHAT_RATE_LIMIT = int(os.getenv("CHAT_RATE_LIMIT", "60"))       # max requests / min
UPLOAD_RATE_LIMIT = int(os.getenv("UPLOAD_RATE_LIMIT", "15"))    # max uploads / min
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "30")) # 30MB file size cap

CATEGORIES = [
    "aadhaar",
    "pension",
    "police",
    "vehicle",
    "pan",
    "driving_license",
    "schemes"
]

CATEGORY_LABELS = {
    "aadhaar": "Aadhaar",
    "pension": "Pension",
    "police": "Police",
    "vehicle": "Vehicle",
    "pan": "PAN",
    "driving_license": "Driving Licence",
    "schemes": "Government Schemes"
}

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt"}

# Production RAG Parameters
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "15"))          # Candidate pool size
RAG_FINAL_K = int(os.getenv("RAG_FINAL_K", "3"))        # Final context size (1-3 sources)
RAG_RELEVANCE_THRESHOLD = float(os.getenv("RAG_RELEVANCE_THRESHOLD", "0.20"))
RAG_DEBUG = os.getenv("RAG_DEBUG", "true").lower() == "true"
TOP_K_RESULTS = RAG_FINAL_K
