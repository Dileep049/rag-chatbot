# Ollama Local LLM & Local Embeddings Setup Guide

This guide explains how to run the **Citizen Assistance RAG Chatbot** completely locally with **₹0 API cost** using **Ollama** for LLM answer generation and **sentence-transformers** for local vector embeddings.

---

## Step 1: Install Ollama

Download and install Ollama for your operating system:
* **Windows / macOS / Linux**: [https://ollama.com/download](https://ollama.com/download)

---

## Step 2: Verify Ollama Installation

Open a terminal or PowerShell prompt and run:

```bash
ollama --version
```

Expected output:
```text
ollama version is 0.x.x
```

---

## Step 3: Download (Pull) Configured Local LLM Model

Pull the lightweight instruct model configured in `.env` (`OLLAMA_MODEL=llama3.2:1b`):

```bash
ollama pull llama3.2:1b
```

> **Note**: For systems with limited RAM, `llama3.2:1b` or `qwen2.5:1.5b` are lightweight (1-2 GB) and run fast on CPU. If you have 8GB+ RAM, you can also use `llama3.2` or `phi3:mini`.

---

## Step 4: Verify Downloaded Models

Check that the model appears in your local list:

```bash
ollama list
```

Expected output:
```text
NAME            ID              SIZE      MODIFIED
llama3.2:1b     baf6a787fd96    1.3 GB    ...
```

---

## Step 5: Start Ollama Server (If Required)

On Windows and macOS, the Ollama desktop app runs automatically in the system tray. If running on Linux or command line:

```bash
ollama serve
```

Verify status by opening `http://localhost:11434` in your browser. It should show:
```text
Ollama is running
```

---

## Step 6: Re-index Knowledge Base with Local Embeddings

Run `ingest.py` to index the official documents in `backend/data/` into ChromaDB using local sentence-transformers embeddings (`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`):

```bash
cd backend
python ingest.py
```

> **First Run Note**: The first run will automatically download the lightweight embedding model (`~470 MB`) from HuggingFace. Subsequent runs will use the cached local model offline.

---

## Step 7: Start FastAPI Backend

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Verify backend health at: [http://localhost:8000/health](http://localhost:8000/health)

Expected JSON response:
```json
{
  "status": "ok",
  "service": "Citizen Assistance RAG API",
  "rag": "operational",
  "chroma": "connected",
  "llm_provider": "ollama",
  "embedding_provider": "local"
}
```

---

## Step 8: Start React Frontend

```bash
cd frontend
npm run dev
```

Open your browser at `http://localhost:5173`.

---

## Summary of Environment Variables

In `backend/.env`:

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b

EMBEDDING_PROVIDER=local
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

CHROMA_PERSIST_DIR=./chroma_db
DATA_DIR=./data
```

---

## ₹0 API Cost Guarantee

* **No OpenAI API Key Required**
* **No OpenAI Credit Charges**
* **100% Privacy & Local Inference**
