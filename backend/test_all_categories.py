import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from app.services.chatbot import ChatbotService

TEST_QUESTIONS = [
    ("Aadhaar", "My Aadhaar card is lost. What should I do?"),
    ("Pension", "What documents are required for pension?"),
    ("Police", "How can I file a police complaint?"),
    ("Vehicle", "Police seized my bike. What is the procedure to get it released?"),
    ("PAN", "My PAN card is lost. How can I get another one?"),
    ("Driving Licence", "My driving licence is lost. What should I do?"),
    ("Schemes", "How can I apply for PM-Kisan government scheme?"),
    ("Unknown Info", "What is the fee for obtaining a private commercial helicopter license in 2026?")
]

def run_tests():
    print("==========================================================")
    print(" Testing Multi-Category RAG Engine & Anti-Hallucination ")
    print("==========================================================")
    
    bot = ChatbotService()
    
    for category_label, q in TEST_QUESTIONS:
        print(f"\n[{category_label}] Question: {q}")
        res = bot.ask(q)
        print(f"\nAnswer:\n{res['answer']}")
        print("\nSources:")
        if res.get('sources'):
            for src in res['sources']:
                print(f"   - Document: {src['document']} | Category: {src.get('category')} | Page: {src['page']}")
        else:
            print("   - No sources retrieved (Anti-Hallucination Active)")
        print("-" * 60)

if __name__ == "__main__":
    run_tests()
