import os
import shutil
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from app.config import CHROMA_PERSIST_DIR, CHROMA_COLLECTION_NAME
from app.rag.embeddings import get_embeddings_service

try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma

class VectorStoreManager:
    """Manages persistent ChromaDB vector storage with stable chunk IDs and category metadata filtering."""
    
    def __init__(self, collection_name: Optional[str] = None):
        os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
        self.embeddings = get_embeddings_service()
        self.collection_name = collection_name or CHROMA_COLLECTION_NAME
        
        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=CHROMA_PERSIST_DIR
        )

        from app.config import DEMO_MODE, DEMO_COLLECTION_NAME
        if DEMO_MODE and self.collection_name == DEMO_COLLECTION_NAME:
            self._ensure_demo_indexed()

    def _ensure_demo_indexed(self):
        try:
            data = self.vectorstore.get(include=[])
            count = len(data.get("ids", []))
            if count == 0:
                from app.rag.loader import MultiCategoryDocumentLoader
                loader = MultiCategoryDocumentLoader()
                demo_docs = loader.load_demo_documents()
                if demo_docs:
                    indexed_count = self.add_documents(demo_docs)
                    doc_names = set(d.metadata.get("document") for d in demo_docs)
                    print("\nDEMO INDEXING")
                    print("----------------")
                    print(f"Documents: {len(doc_names)}")
                    print(f"Chunks: {indexed_count}")
                    print(f"Collection: {self.collection_name}")
                    print("Status: Indexed\n")
        except Exception as e:
            print(f"Notice auto-seeding demo documents: {e}")

    def add_documents(self, documents: List[Document]) -> int:
        """Add or update text chunk documents using stable IDs to prevent duplication."""
        if not documents:
            return 0
            
        ids = []
        for idx, doc in enumerate(documents):
            meta = doc.metadata or {}
            doc_name = meta.get("document", "doc").replace(" ", "_")
            cat = meta.get("category", "gen")
            page = meta.get("page", 1)
            stable_id = f"{doc_name}_{cat}_p{page}_c{idx}"
            ids.append(stable_id)
            
        try:
            self.vectorstore.add_documents(documents=documents, ids=ids)
        except Exception as e:
            err_str = str(e).lower()
            if "dimension" in err_str or "invalidargumenterror" in err_str or "expecting embedding" in err_str:
                print("Embedding dimension change detected. Resetting ChromaDB collection...")
                self.clear_all()
                self.vectorstore.add_documents(documents=documents, ids=ids)
            else:
                raise e
        return len(documents)

    def add_chunks(self, chunks: List[Document]) -> int:
        """Alias for add_documents."""
        return self.add_documents(chunks)

    def similarity_search(self, query: str, category: Optional[str] = None, k: int = 4) -> List[Document]:
        """Similarity search with optional category metadata filter."""
        filter_clause = None
        if category and category.lower() != "all":
            filter_clause = {"category": category.lower()}
            
        try:
            if filter_clause:
                results = self.vectorstore.similarity_search(query, k=k, filter=filter_clause)
                if results:
                    return results
            return self.vectorstore.similarity_search(query, k=k)
        except Exception as e:
            err_str = str(e).lower()
            if "dimension" in err_str or "invalidargumenterror" in err_str or "expecting embedding" in err_str:
                print("Embedding dimension mismatch in ChromaDB. Resetting collection...")
                self.clear_all()
                return []
            print(f"Similarity search error ({e}). Returning fallback search results.")
            try:
                return self.vectorstore.similarity_search(query, k=k)
            except Exception:
                return []

    def get_indexed_documents(self) -> List[Dict[str, Any]]:
        """Return list of unique indexed documents with chunk count and category metadata."""
        try:
            data = self.vectorstore.get(include=["metadatas"])
            metadatas = data.get("metadatas", [])
            doc_map = {}
            for meta in metadatas:
                if not meta:
                    continue
                name = meta.get("document", "Unknown")
                cat = meta.get("category", "General")
                if name not in doc_map:
                    doc_map[name] = {
                        "name": name,
                        "category": cat,
                        "status": "indexed",
                        "chunks": 0
                    }
                doc_map[name]["chunks"] += 1
            return list(doc_map.values())
        except Exception as e:
            print(f"Error fetching indexed documents: {e}")
            return []

    def delete_document(self, document_name: str) -> bool:
        """Delete all vector chunks belonging to a document from ChromaDB."""
        try:
            self.vectorstore.delete(where={"document": document_name})
            return True
        except Exception as e:
            print(f"Error deleting document '{document_name}' from ChromaDB: {e}")
            return False

    def clear_all(self) -> bool:
        """Clears only the active collection without affecting other collections or persist directory."""
        try:
            try:
                self.vectorstore.delete_collection()
            except Exception as e:
                print(f"Notice deleting collection '{self.collection_name}': {e}")

            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=CHROMA_PERSIST_DIR
            )
            return True
        except Exception as e:
            print(f"Notice clearing vector store: {e}")
            return False
