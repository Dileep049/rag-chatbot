import sys
import os
from pathlib import Path

# Ensure app package is importable
sys.path.append(str(Path(__file__).resolve().parent))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True, encoding='utf-8')

from app.config import CATEGORIES, CATEGORY_LABELS
from app.rag.loader import MultiCategoryDocumentLoader
from app.rag.splitter import TextSplitterManager
from app.rag.vectorstore import VectorStoreManager

def main():
    print("==========================================")
    print(" Starting Multi-Category RAG Ingestion ")
    print("==========================================")
    print("Scanning documents...\n")

    loader = MultiCategoryDocumentLoader()
    splitter = TextSplitterManager()
    vectorstore_mgr = VectorStoreManager()
    
    print("Resetting ChromaDB index for local embedding compatibility...")
    vectorstore_mgr.clear_all()
    print("ChromaDB index reset successfully.\n")
    
    total_docs = 0
    total_chunks = 0

    for cat in CATEGORIES:
        label = CATEGORY_LABELS.get(cat, cat.capitalize())
        print(f"{label}:")
        
        raw_docs = loader.load_category_documents(cat)
        doc_count = len(set(d.metadata.get("document") for d in raw_docs)) if raw_docs else 0
        
        if not raw_docs:
            print(f"  Found 0 documents")
            print(f"  Created 0 chunks\n")
            continue
            
        chunks = splitter.split_documents(raw_docs)
        chunk_count = len(chunks)
        
        indexed_count = vectorstore_mgr.add_documents(chunks)
        
        print(f"  Found {doc_count} document(s)")
        print(f"  Created {chunk_count} chunk(s)\n")
        
        total_docs += doc_count
        total_chunks += chunk_count

    print("------------------------------------------")
    print(f"Indexing completed successfully.")
    print(f"Total Documents: {total_docs} | Total Chunks: {total_chunks}")
    print("==========================================")

if __name__ == "__main__":
    main()
