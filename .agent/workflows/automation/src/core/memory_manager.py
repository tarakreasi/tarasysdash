# .agent/workflows/automation/src/core/memory_manager.py
import os
import datetime
from pathlib import Path

MEMORY_DIR = Path(".agent/memory")
ACTIVE_CONTEXT_FILE = MEMORY_DIR / "active_context.md"
DECISION_LOG_FILE = MEMORY_DIR / "decision_log.md"

class MemoryManager:
    def __init__(self):
        self._ensure_memory_structure()

    def _ensure_memory_structure(self):
        """Ensure memory folder and files exist"""
        if not MEMORY_DIR.exists():
            MEMORY_DIR.mkdir(parents=True)
        
        if not ACTIVE_CONTEXT_FILE.exists():
            self._write_context("Initialized", "System Startup", [])

        if not DECISION_LOG_FILE.exists():
            with open(DECISION_LOG_FILE, "w") as f:
                f.write("# 📚 Decision Log\n\n")

    def update_active_context(self, focus: str, sprint_id: str, insights: list):
        """Update the active_context.md file"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        content = f"""# 🧠 Active Context (Live)
**Last Updated**: {timestamp}
**Focus**: {focus}
**Sprint**: {sprint_id}

## 💡 Librarian Insights (Auto-Fetched)
"""
        for item in insights:
            content += f"- {item}\n"

        content += """
## ⚠️ Active Constraints
- Architecture: Split Workflow
- Methodology: TDD
- Limit: 120 lines/sprint
"""
        
        with open(ACTIVE_CONTEXT_FILE, "w") as f:
            f.write(content)
        
        print(f"✅ Active Context updated for: {focus}")

    def log_decision(self, title: str, context: str, decision: str, reason: str):
        """Append a decision to the log"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        
        entry = f"""
## [{timestamp}] {title}
- **Context**: {context}
- **Decision**: {decision}
- **Reason**: {reason}
"""
        with open(DECISION_LOG_FILE, "a") as f:
            f.write(entry)
        
        print(f"✅ Decision logged: {title}")

# Usage Example:
# mem = MemoryManager()
# mem.update_active_context("Auth Module", "Sprint 4.1", ["Use JWT", "Test First"])
