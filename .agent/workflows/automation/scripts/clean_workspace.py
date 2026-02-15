#!/usr/bin/env python3
"""
Workspace Cleaner
Moves old sprints to archive and keeps the workspace clean.
"""
import shutil
import re
from pathlib import Path
from datetime import datetime

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
SPRINTS_DIR = PROJECT_ROOT / "docs" / "dev" / "sprints"
ARTIFACTS_DIR = PROJECT_ROOT / "artifak"
SPRINTS_ARCHIVE = ARTIFACTS_DIR / "sprints_archive"
CURRENT_SPRINT_FILE = PROJECT_ROOT / "current_sprint.md"

def get_current_sprint_filename():
    """Extract the filename of the current sprint from current_sprint.md"""
    if not CURRENT_SPRINT_FILE.exists():
        print("⚠️ current_sprint.md not found.")
        return None
    
    content = CURRENT_SPRINT_FILE.read_text()
    
    # Method 1: Check for Reference Link
    # [Sprint 1.3](docs/dev/sprints/sprint1_3_sprint_queue.md)
    match = re.search(r'\(docs/dev/sprints/(.*?\.md)\)', content)
    if match:
        return match.group(1)
        
    # Method 2: Match by Title (Robust fallback)
    lines = content.splitlines()
    if lines:
        title_line = lines[0]
        # Remove standard prefixes
        clean_title = title_line.replace("# Current Sprint:", "").replace("# Sprint:", "").replace("# ", "").strip()
        print(f"  🔍 Searching for sprint with title: '{clean_title}'")
        
        for f in SPRINTS_DIR.glob("*.md"):
            try:
                f_content = f.read_text()
                f_lines = f_content.splitlines()
                if not f_lines: continue
                
                f_title = f_lines[0].replace("# Sprint:", "").replace("# ", "").strip()
                
                # Check for substring match or exact match
                if clean_title in f_title or f_title in clean_title:
                    return f.name
            except Exception:
                continue
                
    return None

def archive_old_sprints():
    """Move non-active sprints to archive"""
    if not SPRINTS_DIR.exists():
        print("No sprints directory found.")
        return

    SPRINTS_ARCHIVE.mkdir(parents=True, exist_ok=True)
    
    current_filename = get_current_sprint_filename()
    print(f"📌 Active Sprint File: {current_filename}")
    
    count = 0
    for sprint_file in SPRINTS_DIR.glob("*.md"):
        # Skip if it's the current sprint
        if sprint_file.name == current_filename:
            print(f"  👉 Keeping active: {sprint_file.name}")
            continue
            
        # Skip if it's not a sprint definition (heuristic)
        if not (sprint_file.name.startswith("sprint") or "master" in sprint_file.name):
            continue

        # Move to archive
        target = SPRINTS_ARCHIVE / sprint_file.name
        print(f"  📦 Archiving: {sprint_file.name} -> {target}")
        shutil.move(str(sprint_file), str(target))
        count += 1
        
    print(f"\n✅ Archived {count} sprint files.")

def main():
    print("🧹 Cleaning Workspace...")
    archive_old_sprints()
    print("✨ Cleanup Complete.")

if __name__ == "__main__":
    main()
