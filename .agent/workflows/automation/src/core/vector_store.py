"""
Simple Vector Store using Ollama Embeddings
Implements a basic in-memory vector database with persistence.
"""
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional
from .llm import get_embeddings

class SimpleVectorStore:
    """
    A simple vector store for RAG (Retrieval-Augmented Generation).
    Uses Cosine Similarity for search.
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        self.embeddings = get_embeddings()
        self.storage_path = Path(storage_path) if storage_path else None
        self.data: List[Dict[str, Any]] = []
        
        if self.storage_path and self.storage_path.exists():
            self.load()

    def add_text(self, text: str, metadata: Dict[str, Any] = None):
        """Add a single text chunk to the store"""
        if not text.strip():
            return
            
        vector = self.embeddings.embed_query(text)
        self.data.append({
            "text": text,
            "metadata": metadata or {},
            "vector": vector
        })

    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]] = None):
        """Add multiple text chunks to the store"""
        vectors = self.embeddings.embed_documents(texts)
        for i, (text, vector) in enumerate(zip(texts, vectors)):
            meta = metadatas[i] if metadatas else {}
            self.data.append({
                "text": text,
                "metadata": meta,
                "vector": vector
            })

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search for similar texts using cosine similarity"""
        if not self.data:
            return []
            
        query_vector = np.array(self.embeddings.embed_query(query))
        
        results = []
        for item in self.data:
            item_vector = np.array(item["vector"])
            # Cosine similarity: (A dot B) / (||A|| * ||B||)
            sim = np.dot(query_vector, item_vector) / (np.linalg.norm(query_vector) * np.linalg.norm(item_vector))
            results.append({
                "text": item.get("text", ""),
                "metadata": item.get("metadata", {}),
                "score": float(sim)
            })
            
        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def save(self):
        """Save the vector store to disk"""
        if not self.storage_path:
            return
            
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.storage_path, 'w') as f:
            json.dump(self.data, f)
            
    def load(self):
        """Load the vector store from disk"""
        if not self.storage_path or not self.storage_path.exists():
            return
            
        with open(self.storage_path, 'r') as f:
            self.data = json.load(f)

    def clear(self):
        """Clear all data"""
        self.data = []
        if self.storage_path and self.storage_path.exists():
            self.storage_path.unlink()
