import sys
import io
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True, encoding='utf-8')

from app.services.chatbot import ChatbotService

def test_question_differentiation():
    print("==========================================================")
    print(" Testing RAG Retrieval & Answer Differentiation ")
    print("==========================================================")

    test_questions = [
        "My Aadhaar card is lost. What should I do?",
        "How can I download my E-Aadhaar online?",
        "What is E-Aadhaar?",
        "How can I retrieve my Aadhaar number?",
        "What should I do if my registered mobile number is unavailable?",
        "What documents are required for Aadhaar-related services?",
        "What is the Aadhaar enrolment process?",
        "Tell me something that is NOT present in the knowledge base."
    ]

    chatbot = ChatbotService()
    results = []

    for idx, q in enumerate(test_questions, 1):
        print(f"\n--- Question {idx}: '{q}' ---")
        res = chatbot.ask(question=q)
        ans = res.get("answer", "")
        sources = res.get("sources", [])
        
        first_src = sources[0] if sources else {}
        doc_name = first_src.get("document", "N/A")
        sec_name = first_src.get("section", "N/A")
        page_num = first_src.get("page", "N/A")
        
        print(f"Top Source: {doc_name} | Page {page_num} | Section: {sec_name}")
        print(f"Answer Snippet: {ans[:150]}...")
        sys.stdout.flush()
        
        results.append({
            "question": q,
            "answer": ans,
            "source": f"{doc_name}_p{page_num}_{sec_name}"
        })

    print("\n==========================================================")
    print(" SUMMARY OF RETRIEVED SOURCES ACROSS QUESTIONS:")
    print("==========================================================")
    for idx, r in enumerate(results, 1):
        print(f"Q{idx}: {r['source']}")

    unique_sources = set(r['source'] for r in results if r['source'] != "N/A_pN/A_N/A")
    print(f"\nUnique Relevant Source Sections Retrieved: {len(unique_sources)}")
    assert len(unique_sources) >= 3, "Different questions must retrieve different relevant source sections!"
    print("\n[SUCCESS] RAG question differentiation verified successfully!")

if __name__ == "__main__":
    test_question_differentiation()
