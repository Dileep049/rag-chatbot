import os
import shutil
import datetime
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, status
from app.config import DATA_DIR, CATEGORIES, MAX_UPLOAD_SIZE_MB
from app.rag.loader import DocumentLoader
from app.rag.splitter import TextSplitter
from app.rag.vectorstore import VectorStoreManager
from app.auth.dependencies import require_admin

router = APIRouter(prefix="/api/documents", tags=["Documents"])
vectorstore = VectorStoreManager()
splitter = TextSplitter()

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

def index_file(file_path: str, category: str) -> int:
    """Helper to parse, chunk, embed and store a single document into ChromaDB."""
    pages = DocumentLoader.load_document(file_path, category=category)
    if not pages:
        return 0
    chunks = splitter.split_documents(pages)
    return vectorstore.add_chunks(chunks)

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form("other"),
    overwrite: bool = Form(False),
    admin_user: dict = Depends(require_admin)
):
    """Upload a new document, validate, save, and index into ChromaDB. Protected by require_admin."""
    raw_filename = file.filename
    if not raw_filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a valid filename.")

    # Sanitize filename against path traversal
    filename = Path(raw_filename).name
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename format.")

    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Please upload PDF, DOCX or TXT files."
        )

    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Cannot upload an empty file.")

    max_bytes = MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(contents) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed limit of {MAX_UPLOAD_SIZE_MB}MB."
        )

    cat_dir = Path(DATA_DIR) / category.lower()
    os.makedirs(cat_dir, exist_ok=True)
    target_path = cat_dir / filename

    # Duplicate check across all categories
    existing_file_found = False
    existing_cat_dir = None
    for root, dirs, files in os.walk(DATA_DIR):
        if filename in files:
            existing_file_found = True
            existing_cat_dir = root
            break

    if existing_file_found and not overwrite:
        raise HTTPException(
            status_code=409,
            detail=f"This document '{filename}' already exists in the knowledge base."
        )

    if existing_file_found and overwrite:
        vectorstore.delete_document(filename)
        if existing_cat_dir and os.path.exists(os.path.join(existing_cat_dir, filename)):
            try:
                os.remove(os.path.join(existing_cat_dir, filename))
            except Exception:
                pass

    try:
        with open(target_path, "wb") as buffer:
            buffer.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file to disk: {str(e)}")

    try:
        chunk_count = index_file(str(target_path), category=category.lower())
        return {
            "message": f"Document '{filename}' uploaded and indexed successfully.",
            "document": filename,
            "category": category.lower(),
            "type": ext.replace(".", ""),
            "chunks_indexed": chunk_count,
            "status": "Indexed"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to index document into vector database: {str(e)}")

@router.get("")
async def list_documents(admin_user: dict = Depends(require_admin)):
    """List all indexed documents. Protected by require_admin."""
    docs = vectorstore.get_indexed_documents()
    
    enriched_docs = []
    for d in docs:
        filename = d.get("name")
        ext = Path(filename).suffix.replace(".", "").lower() if filename else "pdf"
        file_path = None
        for root, dirs, files in os.walk(DATA_DIR):
            if filename in files:
                file_path = os.path.join(root, filename)
                break
                
        uploaded_at = "Existing"
        if file_path and os.path.exists(file_path):
            mtime = os.path.getmtime(file_path)
            uploaded_at = datetime.datetime.fromtimestamp(mtime).strftime("%d %b %Y")

        enriched_docs.append({
            "name": filename,
            "category": d.get("category", "General"),
            "type": ext,
            "chunks": d.get("chunks", 0),
            "pages": d.get("pages", 1),
            "status": "Indexed",
            "uploaded_at": uploaded_at
        })
        
    return {
        "documents": enriched_docs,
        "total": len(enriched_docs)
    }

@router.post("/reindex/{document_name}")
async def reindex_single_document(
    document_name: str,
    admin_user: dict = Depends(require_admin)
):
    """Re-index a specific document from disk storage into ChromaDB. Protected by require_admin."""
    # Sanitize document_name against path traversal
    document_name = Path(document_name).name
    target_path = None
    target_category = "general"
    
    for root, dirs, files in os.walk(DATA_DIR):
        if document_name in files:
            target_path = os.path.join(root, document_name)
            target_category = os.path.basename(root)
            break

    if not target_path or not os.path.exists(target_path):
        raise HTTPException(
            status_code=404, 
            detail=f"Original document file '{document_name}' not found on disk."
        )

    try:
        vectorstore.delete_document(document_name)
        chunk_count = index_file(target_path, category=target_category)
        return {
            "message": f"Document '{document_name}' successfully re-indexed.",
            "document": document_name,
            "category": target_category,
            "chunks_indexed": chunk_count,
            "status": "Indexed"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error re-indexing document '{document_name}': {str(e)}"
        )

@router.delete("/{document_name}")
async def delete_document(
    document_name: str,
    admin_user: dict = Depends(require_admin)
):
    """Delete a document from ChromaDB index and physical disk storage. Protected by require_admin."""
    document_name = Path(document_name).name
    success = vectorstore.delete_document(document_name)
    
    file_deleted = False
    for root, dirs, files in os.walk(DATA_DIR):
        if document_name in files:
            try:
                os.remove(os.path.join(root, document_name))
                file_deleted = True
            except Exception:
                pass

    if success or file_deleted:
        return {"message": f"Document '{document_name}' deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail=f"Document '{document_name}' not found.")

@router.post("/reindex-all")
async def reindex_all(admin_user: dict = Depends(require_admin)):
    """Re-scan all documents in data/ directory and populate ChromaDB. Protected by require_admin."""
    vectorstore.clear_all()
    total_files = 0
    total_chunks = 0
    
    data_path = Path(DATA_DIR)
    if not data_path.exists():
        os.makedirs(data_path, exist_ok=True)
        
    for cat_dir in data_path.iterdir():
        if cat_dir.is_dir():
            cat_name = cat_dir.name
            for file_path in cat_dir.glob("*.*"):
                if file_path.suffix.lower() in ALLOWED_EXTENSIONS:
                    c_count = index_file(str(file_path), category=cat_name)
                    total_chunks += c_count
                    total_files += 1
                    
    return {
        "message": f"Re-indexed {total_files} documents with {total_chunks} total chunks.",
        "documents_indexed": total_files,
        "chunks_indexed": total_chunks
    }
