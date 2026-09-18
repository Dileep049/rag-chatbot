# 📊 Presentation Slides — Citizen Assistance AI

This document contains slide content for a 15-slide PowerPoint / Google Slides presentation deck.

---

### Slide 1: Title Slide
- **Title**: 🇮🇳 Citizen Assistance AI
- **Subtitle**: Production-Grade Multilingual RAG Chatbot for Government & Citizen Services
- **Presenter**: [Student / Project Team Name]
- **Technologies**: React, FastAPI, LangChain, ChromaDB, OpenAI GPT-4o-mini

---

### Slide 2: Problem Statement
- **Fragmented Official Information**: Guidelines spread across lengthy PDF files and department portals.
- **AI Hallucinations**: Standard LLMs invent non-existent legal sections, fees, and office procedures.
- **Language Barrier**: Formal documentation is predominantly in English, causing friction for regional language speakers.
- **Lack of Verifiable Sources**: Citizens cannot easily verify answers back to official source documents.

---

### Slide 3: Project Objectives
- Build a clean ChatGPT-style conversational assistant without forced category selection.
- Implement an automated RAG document ingestion pipeline for PDF, DOCX, and TXT files.
- Combine semantic vector search with BM25 keyword matching and score-based reranking.
- Enforce strict relevance thresholding to eliminate AI hallucinations.
- Support queries in English, Native Telugu script, and Telugu-English phonetic spelling.
- Add browser Voice Input and RBAC security for document management.

---

### Slide 4: Existing vs. Proposed System
| Feature | Traditional Search / Generic LLM | Proposed Citizen Assistance AI |
| :--- | :--- | :--- |
| **Grounding** | Parametric memory (can hallucinate) | Strict RAG Grounding in official documents |
| **Sources** | Commercial blogs / No citations | Verifiable Document, Page & Section cards |
| **Languages** | Single language focus | English, Native Telugu & Telugu-English |
| **Unknown Queries** | Guesses plausible answers | Refuses with safe No-Information notice |
| **Admin Hub** | Static database updates | Real-time document upload & vector indexing |

---

### Slide 5: System Architecture
- **Frontend**: React + Vite + Tailwind CSS + Web Speech API Voice Input
- **Backend**: FastAPI + Uvicorn + Base64 HMAC-SHA256 JWT Security
- **RAG Engine**: LangChain Core + QueryProcessor + RAGReranker + ContextBuilder
- **Vector DB**: ChromaDB (`langchain-chroma`)
- **LLM**: OpenAI GPT-4o-mini (Strict Grounding Prompt)

---

### Slide 6: RAG Retrieval Methodology
- **Document Chunking**: 700-character chunks with 150-character overlap preserving page & section titles.
- **Hybrid Candidate Pool**: Retrieves top 15 candidate chunks from ChromaDB.
- **Reranking Engine**: Evaluates vector similarity, BM25 term density, heading matches, and entity extraction (*"Section 207"*, *"Form 49A"*).
- **Relevance Threshold**: Filters candidate pool against `RAG_RELEVANCE_THRESHOLD` (`0.20`).

---

### Slide 7: Technology Stack
- **Languages**: Python 3.11, JavaScript (ES6+)
- **API Framework**: FastAPI, Pydantic, Starlette
- **AI Orchestration**: LangChain, OpenAI API
- **Vector Storage**: ChromaDB
- **UI & Styling**: React 18, Vite, Tailwind CSS, Lucide Icons

---

### Slide 8: Core User Features
- **ChatGPT-Style Layout**: Natural typing experience with auto-expanding text box and scroll pill.
- **Interactive Suggestions**: Clickable English & Telugu prompt pills.
- **Copy & Regenerate**: One-click visible text copying and message regeneration.
- **Source Cards**: Accordion displaying document name, category, section, page number, and source URL.

---

### Slide 9: Multilingual & Voice Input
- **Multilingual Query Understanding**: Automatically translates Telugu script (`నా ఆధార్ కార్డు పోయింది`) and phonetic spelling (`Naa Aadhaar card poyindi`) to search concepts.
- **Natural Responding**: Responds in user's input language.
- **Voice Input**: Web Speech Recognition in English (`en-IN`) and Telugu (`te-IN`).

---

### Slide 10: Anti-Hallucination & Legal Safety
- **Relevance Thresholding**: Rejects weak candidate chunks.
- **No-Information Notice**: *"I could not find sufficient information in the available official documents to answer this question."*
- **Legal/Police Disclaimer**: Provides general informational guidance without inventing legal sections.

---

### Slide 11: Admin Hub & Document Management
- **Protected Admin Page (`/admin`)**: Requires JWT login (`admin@citizen.gov.in`).
- **Drag & Drop Upload**: Supports PDF, DOCX, and TXT uploads up to 15MB.
- **Real-Time Indexing**: Document chunking and ChromaDB vector persistence on upload.
- **Document Operations**: Re-index single/all documents, list indexed files, and delete documents.

---

### Slide 12: Security & Production Hardening
- **Authentication**: Base64 HMAC-SHA256 JWT tokens.
- **API Access Control**: Admin document endpoints return `401 Unauthorized` without token.
- **Input Validation**: Path traversal sanitization, extension whitelist, file size caps.
- **Middleware**: IP rate-limiting (60 req/min for chat) and security headers (`X-Frame-Options: DENY`).

---

### Slide 13: Testing & Evaluation Results
- **Automated Test Suite (`test_full_suite.py`)**: 21/21 Tests Passed (100.0%).
- **Evaluation Dataset (`rag_questions.json`)**: 30 evaluation questions across all categories.
- **Out-of-Domain Accuracy**: 100% success in triggering anti-hallucination guardrail.

---

### Slide 14: System Limitations & Future Scope
- **Limitations**: Ingestion quality dependent on uploaded official documents; scanned PDFs require OCR.
- **Future Scope**:
  1. Integration with official state government APIs (DigiLocker).
  2. Text-to-Speech (TTS) voice answers.
  3. Multi-modal RAG for tables and graphics.

---

### Slide 15: Conclusion & Q&A
- **Summary**: Delivered a secure, production-grade, multilingual RAG AI assistant grounded in official government documents.
- **Thank You!**
- **Questions & Answers**
