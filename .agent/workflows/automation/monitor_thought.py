import re
from pathlib import Path

SUPERVISOR_LOG = Path(".agent/automation/supervisor.log")

def extract_latest_thought():
    if not SUPERVISOR_LOG.exists():
        print("Log file not found.")
        return

    content = SUPERVISOR_LOG.read_text()
    
    # regex to find thought blocks
    thoughts = re.findall(r"💭 STRATEGIC THOUGHT:\n(.*?)(?=\n\[)", content, re.DOTALL)
    
    if thoughts:
        print("\n🧠 LATEST AI THOUGHT PROCESS:\n" + "="*40)
        print(thoughts[-1].strip())
        print("="*40 + "\n")
    else:
        print("No thought blocks found yet.")

if __name__ == "__main__":
    extract_latest_thought()
