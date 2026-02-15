    # .agent/workflows/automation/verify_brain.py
    import sys
    import os
    
    # Add src
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(current_dir, "src")
    sys.path.append(src_path)
    
    from developer.brain import AgentBrain
    
    # Mock LLM for determinism in verification
    class MockLLM:
        def invoke(self, messages):
            class Response:
                content = '{"thought": "I need to search", "action": "search_codebase", "args": {"query": "hello"}}'
            return Response()
            
    try:
        brain = AgentBrain()
        brain.llm = MockLLM() # Swap with mock
        
        decision = brain.decide_action("Fix the bug", [])
        
        print("Decision:", decision)
        
        assert decision["action"] == "search_codebase"
        assert decision["args"]["query"] == "hello"
        
        print("✅ Brain verification passed.")

    except Exception as e:
        print(f"❌ Verification failed: {e}")
        exit(1)
    