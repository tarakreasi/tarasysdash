    # .agent/workflows/automation/verify_context.py
    import sys
    import os
    
    # Add src
    sys.path.append(os.path.join(os.getcwd(), ".agent/workflows/automation/src"))
    
    from librarian.context import ContextBuilder
    
    try:
        builder = ContextBuilder()
        
        # Mock results
        results = [
            {"path": "src/main.py", "content": "print('hello')"},
            {"path": "src/utils.py", "content": "def add(a,b): return a+b"},
            {"path": "huge.py", "content": "x" * 10000} # Should be truncated/skipped if limit small
        ]
        
        # Test 1: Normal
        ctx = builder.format_context(results, max_tokens=1000)
        print("--- Context Output ---")
        print(ctx)
        
        assert '<file path="src/main.py">' in ctx
        assert "print('hello')" in ctx
        
        # Test 2: Limit
        ctx_limit = builder.format_context(results, max_tokens=50) # Very small
        # Header consumes some, hopefully skips huge file
        assert "huge.py" not in ctx_limit
        
        print("✅ Context verification passed.")

    except Exception as e:
        print(f"❌ Verification failed: {e}")
        exit(1)
    