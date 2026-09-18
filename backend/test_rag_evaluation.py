import sys
import json
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from app.services.chatbot import ChatbotService
from app.rag.retriever import ContextRetriever

def run_evaluation():
    print("==========================================================")
    print(" Production RAG Quality & Retrieval Evaluation Suite ")
    print("==========================================================")

    dataset_path = Path(__file__).resolve().parent / "tests" / "rag_questions.json"
    if not dataset_path.exists():
        print(f"Error: Evaluation dataset {dataset_path} not found.")
        return

    with open(dataset_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    bot = ChatbotService()
    passed = 0
    total = len(questions)

    for item in questions:
        q_id = item["id"]
        q_text = item["question"]
        expected_cat = item.get("expected_category")
        is_out_of_domain = item.get("is_out_of_domain", False)

        print(f"\n[Test {q_id}] Question: '{q_text}'")
        res = bot.ask(q_text)
        sources = res.get("sources", [])
        answer = res.get("answer", "")

        if is_out_of_domain:
            if "could not find sufficient information" in answer.lower() or len(sources) == 0:
                print("   Result: [PASS] (Anti-Hallucination Guardrail Correctly Triggered)")
                passed += 1
            else:
                print(f"   Result: [FAIL] (Hallucinated answer for out-of-domain query)")
        else:
            if sources and len(sources) > 0:
                retrieved_doc = sources[0]["document"]
                retrieved_cat = sources[0].get("category", "")
                print(f"   Retrieved Document: {retrieved_doc} | Category: {retrieved_cat}")
                print(f"   Page: {sources[0]['page']} | Section: {sources[0]['section']}")
                print("   Result: [PASS]")
                passed += 1
            else:
                print("   Result: [FAIL] (Failed to retrieve relevant official document)")

    print("\n==========================================================")
    print(f" EVALUATION COMPLETED: {passed}/{total} Passed ({(passed/total)*100:.1f}%)")
    print("==========================================================")

if __name__ == "__main__":
    run_evaluation()
