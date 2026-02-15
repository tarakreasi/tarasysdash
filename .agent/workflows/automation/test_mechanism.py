
import sys
import os
from pathlib import Path
import time
import pprint

# Add current dir to path so we can import src
sys.path.append(str(Path(__file__).parent))

from src.agents.graph import graph
from src.core.config import PROJECT_ROOT

def test_agent_streaming():
    print("🚀 STARTING LOCAL AGENT TEST (STREAMING MODE)")
    print(f"📂 Project Root: {PROJECT_ROOT}")
    
    task = "Create a python script 'agent_test.py' that prints 'HELLO LOCAL ASSISTANT'. Then run it to verify it works."
    print(f"\n📋 Task: {task}")
    print("-" * 50)
    
    initial_state = {
        "task": task, 
        "context": "Context: Testing environment", 
        "project_root": str(PROJECT_ROOT),
        "messages": [],
        "review_status": "pending"
    }
    
    start_time = time.time()
    
    try:
        # Use stream() to get output as it happens
        for step_output in graph.stream(initial_state):
            print("\n🔄 NODE UPDATE:")
            for node_name, state_update in step_output.items():
                print(f"👉 Node: {node_name}")
                
                # Print Strategy if from Architect
                if "strategy" in state_update:
                    print(f"\n📝 Strategy Generated:\n{state_update['strategy'][:300]}...")
                
                # Print Messages if from Coder/Verifier
                if "messages" in state_update:
                    last_msg = state_update['messages'][-1]
                    content = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)
                    preview = content if len(content) < 500 else content[:500] + "..."
                    print(f"\n💬 Message:\n{preview}")
                
                # Print Review Status
                if "review_status" in state_update:
                    print(f"\n✅ Review Status: {state_update['review_status']}")
            
            print("-" * 30)
            
        print(f"\n✅ EXECUTION FINISHED in {time.time() - start_time:.2f}s")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_agent_streaming()
