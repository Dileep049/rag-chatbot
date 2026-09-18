import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True, encoding='utf-8')

from app.services.chatbot import ChatbotService
from app.config import DEMO_MODE, CHROMA_COLLECTION_NAME

def run_demo_test_suite():
    print("\n" + "="*80)
    print(f" EXECUTING FINAL DEMO SUITE (DEMO_MODE={DEMO_MODE})")
    print(f" Active Collection: {CHROMA_COLLECTION_NAME}")
    print("="*80 + "\n")

    chatbot = ChatbotService()

    demo_questions = [
        ("Question 1", "My Aadhaar card is lost. What should I do?"),
        ("Question 2", "How can I download E-Aadhaar?"),
        ("Question 3", "How can I update my Aadhaar address?"),
        ("Question 4", "What documents are required for Aadhaar update?"),
        ("Question 5", "What is E-Aadhaar?"),
        ("Question 6", "My vehicle was seized by police. What should I do?"),
        ("Question 7", "How can I apply for a driving licence?"),
        ("Question 8", "What documents are required for pension?"),
        ("Question 9 (Unknown)", "How can I apply for a passport?")
    ]

    for label, q in demo_questions:
        print(f"--- {label} ---")
        print(f"USER QUESTION: {q}")
        res = chatbot.ask(q)
        print("\nGROUNDED ANSWER:")
        print(res["answer"])
        print("\nSOURCES RETURNED:")
        for s in res.get("sources", []):
            print(f"  📄 Document: {s.get('document')}")
            print(f"     Category: {s.get('category')}")
            print(f"     Section:  {s.get('section')}")
            print(f"     Page:     {s.get('page')}")
            print(f"     Source:   {s.get('source_type')}")
        print("\n" + "-"*80 + "\n")

if __name__ == "__main__":
    run_demo_test_suite()
