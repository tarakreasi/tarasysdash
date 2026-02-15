import os
import re
from pathlib import Path
from typing import Optional

class SprintScanner:
    def __init__(self, sprints_dir: str):
        self.sprints_dir = Path(sprints_dir)

    def find_next_sprint(self) -> Optional[Path]:
        """
        Find the next sprint to execute.
        Logic:
        1. List all .md files in sprints_dir.
        2. Sort alphabetically.
        3. Check status inside file.
        4. Return first one with Status: PLANNING.
        """
        if not self.sprints_dir.exists():
            print(f"❌ Sprints dir not found: {self.sprints_dir}")
            return None

        files = sorted([f for f in self.sprints_dir.glob("*.md")])
        
        for file_path in files:
            if self._check_status(file_path, "PLANNING"):
                return file_path
        
        return None

    def _check_status(self, file_path: Path, status: str) -> bool:
        try:
            content = file_path.read_text(encoding="utf-8")
            # Regex for "Status: PLANNING" (case insensitive)
            if re.search(fr"\*\*Status\*\*:\s*{status}", content, re.IGNORECASE):
                return True
            if re.search(fr"Status:\s*{status}", content, re.IGNORECASE):
                return True
        except Exception:
            pass
        return False

if __name__ == "__main__":
    # Test run
    scanner = SprintScanner("docs/supv2/mocks") # Use mocks for testing
    next_sprint = scanner.find_next_sprint()
    if next_sprint:
        print(f"🚀 Next Sprint: {next_sprint}")
    else:
        print("😴 No pending sprints found.")
