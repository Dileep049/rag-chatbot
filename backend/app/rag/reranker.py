import re
from typing import List, Dict, Any, Tuple, Optional
from langchain_core.documents import Document
from app.config import RAG_FINAL_K, RAG_RELEVANCE_THRESHOLD, RAG_DEBUG
from app.rag.query_processor import QueryProcessor

ACTION_KEYWORDS = {
    "lost", "download", "update", "change", "correction", "address", 
    "documents", "document", "seize", "seized", "seizure", "fir", 
    "complaint", "licence", "license", "pension", "scheme", "apply", 
    "application", "status", "retrieval", "retrieve", "duplicate"
}

class RAGReranker:
    """Reranks initial candidate retrieval pool using hybrid semantic-lexical scoring and relevance thresholding."""

    def __init__(self, threshold: float = RAG_RELEVANCE_THRESHOLD, final_k: int = RAG_FINAL_K):
        self.threshold = threshold
        self.final_k = min(final_k, 3)  # Target 1-3 highly relevant sources

    def score_and_rerank(
        self, 
        query: str, 
        candidate_docs: List[Document], 
        target_category: Optional[str] = None
    ) -> Tuple[List[Document], bool]:
        """Scores candidate chunks, filters low relevance scores, and returns top reranked chunks."""
        if not candidate_docs:
            return [], False

        query_keywords = QueryProcessor.extract_keywords(query)
        if not query_keywords:
            query_keywords = [query.lower()]

        q_lower = query.lower()
        query_actions = {kw for kw in ACTION_KEYWORDS if kw in q_lower}

        scored_chunks: List[Tuple[float, Document]] = []
        seen_texts = set()

        generic_kw = {"procedure", "process", "details", "information", "getting", "get", "help", "please"}
        subject_kws = [kw for kw in query_keywords if kw not in generic_kw]

        for doc in candidate_docs:
            text = doc.page_content.strip()
            text_lower = text.lower()

            # Deduplicate identical chunk texts
            if text in seen_texts:
                continue
            seen_texts.add(text)

            meta = doc.metadata or {}
            doc_cat = (meta.get("category") or "").lower()
            section = (meta.get("section") or "").lower()

            # Primary Subject Guardrail: If query specifies subject terms (e.g. 'passport'), chunk must match at least one subject term or category
            if subject_kws:
                has_subject_match = any(skw in text_lower or skw in doc_cat or skw in section for skw in subject_kws)
                if not has_subject_match:
                    scored_chunks.append((0.0, doc))
                    continue

            # Base score starting at baseline
            score = 0.05

            # 1. Lexical Keyword Density Match
            matches = sum(1 for kw in query_keywords if kw in text_lower)
            keyword_score = (matches / len(query_keywords)) * 0.5 if query_keywords else 0
            score += keyword_score

            # 2. Section Heading Match Boost
            if any(kw in section for kw in query_keywords):
                score += 0.15

            # 3. Category Match Boost
            if target_category and doc_cat == target_category.lower():
                score += 0.15

            # 4. Action / Sub-intent Alignment & Conflict Penalty
            if query_actions:
                sec_actions = {kw for kw in ACTION_KEYWORDS if kw in section}
                matching_actions = query_actions.intersection(sec_actions)
                conflicting_actions = sec_actions - query_actions

                requirement_kws = {"documents", "document", "requirements", "proof", "details"}
                is_req_section = bool(sec_actions.intersection(requirement_kws)) or any(rk in section for rk in requirement_kws)

                if matching_actions:
                    score += 0.25
                elif is_req_section and target_category and doc_cat == target_category.lower():
                    # Boost complementary requirement chunks in the same category
                    score += 0.15
                elif conflicting_actions and not is_req_section:
                    # Section explicitly focuses on a different action not requested in query
                    score -= 0.25

            # 5. Exact Entity Match Boost (e.g. Sections, Forms, Act numbers)
            entities = re.findall(r'\b(section\s+\d+|form\s+\d+[a-z]?|crpc|bnss|pvc|fir|rto)\b', q_lower)
            for ent in entities:
                if ent in text_lower:
                    score += 0.2

            # Floor score at 0.0
            score = max(0.0, score)
            scored_chunks.append((score, doc))

        # Sort by total relevance score descending
        scored_chunks.sort(key=lambda x: x[0], reverse=True)

        if RAG_DEBUG:
            print("\n[RAG DEBUG] Scored Candidates:")
            for s, d in scored_chunks[:5]:
                print(f"  - Score: {s:.3f} | Doc: {d.metadata.get('document')} | Sec: {d.metadata.get('section')}")

        if not scored_chunks:
            return [], False

        top_score, top_doc = scored_chunks[0]

        # Check against minimum relevance threshold
        if top_score < self.threshold:
            if RAG_DEBUG:
                print(f"[RAG DEBUG] Top score {top_score:.3f} below threshold {self.threshold}. Declaring insufficient.")
            return [], False

        # Adaptive Relative Thresholding: filter out chunks far below top score
        relative_min_score = max(self.threshold, top_score * 0.55)
        selected_docs = []
        for s, d in scored_chunks:
            if s >= relative_min_score and (top_score - s) <= 0.35:
                selected_docs.append(d)
            if len(selected_docs) >= self.final_k:
                break

        return selected_docs, bool(selected_docs)

