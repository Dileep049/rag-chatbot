import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True, encoding='utf-8')

from app.services.chatbot import ChatbotService

def run_test_suite():
    chatbot = ChatbotService()
    
    questions = [
        ("Question 1", "My Aadhaar card is lost. What should I do?"),
        ("Question 3", "How can I download E-Aadhaar?"),
        ("Question 4", "How can I update my Aadhaar address?"),
        ("Question 5", "What documents are required for Aadhaar update?"),
        ("Question 6", "How can I apply for a driving licence?"),
        ("Question 7", "What documents are required for pension?")
    ]

    print("\n" + "="*80)
    print(" EXECUTING PROCEDURE AND REQUIREMENTS EVALUATION TEST SUITE")
    print("="*80 + "\n")

    for q_id, q in questions:
        print(f"--- [{q_id}] ---")
        print(f"QUESTION: {q}")
        res = chatbot.ask(q)
        ans = res["answer"]
        srcs = res.get("sources", [])
        print("\nANSWER:")
        print(ans)
        print("\nSOURCES:")
        for s in srcs:
            print(f"  - Document: {s.get('document')} | Category: {s.get('category')} | Section: {s.get('section')} | Page: {s.get('page')}")
        print("\n" + "-"*80 + "\n")

    # Follow-up test for Question 2 ("What documents/details are required?")
    print("--- [Question 2 - Follow-up Test] ---")
    q1 = "My Aadhaar card is lost. What should I do?"
    res1 = chatbot.ask(q1)
    history = [
        {"role": "user", "content": q1},
        {"role": "assistant", "content": res1["answer"]}
    ]
    q2 = "What documents/details are required?"
    print(f"FOLLOW-UP QUESTION: {q2}")
    print(f"HISTORY: {q1}")
    res2 = chatbot.ask(q2, history=history)
    print("\nFOLLOW-UP ANSWER:")
    print(res2["answer"])
    print("\nFOLLOW-UP SOURCES:")
    for s in res2.get("sources", []):
        print(f"  - Document: {s.get('document')} | Category: {s.get('category')} | Section: {s.get('section')} | Page: {s.get('page')}")
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    run_test_suite()
