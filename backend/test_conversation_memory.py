import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from app.services.chatbot import ChatbotService

def run_memory_tests():
    print("==========================================================")
    print(" Testing Conversation Memory, Follow-ups & Topic Switch ")
    print("==========================================================")
    
    bot = ChatbotService()
    history = []

    def ask_and_print(q):
        print(f"\n[User]: {q}")
        res = bot.ask(q, history=history)
        answer = res["answer"]
        print(f"[AI]: {answer[:300]}...")
        if res.get("sources"):
            top_src = res["sources"][0]
            print(f"   (Top Source: {top_src['document']} | Category: {top_src.get('category')})")
        else:
            print("   (No Sources - Anti-Hallucination Triggered)")
        
        # Append to conversation history
        history.append({"role": "user", "content": q})
        history.append({"role": "assistant", "content": answer})

    # Test 1: Aadhaar Follow-up Sequence
    print("\n--- TEST 1: Aadhaar Follow-up Sequence ---")
    ask_and_print("My Aadhaar card is lost.")
    ask_and_print("What should I do?")
    ask_and_print("Can I get it online?")

    # Test 2: Topic Switch to Pension
    print("\n--- TEST 2: Topic Switch to Pension ---")
    ask_and_print("My mother wants to apply for pension.")
    ask_and_print("What documents are required?")

    # Test 3: Topic Switch to Vehicle / Police
    print("\n--- TEST 3: Topic Switch to Vehicle / Police ---")
    ask_and_print("Police seized my bike.")
    ask_and_print("How can I get it released?")

    # Test 4: Anti-Hallucination
    print("\n--- TEST 4: Anti-Hallucination Guardrail ---")
    ask_and_print("What is the official penalty fee for parking a spaceship on a public highway in 2026?")

if __name__ == "__main__":
    run_memory_tests()
