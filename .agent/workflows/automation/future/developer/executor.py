# .agent/workflows/automation/src/developer/executor.py
import time

class AgentExecutor:
    def __init__(self, brain, tools):
        self.brain = brain
        self.tools = tools
        self.history = []

    def run_task(self, objective: str, max_steps: int = 10):
        print(f"🚀 Starting Task: {objective}")
        
        for step in range(max_steps):
            print(f"--- Step {step+1} ---")
            
            # 1. Decide
            decision = self.brain.decide_action(objective, self.history)
            print(f"🧠 Thought: {decision.get('thought')}")
            print(f"⚡ Action: {decision.get('action')}")
            
            action = decision.get("action")
            args = decision.get("args", {})
            
            # 2. Execute
            result = ""
            if action == "finish":
                return args.get("response", "Task Completed")
            
            elif action == "search_codebase":
                result = self.tools.search_codebase(**args)
            elif action == "read_file":
                result = self.tools.read_file(**args)
            elif action == "write_file":
                result = self.tools.write_file(**args)
            elif action == "list_dir":
                result = self.tools.list_dir(**args)
            else:
                result = f"Error: Unknown tool '{action}'"
            
            print(f"📝 Result: {result[:100]}...") # Truncate log
            
            # 3. Update History
            self.history.append({
                "action": action,
                "args": args,
                "result": result
            })
            
        return "Max steps reached without completion."