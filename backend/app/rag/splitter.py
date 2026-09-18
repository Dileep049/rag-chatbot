from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import CHUNK_SIZE, CHUNK_OVERLAP

class TextSplitterManager:
    """Splits loaded document pages into overlapping text chunks while preserving metadata."""
    
    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        print("Extracting text and creating chunks...")
        chunks = self.splitter.split_documents(documents)
        print(f"Created {len(chunks)} chunks.")
        return chunks

# Alias for backward compatibility
TextSplitter = TextSplitterManager
