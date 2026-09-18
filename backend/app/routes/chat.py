from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.services.chatbot import ChatbotService
from app.config import CATEGORIES, CATEGORY_LABELS

router = APIRouter(prefix="/api", tags=["Chat"])
chatbot_service = ChatbotService()

class HistoryItem(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    question: str
    category: Optional[str] = None
    history: Optional[List[HistoryItem]] = None

class SourceItem(BaseModel):
    document: str
    page: Any
    category: Optional[str] = None
    section: Optional[str] = None
    excerpt: Optional[str] = None
    source_type: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceItem]

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat API endpoint taking user question and optional history, returning grounded RAG answer + sources."""
    if not request.question or not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty. Please provide a valid question."
        )

    try:
        history_dicts = [{"role": h.role, "content": h.content} for h in request.history] if request.history else []
        
        result = chatbot_service.ask(
            question=request.question.strip(),
            category=request.category,
            history=history_dicts
        )
        
        return ChatResponse(
            answer=result["answer"],
            sources=[SourceItem(**src) for src in result.get("sources", [])]
        )
    except Exception as e:
        print(f"Error processing chat request: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your request: {str(e)}"
        )

@router.get("/categories")
async def get_categories():
    return {
        "categories": [{"id": cat, "name": CATEGORY_LABELS.get(cat, cat.capitalize())} for cat in CATEGORIES]
    }
