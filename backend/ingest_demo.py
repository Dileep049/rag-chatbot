import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True, encoding='utf-8')

from app.config import DEMO_COLLECTION_NAME
from app.rag.loader import MultiCategoryDocumentLoader
from app.rag.vectorstore import VectorStoreManager

def main():
    print("==========================================")
    print(" Starting Demo RAG Knowledge Base Ingestion ")
    print(f" Target Collection: {DEMO_COLLECTION_NAME}")
    print("==========================================")

    loader = MultiCategoryDocumentLoader()
    demo_vectorstore = VectorStoreManager(collection_name=DEMO_COLLECTION_NAME)
    
    print("Resetting Demo ChromaDB collection...")
    demo_vectorstore.clear_all()
    print("Demo collection reset successfully.\n")

    demo_docs = loader.load_demo_documents()
    print(f"Loaded {len(demo_docs)} demo section document(s).")
    
    if demo_docs:
        indexed_count = demo_vectorstore.add_documents(demo_docs)
        doc_names = set(d.metadata.get("document") for d in demo_docs if d.metadata)
        
        # Verify from ChromaDB directly
        actual_data = demo_vectorstore.vectorstore.get(include=[])
        actual_chunks = len(actual_data.get("ids", []))
        
        print("\nDEMO INDEXING COMPLETE")
        print(f"Collection: {DEMO_COLLECTION_NAME}")
        print(f"Documents: {len(doc_names)}")
        print(f"Chunks: {actual_chunks}")
        
        for doc in demo_docs:
            meta = doc.metadata or {}
            print(f"  - [{meta.get('document')}] Section: {meta.get('section')} | Category: {meta.get('category')} | Page: {meta.get('page')}")

    print("------------------------------------------")
    print("Demo Indexing completed successfully.")
    print("==========================================")

if __name__ == "__main__":
    main()
