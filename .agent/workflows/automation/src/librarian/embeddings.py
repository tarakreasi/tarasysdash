# .agent/workflows/automation/src/librarian/embeddings.py
"""
Embedding Service using Sentence-Transformers (Pure Python, No Ollama Required)

Model: all-MiniLM-L6-v2
- Size: ~90MB
- Dimension: 384
- Speed: Fast on CPU
- Quality: Good for semantic search
"""
from typing import List

# Lazy loading to avoid import overhead
_model = None

def _get_model():
    """Lazy load the model on first use"""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            print("📚 Loading embedding model (first time may take a moment)...")
            _model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ Embedding model loaded successfully")
        except ImportError:
            print("❌ sentence-transformers not installed. Run: pip install sentence-transformers")
            raise
    return _model

class EmbeddingService:
    """
    Embedding service using Sentence-Transformers.
    No Ollama server required - pure Python implementation.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._dimension = 384  # all-MiniLM-L6-v2 dimension
    
    @property
    def dimension(self) -> int:
        """Return embedding dimension"""
        return self._dimension
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        try:
            model = _get_model()
            embedding = model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            print(f"❌ Embedding error: {e}")
            # Fallback: return zero vector
            return [0.0] * self._dimension
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (batch).
        More efficient than calling get_embedding() multiple times.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            model = _get_model()
            embeddings = model.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()
        except Exception as e:
            print(f"❌ Batch embedding error: {e}")
            return [[0.0] * self._dimension for _ in texts]