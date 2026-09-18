from app.rag.loader import MultiCategoryDocumentLoader
from app.rag.splitter import TextSplitterManager
from app.rag.vectorstore import VectorStoreManager
from app.rag.retriever import ContextRetriever
from app.rag.reranker import RAGReranker
from app.rag.context_builder import ContextBuilder
from app.rag.embeddings import get_embeddings_service
from app.config import LLM_PROVIDER, EMBEDDING_PROVIDER
from langchain_core.documents import Document

def test_local_embedding_provider():
    emb = get_embeddings_service()
    assert emb is not None
    assert EMBEDDING_PROVIDER == "local"
    vec1 = emb.embed_query("Aadhaar card process")
    assert isinstance(vec1, list)
    assert len(vec1) > 0
    vec_docs = emb.embed_documents(["Test document content"])
    assert isinstance(vec_docs, list)
    assert len(vec_docs) == 1
    assert len(vec_docs[0]) == len(vec1), "Embedding dimensions must be consistent"

def test_ollama_llm_provider():
    assert LLM_PROVIDER == "ollama"

def test_document_loader():
    loader = MultiCategoryDocumentLoader()
    docs = loader.load_all_documents()
    assert isinstance(docs, list)
    assert len(docs) > 0, "Knowledge base documents should be loaded from data/"
    
    sample = docs[0]
    assert "document" in sample.metadata
    assert "category" in sample.metadata
    assert "page" in sample.metadata

def test_text_splitter():
    splitter = TextSplitterManager(chunk_size=300, chunk_overlap=50)
    sample_doc = Document(
        page_content="Header Section\n\nThis is a test paragraph for document splitting. " * 10,
        metadata={"document": "test.txt", "category": "aadhaar", "page": 1}
    )
    chunks = splitter.split_documents([sample_doc])
    assert len(chunks) > 1
    assert chunks[0].metadata["document"] == "test.txt"

def test_vectorstore_manager():
    vs = VectorStoreManager()
    indexed_docs = vs.get_indexed_documents()
    assert isinstance(indexed_docs, list)

def test_context_retriever():
    retriever = ContextRetriever()
    res = retriever.get_relevant_context("My Aadhaar card is lost.")
    assert "context_text" in res
    assert "sources" in res

def test_reranker_relevance_threshold():
    reranker = RAGReranker(threshold=0.20, final_k=4)
    # High relevance candidates
    docs = [
        Document(page_content="Lost Aadhaar card replacement process", metadata={"category": "aadhaar", "document": "a.txt", "section": "Lost Aadhaar"}),
        Document(page_content="Unrelated text about cooking", metadata={"category": "general", "document": "b.txt", "section": "General"})
    ]
    selected, sufficient = reranker.score_and_rerank("lost aadhaar card", docs, target_category="aadhaar")
    assert len(selected) > 0
    assert sufficient is True

    # Low relevance candidates
    unrelated_docs = [
        Document(page_content="Quantum physics wave particle duality", metadata={"category": "physics", "document": "p.txt", "section": "Quantum"})
    ]
    selected_empty, sufficient_fail = reranker.score_and_rerank("how to recover lost pension card", unrelated_docs)
    assert len(selected_empty) == 0
    assert sufficient_fail is False

def test_context_builder():
    docs = [
        Document(page_content="Procedure step 1...", metadata={"document": "guide.pdf", "category": "aadhaar", "page": 2, "section": "Section A"}),
        Document(page_content="Procedure step 2...", metadata={"document": "guide.pdf", "category": "aadhaar", "page": 2, "section": "Section A"})
    ]
    text, sources = ContextBuilder.build_context(docs)
    assert "[Source Document 1:" in text
    assert len(sources) == 1 # Deduplicated same page & section
    assert sources[0]["document"] == "guide.pdf"
