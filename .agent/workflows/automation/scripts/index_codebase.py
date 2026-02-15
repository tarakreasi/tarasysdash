# .agent/workflows/automation/scripts/index_codebase.py
import sys
import os
import argparse

# Get automation dir relative to this script
script_dir = os.path.dirname(os.path.abspath(__file__))
automation_dir = os.path.dirname(script_dir) # .agent/workflows/automation
src_path = os.path.join(automation_dir, "src")
sys.path.append(src_path)

from librarian.service import Librarian

def main():
    parser = argparse.ArgumentParser(description="Index the code base into the Librarian DB.")
    parser.add_argument("--root", type=str, default=None, help="Root directory to index. Defaults to Project Root.")
    parser.add_argument("--clean", action="store_true", help="Clean DB before indexing.")
    
    args = parser.parse_args()
    
    # Determine workspace root
    # If script is in copy_of_agent/new_agent2/.agent/workflows/automation/scripts/
    # Project root is ../../../../
    if args.root:
        workspace_root = os.path.abspath(args.root)
    else:
        # Go up 4 levels from scripts dir: automation -> workflows -> .agent -> new_agent2
        workspace_root = os.path.abspath(os.path.join(automation_dir, "../../.."))
    
    print(f"📚 Librarian Indexer initialized for: {workspace_root}")
    
    # DB Path
    db_path = os.path.join(automation_dir, "memory", "librarian.db")
    print(f"💾 Database: {db_path}")
    
    if args.clean and os.path.exists(db_path):
        print("🧹 Cleaning existing database...")
        os.remove(db_path)
    
    librarian = Librarian(workspace_root=workspace_root, db_path=db_path)
    
    print("⏳ Starting Indexing... (This may take a moment)")
    librarian.index()
    print("✅ Indexing Complete.")

if __name__ == "__main__":
    main()
