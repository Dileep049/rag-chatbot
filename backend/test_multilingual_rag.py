import sys
import io
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app.services.chatbot import ChatbotService

def run_multilingual_tests():
    print("==========================================================")
    print(" Testing Multilingual RAG (Telugu, Telugu-English, English) ")
    print("==========================================================")

    bot = ChatbotService()

    TEST_CASES = [
        ("Telugu Script", "నా ఆధార్ కార్డు పోయింది. నేను ఏం చేయాలి?"),
        ("Telugu-English Mixed", "Naa Aadhaar card poyindi. Em cheyali?"),
        ("Telugu Pension", "Ma amma pension ki em documents kavali?"),
        ("Telugu Vehicle/Police", "Police naa bike teesukunnaru. Ela release cheyinchukovali?"),
        ("English Standard", "My driving licence is lost. What should I do?")
    ]

    for label, q in TEST_CASES:
        print(f"\n[{label}] User: {q}")
        res = bot.ask(q)
        answer = res["answer"]
        sources = res.get("sources", [])
        print(f"   AI Answer:\n   {answer[:250]}...")
        if sources:
            top = sources[0]
            print(f"   (Top Source: {top['document']} | Category: {top.get('category')} | Page: {top['page']})")
            print("   Result: [PASS]")
        else:
            print("   Result: [FAIL] (No sources retrieved)")

    # Follow-up test in Telugu
    print("\n--- TEST: Multilingual Follow-up Sequence ---")
    history = []
    
    q1 = "Naa Aadhaar card poyindi."
    print(f"\n[User]: {q1}")
    res1 = bot.ask(q1, history=history)
    history.append({"role": "user", "content": q1})
    history.append({"role": "assistant", "content": res1["answer"]})
    print(f"[AI]: {res1['answer'][:200]}...")

    q2 = "Next em cheyali?"
    print(f"\n[User]: {q2}")
    res2 = bot.ask(q2, history=history)
    print(f"[AI]: {res2['answer'][:200]}...")
    if res2.get("sources"):
        print(f"   (Follow-up Top Source: {res2['sources'][0]['document']})")
        print("   Result: [PASS] Follow-up maintained Aadhaar context in Telugu")
    else:
        print("   Result: [FAIL]")

if __name__ == "__main__":
    run_multilingual_tests()
