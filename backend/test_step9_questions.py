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
        ("Question 2", "How can I download E-Aadhaar?"),
        ("Question 3", "How can I update my Aadhaar address?"),
        ("Question 4", "What documents are required for Aadhaar update?"),
        ("Question 5", "What is E-Aadhaar?"),
        ("Question 6", "My vehicle was seized by police. What should I do?"),
        ("Question 7", "How can I apply for a driving licence?"),
        ("Question 8", "What documents are required for pension?"),
        ("Question 9", "How can I apply for a passport?")
    ]

    print("\n" + "="*80)
    print(" EXECUTING ALL 9 DEMO RAG EVALUATION QUESTIONS")
    print("="*80 + "\n")

    results = []
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
            print(f"  - Document: {s.get('document')} | Category: {s.get('category')} | Section: {s.get('section')} | Page: {s.get('page')} | Source Type: {s.get('source_type')}")
        print("\n" + "-"*80 + "\n")
        results.append((q_id, q, ans, srcs))

    # Follow-up test
    print("--- [Follow-up Test] ---")
    q1 = "My Aadhaar card is lost. What should I do?"
    res1 = chatbot.ask(q1)
    history = [
        {"role": "user", "content": q1},
        {"role": "assistant", "content": res1["answer"]}
    ]
    q_followup = "What should I do next?"
    print(f"FOLLOW-UP QUESTION: {q_followup}")
    print(f"HISTORY: {history[0]['content']}")
    res_followup = chatbot.ask(q_followup, history=history)
    print("\nFOLLOW-UP ANSWER:")
    print(res_followup["answer"])
    print("\nFOLLOW-UP SOURCES:")
    for s in res_followup.get("sources", []):
        print(f"  - Document: {s.get('document')} | Category: {s.get('category')} | Section: {s.get('section')} | Page: {s.get('page')}")
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    run_test_suite()
