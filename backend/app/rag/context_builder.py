import re
from typing import List, Dict, Any, Tuple
from langchain_core.documents import Document
from app.config import DEMO_MODE, CATEGORY_LABELS

class ContextBuilder:
    """Compresses, deduplicates, and formats retrieved document chunks into clean LLM context and source cards."""

    @staticmethod
    def build_context(docs: List[Document]) -> Tuple[str, List[Dict[str, Any]]]:
        if not docs:
            return "", []

        context_blocks = []
        sources = []
        seen_sources = set()

        for idx, doc in enumerate(docs, 1):
            meta = doc.metadata or {}
            doc_name = meta.get("document", "official_guide.pdf")
            raw_cat = meta.get("category", "general")
            category_label = CATEGORY_LABELS.get(raw_cat, raw_cat.title() if raw_cat else "General")
            page_num = meta.get("page", 1)
            section = meta.get("section", f"Page {page_num}")
            source_url = meta.get("source_url", "")

            source_type = meta.get("source_type", "Demo Knowledge Base" if DEMO_MODE else "Official Document")
            text = doc.page_content.strip()

            context_blocks.append(
                f"SOURCE:\n"
                f"Document: {doc_name}\n"
                f"Category: {category_label}\n"
                f"Page: {page_num}\n"
                f"Section: {section}\n"
                f"Source Type: {source_type}\n\n"
                f"CONTENT:\n"
                f"{text}\n"
            )

            clean_text = re.sub(r'^(?:DEMO KNOWLEDGE BASE|Category:[^\n]*|Section:[^\n]*|Page:[^\n]*|\s+)+', '', text, flags=re.IGNORECASE).strip()
            if not clean_text:
                clean_text = text

            src_key = (doc_name, page_num, section)
            if src_key not in seen_sources:
                seen_sources.add(src_key)
                src_entry = {
                    "document": doc_name,
                    "category": category_label,
                    "page": page_num,
                    "section": section,
                    "source_type": source_type,
                    "excerpt": clean_text[:250] + "..." if len(clean_text) > 250 else clean_text
                }
                if source_url:
                    src_entry["source_url"] = source_url
                sources.append(src_entry)

        full_context = "\n---\n".join(context_blocks)
        return full_context, sources
