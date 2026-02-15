# .agent/workflows/automation/verify_librarian_full.py
import sys
import os

# Add src - Use relative path from this script location to be robust
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "src")
sys.path.append(src_path)

from librarian.service import Librarian

try:
    
    # Create a temp dir for workspace root in /tmp to avoid blacklist issues with .agent
    import tempfile
    temp_dir = tempfile.mkdtemp(prefix="librarian_test_")
    
    test_db = os.path.join(current_dir, "memory", "test_full.db")
    if os.path.exists(test_db):
        os.remove(test_db)
        
    # 1. Init
    lib = Librarian(workspace_root=temp_dir, db_path=test_db)
    
    # 2. Create a unique file to find in the CWD
    secret_file = os.path.join(temp_dir, "secret_knowledge.txt")
    with open(secret_file, "w") as f:
        f.write(" The verification password is: 'BLUE_ORANGE_123'. ")
        
    # 3. Index
    lib.index()
    
    # 4. Query
    context = lib.query("What is the verification password?")
    
    print("--- Retrieval Result ---")
    print(context)
    
    # 5. Assert
    assert "BLUE_ORANGE_123" in context
    assert "secret_knowledge.txt" in context
    
    print("✅ End-to-End Librarian verification passed.")

except Exception as e:
    print(f"❌ Verification failed: {e}")
    # Print traceback for debugging
    import traceback
    traceback.print_exc()
    exit(1)
finally:
    # Cleanup
    if 'temp_dir' in locals() and os.path.exists(temp_dir):
        import shutil
        shutil.rmtree(temp_dir)
    if os.path.exists(test_db):
        os.remove(test_db)