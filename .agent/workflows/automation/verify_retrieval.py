    # .agent/workflows/automation/verify_retrieval.py
    import sys
    import os
    import json
    import sqlite_vec
    
    # Add src
    sys.path.append(os.path.join(os.getcwd(), ".agent/workflows/automation/src"))
    
    from librarian.db_manager import DatabaseManager
    # Mock embedder or real one
    from librarian.retriever import LibrarianRetriever
    
    db_path = ".agent/workflows/automation/memory/test_librarian_retrieval.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        
    try:
        # Setup
        mgr = DatabaseManager(db_path)
        
        # 1. Seed DB with known data
        # We need a dummy file
        files = mgr.db["files"]
        files.insert({"id": 1, "path": "test_search.py", "hash": "abc", "last_modified": 0.0})
        
        # Mock Embedder
        class MockEmbedder:
            def get_embedding(self, text):
                # Return distinctive vectors
                if "apple" in text: return [1.0, 0.0, 0.0, 0.0]
                if "banana" in text: return [0.0, 1.0, 0.0, 0.0]
                return [0.5, 0.5, 0.0, 0.0]
        
        embedder = MockEmbedder()
        
        chunks = mgr.db["chunks"]
        chunks.insert({
            "file_id": 1,
            "chunk_index": 0,
            "content": "This is a function about apples.",
            "embedding": [1.0, 0.0, 0.0, 0.0], # Matches apple
            "metadata": "{}"
        })
        chunks.insert({
            "file_id": 1,
            "chunk_index": 1,
            "content": "This is a function about bananas.",
            "embedding": [0.0, 1.0, 0.0, 0.0], # Matches banana
            "metadata": "{}"
        })
        
        # 2. Test Retriever
        retriever = LibrarianRetriever(mgr, embedder)
        
        # Query for apple
        print("Querying for 'apple'...")
        results = retriever.query("apple function", top_k=1)
        print(f"Results: {results}")
        
        assert len(results) >= 1
        assert "apple" in results[0]["content"]
        
        print("✅ Retrieval verification passed.")

    except Exception as e:
        print(f"❌ Verification failed: {e}")
        exit(1)
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
    