# .agent/workflows/automation/dev_agent_cli.py
import argparse
import os
import sys

# Get the directory where the script is located (automation dir)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add src relative to script location
sys.path.append(os.path.join(script_dir, "src"))

from librarian.service import Librarian
from developer.tools import DeveloperTools
from developer.brain import AgentBrain
from developer.executor import AgentExecutor

def main():
    parser = argparse.ArgumentParser(description="Auto-Developer Agent CLI")
    parser.add_argument("objective", type=str, help="The task to perform")
    parser.add_argument("--model", type=str, default="qwen2.5-coder:7b", help="Ollama model to use")
    
    args = parser.parse_args()
    
    # We want the agent to work on the current working directory where the user calls it from
    # But if we are testing from within automation dir, it will be that.
    cwd = os.getcwd()
    print(f"🤖 Auto-Developer initialized in: {cwd}")
    
    # 1. Init Librarian (Knowledge)
    # Note: If running on a large repo, this might be slow if we index everything.
    # For now, we trust the defaults.
    librarian = Librarian(workspace_root=cwd)
    
    # 2. Init Tools (Hands)
    tools = DeveloperTools(librarian)
    
    # 3. Init Brain (Mind)
    brain = AgentBrain(model_name=args.model)
    
    # 4. Init Executor (Body)
    executor = AgentExecutor(brain, tools)
    
    # 5. Run
    result = executor.run_task(args.objective)
    print(f"\n✅ Result: {result}")

if __name__ == "__main__":
    main()