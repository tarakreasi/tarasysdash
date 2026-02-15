    # .agent/workflows/automation/verify_indexer.py
    import sys
    import os
    
    # Add src to path
    sys.path.append(os.path.join(os.getcwd(), ".agent/workflows/automation/src"))
    
    from librarian.db_manager import DatabaseManager
    from librarian.embeddings import EmbeddingService
    from librarian.indexer import LibrarianIndexer
    
    db_path = ".agent/workflows/automation/memory/test_librarian_index.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        
    try:
        mgr = DatabaseManager(db_path)
        
        # Mock class for verification speed
        class MockEmbedder:
            def get_embedding(self, text):
                return [0.1] * 768
                
        embedder = MockEmbedder()
        indexer = LibrarianIndexer(mgr, embedder)
        
        # Create dummy file
        with open("test_doc_verify.md", "w") as f:
            f.write("Hello world. This is a test document for indexing.")
            
        # Index
        indexer.index_file("test_doc_verify.md")
        
        # Verify
        files_count = mgr.db["files"].count
        chunks_count = mgr.db["chunks"].count
        print(f"Files: {files_count}, Chunks: {chunks_count}")
        
        assert files_count == 1
        assert chunks_count > 0
        
        print("✅ Indexing flow verified.")

    except Exception as e:
        print(f"❌ Verification failed: {e}")
        exit(1)
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
        if os.path.exists("test_doc_verify.md"):
            os.remove("test_doc_verify.md")
    