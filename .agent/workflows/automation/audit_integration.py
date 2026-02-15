"""
Audit Script for RAG Intelligence & Sparring History
1. Tests "Sparring History" retrieval (UI Patterns, Lessons Learned).
2. Audits current Supervisor execution (Logs, Thoughts).
3. Verifies Integration status.
"""
import sys
from pathlib import Path
import re

# Add path for imports
sys.path.append(str(Path(__file__).parent))

from src.core.knowledge_base import KnowledgeBase
from src.core.config import PROJECT_ROOT

def audit_rag_intelligence():
    print(f"\n🧠 AUDIT: RAG INTELLIGENCE CHECK")
    print("=" * 50)
    
    kb = KnowledgeBase()
    
    # Test Queries designed to hit Sparring History
    test_queries = [
        "What are the UI design patterns for server metrics?",
        "How do we handle VRAM optimization for Ollama?",
        "What is the recommended color for CPU metrics?",
    ]
    
    for q in test_queries:
        print(f"\n🔎 Query: '{q}'")
        results = kb.query_standards(q, top_k=1)
        
        if results:
            # Extract source to verify it comes from history
            match = re.search(r"--- FROM (.*?) ---", results)
            source = match.group(1) if match else "Unknown"
            snippet = results.split('---')[-1][:200].strip().replace('\n', ' ')
            
            print(f"   ✅ Found in: {source}")
            print(f"   📄 Snippet: \"{snippet}...\"")
            
            if ".gemini" in source or "knowledge" in source:
                print("   🌟 SUCCESS: Retrieved from Sparring History!")
            else:
                print("   ⚠️  Retrieved from Standards (Fallback)")
        else:
            print("   ❌ FAILED: No context found.")

def audit_supervisor_thought():
    print(f"\n🤖 AUDIT: SUPERVISOR THOUGHT PROCESS")
    print("=" * 50)
    
    log_file = PROJECT_ROOT / ".agent" / "automation" / "supervisor.log"
    if not log_file.exists():
        print("❌ Supervisor log not found.")
        return

    content = log_file.read_text()
    
    # Find latest "STRATEGIC THOUGHT"
    thoughts = re.findall(r"💭 STRATEGIC THOUGHT:\n(.*?)(?=\n\[)", content, re.DOTALL)
    
    if thoughts:
        latest = thoughts[-1].strip()
        print(f"💡 Latest Strategic Thought:\n{'-'*30}\n{latest}\n{'-'*30}")
        
        # Grading the thought
        score = 0
        if "risk" in latest.lower(): score += 1
        if "alternative" in latest.lower(): score += 1
        if "security" in latest.lower(): score += 1
        
        print(f"\n📊 Intelligence Score: {score}/3")
        if score == 3: print("   🌟 EXCELLENT: Critical thinking detected.")
        elif score > 0: print("   ✅ GOOD: Basic reasoning detected.")
        else: print("   ⚠️  WEAK: No strategic depth found.")
    else:
        print("⚠️  No strategic thoughts recorded yet.")

if __name__ == "__main__":
    audit_rag_intelligence()
    audit_supervisor_thought()
