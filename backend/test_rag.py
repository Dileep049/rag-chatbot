import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from app.rag.loader import DocumentLoader
from app.rag.splitter import TextSplitter
from app.rag.vectorstore import VectorStoreManager
from app.services.chatbot import ChatbotService

def test_pipeline():
    print("--- 1. Testing Document Loader & Splitter ---")
    pages = DocumentLoader.load_document("data/aadhaar/aadhaar_official_guide.txt", category="aadhaar")
    print(f"Loaded {len(pages)} sections/pages from Aadhaar document.")
    
    splitter = TextSplitter()
    chunks = splitter.split_documents(pages)
    print(f"Generated {len(chunks)} chunks.")
    
    print("\n--- 2. Testing VectorStore Ingestion ---")
    vs = VectorStoreManager()
    count = vs.add_chunks(chunks)
    print(f"Indexed {count} chunks into ChromaDB.")
    
    print("\n--- 3. Testing Context Retrieval & Similarity Search ---")
    bot = ChatbotService()
    question = "My Aadhaar card is lost. What should I do?"
    res = bot.answer_question(question)
    
    print("\n=== QUESTION ===")
    print(question)
    print("\n=== ANSWER ===")
    print(res["answer"])
    print("\n=== SOURCES ===")
    for src in res["sources"]:
        print(f"- Doc: {src['document']} | Page: {src['page']} | Section: {src['section']}")
        
    print("\n[SUCCESS] RAG Pipeline Verification Complete!")

if __name__ == "__main__":
    test_pipeline()
