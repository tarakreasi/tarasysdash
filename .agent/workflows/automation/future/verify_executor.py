    # .agent/workflows/automation/verify_executor.py
    import sys
    import os
    
    # Add src
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(current_dir, "src")
    sys.path.append(src_path)
    
    from developer.executor import AgentExecutor
    
    # Mocks
    class MockBrain:
        def __init__(self):
            self.steps = 0
        def decide_action(self, obj, hist):
            self.steps += 1
            if self.steps == 1:
                return {"thought": "write", "action": "write_file", "args": {"file_path": "test.txt", "content": "hi"}}
            else:
                return {"thought": "done", "action": "finish", "args": {"response": "Done"}}
                
    class MockTools:
        def write_file(self, file_path, content):
            return "Success"
        def search_codebase(self, query): pass
        def read_file(self, file_path): pass
        def list_dir(self, directory): pass

    try:
        brain = MockBrain()
        tools = MockTools()
        executor = AgentExecutor(brain, tools)
        
        res = executor.run_task("Do test")
        
        print(f"Result: {res}")
        assert res == "Done"
        assert len(executor.history) == 1 # Only the write action is in history, finish returns immediately
        
        print("✅ Executor verification passed.")

    except Exception as e:
        print(f"❌ Verification failed: {e}")
        exit(1)
    