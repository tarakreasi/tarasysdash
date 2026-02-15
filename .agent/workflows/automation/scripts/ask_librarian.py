# .agent/workflows/automation/scripts/ask_librarian.py
import sys
import os
import argparse

# Get automation dir relative to this script
script_dir = os.path.dirname(os.path.abspath(__file__))
automation_dir = os.path.dirname(script_dir) # .agent/workflows/automation
src_path = os.path.join(automation_dir, "src")
sys.path.append(src_path)

from librarian.service import Librarian
from core.memory_manager import MemoryManager

def main():
    parser = argparse.ArgumentParser(description="Ask the Librarian a question about the codebase.")
    parser.add_argument("query", type=str, help="The natural language query.")
    parser.add_argument("--top_k", type=int, default=5, help="Number of chunks to retrieve.")
    
    # Active Memory Flags
    parser.add_argument("--update-context", action="store_true", help="Update .agent/memory/active_context.md with result")
    parser.add_argument("--focus", type=str, default="General Query", help="Focus/Task name for context update")
    parser.add_argument("--sprint", type=str, default="N/A", help="Current Sprint ID")
    
    args = parser.parse_args()
    
    # Project root calculation (same as indexer)
    workspace_root = os.path.abspath(os.path.join(automation_dir, "../../.."))
    db_path = os.path.join(automation_dir, "memory", "librarian.db")
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}. Please run `scripts/index_codebase.py` first.")
        sys.exit(1)
        
    librarian = Librarian(workspace_root=workspace_root, db_path=db_path)
    
    print(f"🔍 Searching for: '{args.query}'...")
    try:
        context = librarian.query(args.query, top_k=args.top_k)
        print("\n--- 📖 LIBRARIAN ANSWER (Context) ---\n")
        print(context)
        print("\n-------------------------------------")
        
        # ACTIVE MEMORY UPDATE
        if args.update_context:
            print(f"\n🧠 Updating Active Memory for focus: {args.focus}...")
            mem = MemoryManager()
            
            # Split context lines for bullet points
            insights = [line for line in context.split('\n') if line.strip()]
            
            # Update file
            mem.update_active_context(
                focus=args.focus,
                sprint_id=args.sprint,
                insights=insights[:10] # Top 10 insights only
            )
            
    except Exception as e:
        print(f"❌ Error during query: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
