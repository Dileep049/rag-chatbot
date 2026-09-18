import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True, encoding='utf-8')

from app.services.chatbot import ChatbotService

def run_test_suite():
    chatbot = ChatbotService()
    
    questions = [
        ("Question 1 - Aadhaar Lost", "My Aadhaar card is lost. What should I do?"),
        ("Question 2 - Aadhaar Doc Required", "What documents are required for Aadhaar update?"),
        ("Question 3 - Download E-Aadhaar", "How can I download E-Aadhaar?"),
        ("Question 4 - What is E-Aadhaar", "What is E-Aadhaar?"),
        ("Question 5 - Update Address", "How can I update my Aadhaar address?"),
        ("Question 6 - Police Seizure", "My vehicle was seized by police. What should I do?"),
        ("Question 7 - Driving Licence", "How can I apply for a driving licence?"),
        ("Question 8 - Pension Docs", "What documents are required for pension?"),
        ("Question 9 - Unsupported Passport", "How can I apply for a passport?"),
        ("Question 10 - Telugu English Mixed", "Aadhaar update ki em documents kavali?")
    ]

    print("\n" + "="*80)
    print(" EXECUTING FINAL 26-RULE CITIZEN ASSISTANCE RAG EVALUATION SUITE")
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

    # Follow-up test
    print("--- [Follow-up Memory Test] ---")
    q1 = "My Aadhaar card is lost. What should I do?"
    res1 = chatbot.ask(q1)
    history = [
        {"role": "user", "content": q1},
        {"role": "assistant", "content": res1["answer"]}
    ]
    q_followup = "What documents are required?"
    print(f"FOLLOW-UP QUESTION: {q_followup}")
    print(f"HISTORY: {q1}")
    res_followup = chatbot.ask(q_followup, history=history)
    print("\nFOLLOW-UP ANSWER:")
    print(res_followup["answer"])
    print("\nFOLLOW-UP SOURCES:")
    for s in res_followup.get("sources", []):
        print(f"  - Document: {s.get('document')} | Category: {s.get('category')} | Section: {s.get('section')} | Page: {s.get('page')}")
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    run_test_suite()
