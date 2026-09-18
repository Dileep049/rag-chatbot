# 🇮🇳 Citizen Assistance AI — Production-Grade RAG Chatbot

An intelligent, grounded **Citizen Assistance RAG Chatbot** built with **FastAPI**, **LangChain**, **ChromaDB**, **OpenAI GPT-4o-mini**, and **React (Vite + Tailwind CSS)**. Designed to provide accurate, reliable, and strictly grounded answers to citizens inquiring about Indian official government services, procedures, police complaints, pensions, Aadhaar, vehicle procedures, PAN cards, driving licences, and government schemes.

---

## 📚 Documentation & Viva Artifacts (`docs/`)

- 🎓 [**Viva Preparation Guide (`docs/VIVA.md`)**](file:///d:/chatbot/docs/VIVA.md): 30 detailed Viva Voce questions & answers covering AI, RAG, ChromaDB, FastAPI, React, Security, and System Limitations.
- 🎬 [**Live Demo Script (`docs/DEMO_SCRIPT.md`)**](file:///d:/chatbot/docs/DEMO_SCRIPT.md): Step-by-step 7-minute presentation and live demonstration sequence.
- 📑 [**Academic Project Report (`docs/PROJECT_REPORT.md`)**](file:///d:/chatbot/docs/PROJECT_REPORT.md): Complete project report with Abstract, Methodology, Architecture, and Testing results.
- 📊 [**Presentation Slides (`docs/PRESENTATION.md`)**](file:///d:/chatbot/docs/PRESENTATION.md): 15-slide PowerPoint deck content.
- 📷 [**Screenshot Checklist (`docs/SCREENSHOT_CHECKLIST.md`)**](file:///d:/chatbot/docs/SCREENSHOT_CHECKLIST.md): 12 recommended UI and system screenshots.

---

## 🌟 Key Features

- **ChatGPT-Style Conversational Interface**: Simple, modern conversational interface supporting text and voice queries. No mandatory category selection required.
- **Multilingual Support**: Seamlessly understands questions asked in **English**, **Native Telugu script** (`నా ఆధార్ కార్డు పోయింది. నేను ఏం చేయాలి?`), and **Telugu-English mixed phonetic spelling** (`Naa Aadhaar card poyindi. Em cheyali?`).
- **Voice Input (Microphone 🎤)**: Integrated Web Speech Recognition supporting English (`en-IN`) and Telugu (`te-IN`) with manual text editing prior to submission.
- **Hybrid Retrieval & Reranking**: Combines semantic vector similarity search with BM25 keyword density matching, heading alignment, entity extraction, and score-based reranking.
- **Relevance Threshold & Anti-Hallucination Guardrails**: Evaluates retrieval candidates against `RAG_RELEVANCE_THRESHOLD` (`0.20`). Automatically triggers safe refusal when information is missing from indexed official documents: *"I could not find sufficient information in the available official documents to answer this question."*
- **Source Verification & Accordions**: Every answer provides collapsible source cards showing verified document names, category tags, page numbers, section titles, and official source links.
- **Admin Hub & Document Management**: Dedicated Admin dashboard (`/admin`) for uploading PDF, DOCX, and TXT documents, re-indexing vector stores, and deleting documents.
- **Role-Based Access Control (RBAC)**: Protects all document management REST APIs (`POST /upload`, `GET /documents`, `DELETE`) with HMAC-SHA256 Base64 JWT Bearer token authentication requiring `role: admin`.
- **Security & Production Safeguards**: Input validation, filename sanitization, file size limits (15MB cap), rate-limiting middleware, CORS restriction, security HTTP headers (`X-Frame-Options`, `X-Content-Type-Options`), and health check `/health`.

---

## 📐 System Architecture

```text
Official Government Documents (PDF, DOCX, TXT)
                      │
                      ▼
     Text Extraction & Section Parser
                      │
                      ▼
      Chunking (TextSplitterManager)
                      │
                      ▼
    Embeddings (OpenAI / Local Fallback)
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
   Standalone Query Rewriter & Topic Switcher
                      │
                      ▼
   Hybrid Candidate Retrieval (Top 15 Chunks)
                      │
                      ▼
      Score Reranker (BM25 + Semantic + Entity Matches)
                      │
                      ▼
   Relevance Threshold Check (Threshold = 0.20)
             /                \
        Sufficient       Insufficient
           │                  │
           ▼                  ▼
   ContextBuilder    Anti-Hallucination Guardrail
 (Context Compression) ("I could not find sufficient...")
           │
           ▼
     OpenAI LLM (GPT-4o-mini)
      (Strict Grounding)
           │
           ▼
 Grounded Multilingual Answer + Verified Sources
           │
           ▼
   React Chat UI (Copy, Regenerate, Sources)
```

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
| :--- | :--- |
| **Frontend** | React 18, Vite, Tailwind CSS, Lucide Icons, Axios |
| **Backend** | Python 3.11, FastAPI, Uvicorn, Pydantic |
| **AI Orchestration** | LangChain Core, LangChain Community, PyPDF, python-docx |
| **Vector Storage** | ChromaDB (`langchain-chroma`) |
| **LLM & Embeddings** | OpenAI API (`gpt-4o-mini`, `text-embedding-3-small` / Local Fallback) |
| **Authentication & Security** | Base64 HMAC-SHA256 JWT, Rate-Limiting, Security Headers |

---

## 🌐 REST API Reference

| Method | Endpoint | Auth | Purpose |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Public | Root API status endpoint |
| `GET` | `/health` | Public | Health check endpoint verifying RAG & ChromaDB |
| `POST` | `/api/chat` | Public | Citizen chat endpoint accepting `{ question, history }` |
| `POST` | `/api/auth/login` | Public | Admin login endpoint returning JWT Bearer token |
| `GET` | `/api/auth/me` | Bearer | Validates active Admin JWT session |
| `GET` | `/api/documents` | Admin | Lists all indexed documents with metadata |
| `POST` | `/api/documents/upload` | Admin | Uploads and indexes a new PDF/DOCX/TXT file |
| `POST` | `/api/documents/reindex/{name}` | Admin | Re-indexes single document from disk storage |
| `DELETE` | `/api/documents/{name}` | Admin | Deletes document vectors from ChromaDB and disk |

---

## 🚀 Running Locally

### 1. Start FastAPI Backend

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will start at: `http://localhost:8000` (Swagger docs at `http://localhost:8000/docs`).

### 2. Start React Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will start at: `http://localhost:3000`.

---

## 🧪 Execution of Test Suite

Run the full automated unit, integration, and security test suite:

```bash
cd backend
python test_full_suite.py
```

Run the 30-question Multilingual RAG Evaluation:

```bash
python test_multilingual_rag.py
```

---

## 🐳 Docker Production Deployment

Build and spin up the complete production environment using Docker Compose:

```bash
docker-compose up --build -d
```

- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **ChromaDB**: Persisted in Docker volume `chroma_data`.
