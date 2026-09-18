import re
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from app.rag.vectorstore import VectorStoreManager
from app.rag.query_processor import QueryProcessor
from app.rag.reranker import RAGReranker
from app.rag.context_builder import ContextBuilder
from app.config import RAG_TOP_K, RAG_FINAL_K, RAG_RELEVANCE_THRESHOLD, RAG_DEBUG

OFFICIAL_DOMAIN_KEYWORDS = [
    "aadhaar", "uidai", "eid", "uid", "pension", "ignoaps", "senior citizen", "police", "fir", 
    "complaint", "vehicle", "bike", "car", "seized", "impound", "rto", "superdari", 
    "pan", "license", "licence", "driving", "pm-kisan", "ayushman", "scheme", "welfare"
]

class ContextRetriever:
    """Production RAG Retriever with Hybrid Retrieval, Query Expansion, Reranking, and Thresholding."""
    
    def __init__(self, vectorstore: Optional[VectorStoreManager] = None):
        self.vs_manager = vectorstore or VectorStoreManager()
        self.reranker = RAGReranker(threshold=RAG_RELEVANCE_THRESHOLD, final_k=RAG_FINAL_K)

    def detect_category(self, question: str) -> Optional[str]:
        """Automatic keyword/heuristic category detector before retrieval."""
        q = question.lower()
        
        if any(k in q for k in ["aadhaar", "uidai", "eid", "uid"]):
            return "aadhaar"
        if any(k in q for k in ["pension", "old age", "ignoaps", "senior citizen", "widow pension"]):
            return "pension"
        if any(k in q for k in ["police", "fir", "complaint", "sho", "station", "cognizable", "zero fir"]):
            return "police"
        if any(k in q for k in ["bike", "car", "vehicle", "seize", "seized", "impound", "rto", "mv act", "superdari"]):
            return "vehicle"
        if any(k in q for k in ["pan card", "pan ", "nsdl", "utiitsl", "e-pan"]):
            return "pan"
        if any(k in q for k in ["driving licence", "driving license", "dl", "parivahan", "lld"]):
            return "driving_license"
        if any(k in q for k in ["scheme", "pm-kisan", "kisan", "ayushman", "pm-jay", "benefit", "subsidy"]):
            return "schemes"
            
        return None

    def get_relevant_context(
        self, 
        question: str, 
        category: Optional[str] = None, 
        top_k: int = RAG_TOP_K
    ) -> Dict[str, Any]:
        """Hybrid Retrieval -> Candidate Pool -> Reranking -> Relevance Threshold -> Context Selection."""
        target_category = category or self.detect_category(question)
        q_lower = question.lower()
        
        from app.config import DEMO_MODE
        
        # In DEMO_MODE, bypass domain pre-check so all demo questions run through vector similarity search
        if not DEMO_MODE:
            has_domain_terms = any(kw in q_lower for kw in OFFICIAL_DOMAIN_KEYWORDS)
            if not has_domain_terms and not target_category:
                if RAG_DEBUG:
                    print(f"[RAG DEBUG] Query '{question}' lacks domain terms and category. Returning empty.")
                return {
                    "context_text": "",
                    "documents": [],
                    "sources": [],
                    "detected_category": None
                }

        # 1. Hybrid Candidate Retrieval (Query Variations)
        expansions = QueryProcessor.generate_expansions(question, target_category)
        candidate_pool: List[Document] = []
        seen_ids = set()

        for q_var in expansions:
            docs = self.vs_manager.similarity_search(
                query=q_var,
                category=target_category,
                k=top_k
            )
            for doc in docs:
                chunk_id = f"{doc.metadata.get('document')}_{doc.metadata.get('page')}_{doc.page_content[:50]}"
                if chunk_id not in seen_ids:
                    seen_ids.add(chunk_id)
                    candidate_pool.append(doc)

        if RAG_DEBUG:
            print("\n[RAG DEBUG]")
            print(f"Original Question:\n{question}\n")
            print(f"Collection:\n{self.vs_manager.collection_name}\n")
            if candidate_pool:
                top_m = candidate_pool[0].metadata or {}
                print("Retrieved:")
                print(f"Document: {top_m.get('document')}")
                print(f"Category: {top_m.get('category')}")
                print(f"Section: {top_m.get('section')}")
                print(f"Page: {top_m.get('page')}")
            print(f"\nRetrieved chunks: {len(candidate_pool)}\n")

        # 2. Reranking & Relevance Thresholding
        selected_docs, is_sufficient = self.reranker.score_and_rerank(
            query=question,
            candidate_docs=candidate_pool,
            target_category=target_category
        )

        if not is_sufficient or not selected_docs:
            return {
                "context_text": "",
                "documents": [],
                "sources": [],
                "detected_category": target_category
            }

        # 3. Context Selection & Formatting
        context_text, sources = ContextBuilder.build_context(selected_docs)

        return {
            "context_text": context_text,
            "documents": selected_docs,
            "sources": sources,
            "detected_category": target_category
        }
