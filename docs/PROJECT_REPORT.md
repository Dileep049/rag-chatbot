# 📑 Academic Project Report — Citizen Assistance AI

## 1. Title Page
**Project Title**: Citizen Assistance AI — Production-Grade Multilingual RAG Chatbot  
**Domain**: Artificial Intelligence, Natural Language Processing, Retrieval-Augmented Generation (RAG)  
**Technology Stack**: Python, FastAPI, LangChain, OpenAI GPT-4o-mini, ChromaDB, React.js, Tailwind CSS  

---

## 2. Abstract
The **Citizen Assistance AI** system is a grounded, production-ready Retrieval-Augmented Generation (RAG) web application designed to help citizens inquire about Indian government services, procedural guidelines, pensions, police procedures, vehicle impoundments, Aadhaar recovery, PAN cards, driving licences, and welfare schemes.

Built using FastAPI, LangChain, ChromaDB vector store, and React, the system processes multi-category PDF, DOCX, and TXT official documents into semantic chunks. It features a hybrid retrieval pipeline combining vector similarity search with BM25 keyword matching, entity extraction, score-based reranking, and strict relevance thresholding (`RAG_RELEVANCE_THRESHOLD = 0.20`). It supports queries in English, Native Telugu script, and Telugu-English phonetic spelling, along with integrated browser Voice Input. All administrative document management endpoints are secured using HMAC-SHA256 Base64 JWT Role-Based Access Control (RBAC).

---

## 3. Introduction & Background
Navigating government procedures, legal rights, and welfare scheme documentation is frequently challenging for citizens due to complex legal phrasing, lengthy PDF guidelines, and language barriers. Existing public LLMs often hallucinate office procedures, legal sections, and required documents. 

This project bridges this gap by grounding conversational AI answers strictly in indexed department guidelines, providing verified source citations (document name, page number, section title) and multi-language comprehension.

---

## 4. Problem Statement
1. **Unreliable AI Answers**: Standard generative models generate plausible but incorrect information regarding fees, legal sections, and government application processes.
2. **Document Fragmented Across Portals**: Guidelines are distributed across multiple department portals in dense PDF files.
3. **Language Barriers**: Information is predominantly published in formal English, making it hard for regional language speakers to navigate.
4. **Lack of Verifiable Sources**: Traditional search engines return commercial blogs rather than official department notices.

---

## 5. System Objectives
- Develop a clean ChatGPT-style interface without forcing manual category selection.
- Implement an automated RAG ingestion pipeline supporting PDF, DOCX, and TXT file formats.
- Design a hybrid candidate retrieval and reranking engine to prioritize relevant chunks.
- Enforce strict anti-hallucination relevance thresholding.
- Provide multilingual support for English, Native Telugu script, and Telugu-English phonetic input.
- Enable hands-free voice input via Web Speech Recognition.
- Implement RBAC security protecting Admin document management APIs.

---

## 6. System Architecture & RAG Methodology

### 6.1 System Architecture Diagram

```text
Official Documents (PDF, DOCX, TXT)
            │
            ▼
 Text Extraction & Section Parsing
            │
            ▼
  Chunking (TextSplitterManager)
            │
            ▼
 OpenAI Embeddings / Fallback Generator
            │
            ▼
   ChromaDB Persistent Vector Store
            │
            ▼
    User Question (Text / Voice)
            │
            ▼
 Language Understanding & Concept Translation
            │
            ▼
 Query Rewriting & Topic Switcher
            │
            ▼
 Candidate Pool Retrieval (Top 15 Chunks)
            │
            ▼
 RAG Reranker (BM25 + Semantic + Entity Matches)
            │
            ▼
 Relevance Threshold Filter (Score >= 0.20)
       /                 \
 Pass Threshold      Fail Threshold
       │                   │
       ▼                   ▼
ContextBuilder     Anti-Hallucination Guardrail
 (Compression)   ("I could not find sufficient...")
       │
       ▼
OpenAI LLM (GPT-4o-mini)
 (Strict Grounding)
       │
       ▼
Grounded Multilingual Answer + Verified Sources
       │
       ▼
 React Chat UI (Copy, Retry, Accordion Sources)
```

---

## 7. System Modules

### 7.1 Document Ingestion & Chunking (`backend/app/rag/loader.py`, `splitter.py`)
- Extracts document text and preserves section headers and page metadata.
- Dividers text into overlapping 700-character chunks with 150-character overlap.

### 7.2 Hybrid Retrieval & Reranker (`backend/app/rag/retriever.py`, `reranker.py`)
- Retrieves a candidate pool of 15 chunks from ChromaDB.
- Scores candidates based on vector similarity, BM25 term density, heading matches, and entity extraction (e.g. *"Section 207"*, *"Form 49A"*).
- Applies `RAG_RELEVANCE_THRESHOLD` (`0.20`). Returns empty context when top score is insufficient.

### 7.3 Multilingual Query Processor (`backend/app/rag/query_processor.py`)
- Maps Telugu script and Telugu-English phonetic tokens into English search concepts for vector retrieval.
- Instructs the LLM system prompt to respond in the user's natural language.

### 7.4 Security & Admin Hub (`backend/app/auth/`, `routes/documents.py`)
- Issues HMAC-SHA256 Base64 JWT tokens for Admin authentication (`admin@citizen.gov.in`).
- Protects document management APIs (`POST /upload`, `GET /documents`, `DELETE`) with `Depends(require_admin)`.

---

## 8. Testing & Evaluation Results
The system was evaluated using an automated test suite (`test_full_suite.py`) and a 30-question evaluation dataset (`tests/rag_questions.json`).

| Test Suite Module | Test Coverage | Pass Rate |
| :--- | :--- | :--- |
| **RAG Pipeline** | Loading, Chunking, Vectorstore, Retrieval, Reranking, Thresholding | **100% (6/6)** |
| **Chat REST API** | Valid queries, empty inputs, out-of-domain guardrails, history | **100% (4/4)** |
| **Document APIs** | Upload, file validation, listing, re-indexing, deletion | **100% (4/4)** |
| **Authentication** | Login, invalid password, JWT validation, token rejection | **100% (4/4)** |
| **Security & Headers**| RBAC protection, health check, HTTP security headers | **100% (3/3)** |
| **Total Test Suite** | **Comprehensive Full Integration Suite** | **100% (21/21)** |

---

## 9. System Limitations & Future Scope

### Limitations
1. Grounding relies on the coverage and quality of uploaded official documents.
2. Web Speech Voice Input depends on browser support (Google Chrome, Edge, Safari).
3. Image-only scanned PDFs require OCR pre-processing.

### Future Scope
1. Integration with official state government APIs (DigiLocker, e-District).
2. Text-to-Speech (TTS) audio answers in regional Indian languages.
3. Multi-modal RAG for processing document tables, graphs, and infographics.

---

## 10. Conclusion
The **Citizen Assistance AI** project successfully demonstrates a production-grade, secure, and grounded multilingual RAG solution. By combining hybrid retrieval, reranking, anti-hallucination thresholding, role-based security, and a ChatGPT-style interface, the system provides reliable and verifiable guidance for citizens inquiring about government services.
