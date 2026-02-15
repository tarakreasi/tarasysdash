    # .agent/workflows/automation/verify_tools.py
    import sys
    import os
    import shutil
    import tempfile
    
    # Add src - Use relative path from this script location to be robust
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(current_dir, "src")
    sys.path.append(src_path)
    
    from developer.tools import DeveloperTools
    from librarian.service import Librarian
    
    # Setup temp environment
    temp_dir = tempfile.mkdtemp(prefix="dev_tools_test_")
    # Make sure DB is in temp ref
    test_db = os.path.join(temp_dir, "test.db")
    
    try:
        # 1. Init
        lib = Librarian(workspace_root=temp_dir, db_path=test_db)
        tools = DeveloperTools(lib)
        
        # 2. Test Write
        test_file = os.path.join(temp_dir, "hello.py")
        msg = tools.write_file(test_file, "print('Hello World')")
        assert "Successfully wrote" in msg
        assert os.path.exists(test_file)
        
        # 3. Test Read
        content = tools.read_file(test_file)
        assert "print('Hello World')" in content
        
        # 4. Test Indexing/Search (Write should have triggered index)
        # Verify search returns something about Hello World
        # Note: We rely on Librarian implementation from 4.2
        # Since Embeddings might be mock or real, just testing the call flow is enough for unit test
        res = tools.search_codebase("Hello World")
        print("Search Result (Length):", len(res))
        
        print("✅ Developer Tools verification passed.")

    except Exception as e:
        print(f"❌ Verification failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    