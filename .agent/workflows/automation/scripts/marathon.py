#!/usr/bin/env python3
import os
import subprocess
import re
import sys

SPRINT_DIR = "docs/dev/sprints"
EXECUTOR = ".agent/workflows/automation/scripts/execute_sprint_manual.py"

def get_pending_sprints():
    sprints = []
    for f in os.listdir(SPRINT_DIR):
        if f.endswith(".md") and f.startswith("sprint6_"):
            path = os.path.join(SPRINT_DIR, f)
            with open(path, "r") as file:
                content = file.read()
                if "**Status**: PLANNING" in content:
                    sprints.append(f)
    
    # Sort by number: sprint6_2_3 -> 6, 2, 3
    def sort_key(name):
        nums = re.findall(r'\d+', name)
        return [int(n) for n in nums]
    
    return sorted(sprints, key=sort_key)

def mark_done(filename):
    path = os.path.join(SPRINT_DIR, filename)
    with open(path, "r") as file:
        content = file.read()
    
    updated = content.replace("**Status**: PLANNING", "**Status**: DONE")
    with open(path, "w") as file:
        file.write(updated)

def main():
    print("🏃 Starting Sprint Marathon...")
    pending = get_pending_sprints()
    
    if not pending:
        print("✅ No pending sprints found.")
        return

    print(f"📋 Found {len(pending)} sprints in queue.")
    
    for sprint in pending:
        print(f"\n🚀 EXECUTING: {sprint}")
        print("="*40)
        
        path = os.path.join(SPRINT_DIR, sprint)
        try:
            # Run the manual executor which uses uv and our refined supervisor
            result = subprocess.run(
                ["uv", "run", "python", EXECUTOR, path],
                check=True
            )
            
            if result.returncode == 0:
                print(f"✅ COMPLETED: {sprint}")
                mark_done(sprint)
            else:
                print(f"❌ FAILED: {sprint}. Stopping marathon.")
                sys.exit(1)
        
        except subprocess.CalledProcessError as e:
            print(f"❌ CRITICAL ERROR in {sprint}: {e}")
            sys.exit(1)

    print("\n🏆 MARATHON FINISHED! All sprints executed.")

if __name__ == "__main__":
    main()
