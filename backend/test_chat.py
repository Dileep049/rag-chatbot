import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from app.services.chatbot import ChatbotService

TEST_QUESTIONS = [
    "1. My Aadhaar card is lost. What should I do?",
    "2. How can I download my Aadhaar?",
    "3. What documents are required for Aadhaar update?",
    "4. Can I update my Aadhaar address?",
    "5. What should I do if I cannot find my Aadhaar number?"
]

def run_tests():
    print("==================================================")
    print(" Testing Citizen Assistance Aadhaar Chatbot RAG ")
    print("==================================================")
    
    bot = ChatbotService()
    
    for q in TEST_QUESTIONS:
        print(f"\nQuestion: {q}")
        res = bot.ask(q)
        print(f"\nAnswer:\n{res['answer']}")
        print("\nSources:")
        for src in res.get('sources', []):
            print(f"   - Document: {src['document']} | Page: {src['page']}")
        print("-" * 50)

if __name__ == "__main__":
    run_tests()
