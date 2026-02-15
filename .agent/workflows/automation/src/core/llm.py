"""LLM Configuration Module"""
from langchain_ollama import ChatOllama, OllamaEmbeddings
from .config import OLLAMA_BASE_URL, MODEL_FAST, MODEL_SMART, MODEL_EMBEDDING

def get_llm(model: str = None, temperature: float = 0.7):
    """Get configured ChatOllama instance"""
    model = model or MODEL_FAST
    return ChatOllama(
        base_url=OLLAMA_BASE_URL,
        model=model,
        temperature=temperature
    )

def get_embeddings():
    """Get configured Ollama embeddings"""
    return OllamaEmbeddings(
        base_url=OLLAMA_BASE_URL,
        model=MODEL_EMBEDDING
    )
