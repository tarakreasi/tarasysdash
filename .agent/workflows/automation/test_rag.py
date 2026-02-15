"""
Test script for Semantic RAG (nomic-embed-text) integration
"""
import sys
from pathlib import Path

# Add current dir to path
sys.path.append(str(Path(__file__).parent))

from src.core.knowledge_base import KnowledgeBase
from src.core.config import PROJECT_ROOT

def test_rag():
    print("🚀 Initializing KnowledgeBase...")
    kb = KnowledgeBase()
    
    print("📦 Indexing standards (force indexing for test)...")
    kb.index_standards(force=True)
    
    print("\n🔍 Testing Semantic Search...")
    queries = [
        "How to write Vue components?",
        "REST API best practices",
        "CSS and styling standards"
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        result = kb.query_standards(query, top_k=1)
        if result:
            print(f"Result found (first 100 chars):\n{result[:300]}...")
        else:
            print("❌ No results found.")

if __name__ == "__main__":
    test_rag()
