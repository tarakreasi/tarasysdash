import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.abspath(".agent/workflows/automation/src"))
from supervisor.executor import SprintExecutor

if len(sys.argv) < 2:
    print("Usage: python execute_sprint.py <sprint_file.md>")
    sys.exit(1)

sprint_file = Path(sys.argv[1])
if not sprint_file.exists():
    print(f"File not found: {sprint_file}")
    sys.exit(1)

executor = SprintExecutor(coding_rules="Follow Vue 3 Style Guide")
success = executor.execute(sprint_file)

if success:
    print("✅ Sprint Execution Successful")
    sys.exit(0)
else:
    print("❌ Sprint Execution Failed")
    sys.exit(1)
