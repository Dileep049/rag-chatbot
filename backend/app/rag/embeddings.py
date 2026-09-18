import re
import hashlib
import numpy as np
from typing import List
from langchain_core.embeddings import Embeddings
from app.config import EMBEDDING_PROVIDER, EMBEDDING_MODEL, OPENAI_API_KEY

class LocalSentenceTransformerEmbeddings(Embeddings):
    """Local Sentence Transformers embeddings wrapper for multilingual support (English, Telugu, Telugu-English)."""
    
    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        self.model_name = model_name
        self.model = None
        self.hf_embeddings = None
        self.fallback = LocalFallbackEmbeddings()
        self.use_fallback = False
        
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
        except Exception as e:
            print(f"Notice: Using local fallback embeddings generator ({e}).")
            self.use_fallback = True

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if self.use_fallback:
            return self.fallback.embed_documents(texts)
        try:
            if self.hf_embeddings is not None:
                return self.hf_embeddings.embed_documents(texts)
            if self.model is not None:
                embeddings = self.model.encode(texts, show_progress_bar=False)
                return embeddings.tolist()
            return self.fallback.embed_documents(texts)
        except Exception as e:
            print(f"Notice: Local embedding call failed ({e}). Switching to local fallback embeddings.")
            self.use_fallback = True
            return self.fallback.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        if self.use_fallback:
            return self.fallback.embed_query(text)
        try:
            if self.hf_embeddings is not None:
                return self.hf_embeddings.embed_query(text)
            if self.model is not None:
                embedding = self.model.encode(text, show_progress_bar=False)
                return embedding.tolist()
            return self.fallback.embed_query(text)
        except Exception as e:
            print(f"Notice: Local embedding query failed ({e}). Switching to local fallback embeddings.")
            self.use_fallback = True
            return self.fallback.embed_query(text)

class SafeOpenAIEmbeddings(Embeddings):
    """Embeddings wrapper trying OpenAIEmbeddings and catching 401 / Auth / Quota errors with fallback."""
    
    def __init__(self, openai_key: str):
        try:
            from langchain_openai import OpenAIEmbeddings
            self.primary_embeddings = OpenAIEmbeddings(
                openai_api_key=openai_key,
                model="text-embedding-3-small"
            )
        except Exception:
            self.primary_embeddings = None
        self.fallback = LocalFallbackEmbeddings()
        self.use_fallback = False if self.primary_embeddings else True

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if self.use_fallback or not self.primary_embeddings:
            return self.fallback.embed_documents(texts)
            
        try:
            return self.primary_embeddings.embed_documents(texts)
        except Exception as e:
            print(f"Notice: OpenAI Embeddings call failed ({e}). Switching to local fallback embeddings.")
            self.use_fallback = True
            return self.fallback.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        if self.use_fallback or not self.primary_embeddings:
            return self.fallback.embed_query(text)
            
        try:
            return self.primary_embeddings.embed_query(text)
        except Exception as e:
            print(f"Notice: OpenAI Embeddings call failed ({e}). Switching to local fallback embeddings.")
            self.use_fallback = True
            return self.fallback.embed_query(text)

class LocalFallbackEmbeddings(Embeddings):
    """Deterministic vector embeddings generator fallback when local model or API key is unconfigured."""
    
    def __init__(self, dim: int = 384):
        self.dim = dim

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._embed_text(t) for t in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._embed_text(text)

    def _embed_text(self, text: str) -> List[float]:
        words = re.findall(r'\w+', text.lower())
        vec = np.zeros(self.dim, dtype=np.float32)
        if not words:
            return vec.tolist()
            
        for w in words:
            h_int = int(hashlib.md5(w.encode('utf-8')).hexdigest(), 16)
            h = h_int % self.dim
            vec[h] += 1.0
            h2 = (h_int * 31) % self.dim
            vec[h2] += 0.5

        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()

def get_embeddings_service() -> Embeddings:
    """Returns local embedding model by default, or SafeOpenAIEmbeddings if explicitly requested."""
    if EMBEDDING_PROVIDER == "openai" and OPENAI_API_KEY and not OPENAI_API_KEY.startswith("your_"):
        try:
            return SafeOpenAIEmbeddings(OPENAI_API_KEY)
        except Exception as e:
            print(f"Notice: Could not initialize SafeOpenAIEmbeddings ({e}). Switching to local embeddings.")

    try:
        return LocalSentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    except Exception as e:
        print(f"Notice: Could not initialize LocalSentenceTransformerEmbeddings ({e}). Utilizing fallback embedding generator.")
        return LocalFallbackEmbeddings()
