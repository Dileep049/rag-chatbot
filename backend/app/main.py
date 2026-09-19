import time
from collections import defaultdict
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import (
    CORS_ORIGINS, 
    RATE_LIMIT_ENABLED, 
    CHAT_RATE_LIMIT, 
    UPLOAD_RATE_LIMIT, 
    RAG_DEBUG,
    LLM_PROVIDER,
    EMBEDDING_PROVIDER
)
from app.routes.chat import router as chat_router
from app.routes.documents import router as documents_router
from app.routes.auth import router as auth_router

app = FastAPI(
    title="Citizen Assistance RAG API",
    description="Production-Ready Official Backend API for Citizen Assistance AI Chatbot",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS if CORS_ORIGINS else ["*"],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting Storage: ip -> [timestamps]
rate_limit_records = defaultdict(list)

@app.middleware("http")
async def security_and_rate_limit_middleware(request: Request, call_next):
    """Enforces Security HTTP Headers and Configurable Rate Limiting."""
    if request.method == "OPTIONS":
        return await call_next(request)

    client_ip = request.client.host if request.client else "127.0.0.1"
    now = time.time()

    # Rate limiting pre-check
    if RATE_LIMIT_ENABLED:
        path = request.url.path
        limit = CHAT_RATE_LIMIT if "/chat" in path else (UPLOAD_RATE_LIMIT if "/upload" in path else 120)
        
        # Clean timestamps older than 60s
        timestamps = [ts for ts in rate_limit_records[client_ip] if now - ts < 60]
        rate_limit_records[client_ip] = timestamps

        if len(timestamps) >= limit:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Rate limit exceeded. Please wait a moment before sending more requests."}
            )

        rate_limit_records[client_ip].append(now)

    # Process Request
    response = await call_next(request)

    # Security Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response

# Routes
app.include_router(chat_router)
app.include_router(documents_router)
app.include_router(auth_router)

from app.config import (
    CORS_ORIGINS, 
    RATE_LIMIT_ENABLED, 
    CHAT_RATE_LIMIT, 
    UPLOAD_RATE_LIMIT, 
    RAG_DEBUG,
    LLM_PROVIDER,
    EMBEDDING_PROVIDER,
    DEMO_MODE,
    CHROMA_COLLECTION_NAME
)

@app.get("/")
async def root():
    """Root status endpoint."""
    return {
        "status": "ok",
        "service": "Citizen Assistance RAG API",
        "version": "1.0.0",
        "demo_mode": DEMO_MODE
    }

@app.get("/health")
async def health_check():
    """Health check endpoint verifying API and ChromaDB operational status."""
    return {
        "status": "ok",
        "service": "Citizen Assistance RAG API",
        "rag": "operational",
        "chroma": "connected",
        "demo_mode": DEMO_MODE,
        "collection": CHROMA_COLLECTION_NAME,
        "llm_provider": LLM_PROVIDER,
        "embedding_provider": EMBEDDING_PROVIDER
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=["app"])
