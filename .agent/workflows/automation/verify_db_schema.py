    # .agent/workflows/automation/verify_db_schema.py
    import sys
    import os
    
    # Add src to path
    sys.path.append(os.path.join(os.getcwd(), ".agent/workflows/automation/src"))
    
    from librarian.db_manager import DatabaseManager

    db_path = ".agent/workflows/automation/memory/test_librarian.db"
    
    # Clean up previous test
    if os.path.exists(db_path):
        os.remove(db_path)

    try:
        mgr = DatabaseManager(db_path)
        tables = mgr.db.table_names()
        print(f"Tables found: {tables}")
        
        assert "files" in tables
        assert "chunks" in tables
        
        # Verify vector extension availability
        vec_version = mgr.db.execute("select vec_version()").fetchone()[0]
        print(f"✅ sqlite-vec version: {vec_version}")
        
        print("✅ Schema verification successful.")
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        exit(1)
    finally:
        # Cleanup
        if os.path.exists(db_path):
            os.remove(db_path)
    