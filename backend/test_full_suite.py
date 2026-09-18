import sys
import io
import traceback
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True, encoding='utf-8')

from tests.test_rag import (
    test_local_embedding_provider,
    test_ollama_llm_provider,
    test_document_loader, 
    test_text_splitter, 
    test_vectorstore_manager, 
    test_context_retriever, 
    test_reranker_relevance_threshold, 
    test_context_builder
)
from tests.test_chat import (
    test_chat_valid_question, 
    test_chat_empty_question, 
    test_chat_out_of_domain, 
    test_chat_with_conversation_history,
    test_chat_telugu_question,
    test_chat_mixed_language_question
)
from tests.test_documents import (
    test_unauthenticated_document_access, 
    test_admin_list_documents, 
    test_upload_and_delete_txt_document, 
    test_invalid_file_type_upload
)
from tests.test_auth import (
    test_admin_login_success, 
    test_admin_login_invalid_password, 
    test_auth_me_valid_token, 
    test_auth_me_invalid_token
)
from tests.test_security import (
    test_health_check_endpoint, 
    test_unauthenticated_api_protection, 
    test_security_headers_present
)
from test_rag_differentiation import test_question_differentiation

def run_all():
    print("==========================================================")
    print(" Executing Comprehensive Production RAG Unit & Integration Test Suite ")
    print("==========================================================")

    test_functions = [
        ("Local Embeddings Provider", test_local_embedding_provider),
        ("Ollama Local LLM Provider Config", test_ollama_llm_provider),
        ("RAG Document Loader", test_document_loader),
        ("RAG Text Splitter", test_text_splitter),
        ("RAG VectorStore Manager", test_vectorstore_manager),
        ("RAG Context Retriever", test_context_retriever),
        ("RAG Reranker & Threshold", test_reranker_relevance_threshold),
        ("RAG Context Builder", test_context_builder),
        ("Chat REST API Valid Question", test_chat_valid_question),
        ("Chat REST API Empty Input Validation", test_chat_empty_question),
        ("Chat REST API Out-of-Domain Anti-Hallucination", test_chat_out_of_domain),
        ("Chat REST API Conversation Memory", test_chat_with_conversation_history),
        ("Chat REST API Telugu Question", test_chat_telugu_question),
        ("Chat REST API Mixed-Language Question", test_chat_mixed_language_question),
        ("RAG Query Differentiation Verification", test_question_differentiation),
        ("Auth Unauthenticated Document API Blocking", test_unauthenticated_document_access),
        ("Auth Admin List Documents", test_admin_list_documents),
        ("Auth Admin Upload & Delete Document", test_upload_and_delete_txt_document),
        ("Auth Admin Upload File Validation", test_invalid_file_type_upload),
        ("Auth Admin Login Success", test_admin_login_success),
        ("Auth Admin Login Invalid Password", test_admin_login_invalid_password),
        ("Auth Valid Token Verification", test_auth_me_valid_token),
        ("Auth Invalid Token Rejection", test_auth_me_invalid_token),
        ("Security Health Check Endpoint", test_health_check_endpoint),
        ("Security Unauthenticated API Protection", test_unauthenticated_api_protection),
        ("Security HTTP Headers", test_security_headers_present)
    ]

    passed = 0
    total = len(test_functions)

    for name, fn in test_functions:
        print(f"\nRunning {name}...")
        try:
            fn()
            print(f"   Result: [PASS]")
            passed += 1
        except Exception as e:
            print(f"   Result: [FAIL] ({e})")
            traceback.print_exc()

    print("\n==========================================================")
    print(f" FULL TEST SUITE RESULT: {passed}/{total} Passed ({(passed/total)*100:.1f}%)")
    print("==========================================================")

if __name__ == "__main__":
    run_all()
