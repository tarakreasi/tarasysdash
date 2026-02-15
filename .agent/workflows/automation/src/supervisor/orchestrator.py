import sys
import subprocess
import time
import re
from pathlib import Path

# FIX: Allow execution from anywhere by adding project root to sys.path
current_file = Path(__file__).resolve()
# Assuming structure: .agent/workflows/automation/src/supervisor/orchestrator.py
# Root is 5 levels up
project_root = current_file.parents[5]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

try:
    from .scanner import SprintScanner
    from .executor import SprintExecutor
except ImportError:
    # If run as script
    from scanner import SprintScanner
    from executor import SprintExecutor
# from termcolor import colored # REMOVED

class SupervisorOrchestrator:
    def __init__(self, sprints_dir: str, auto_approve: bool = False, autostop: bool = True):
        self.scanner = SprintScanner(sprints_dir)
        
        # Load Coding Standards
        standards_path = project_root / ".agent" / "rules" / "CODING_STANDARDS.md"
        rules = ""
        if standards_path.exists():
            rules = standards_path.read_text()
            
        self.executor = SprintExecutor(coding_rules=rules)
        self.auto_approve = auto_approve
        self.autostop = autostop
        self.project_root = Path.cwd()

    def log(self, level, msg):
        # Simple logging without colors
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {msg}")

    def run_loop(self):
        self.log("SYSTEM", f"🕵️ Supervisor V3 ({'Watch' if not self.autostop else 'One-pass'}) Started...")
        self.log("INFO", f"Scanning: {self.scanner.sprints_dir}")

        while True:
            try:
                next_sprint = self.scanner.find_next_sprint()
                
                if not next_sprint:
                    if self.autostop:
                        self.log("SUCCESS", "🏁 No pending sprints. Autostop engaged. Goodbye!")
                        break
                    else:
                        self.log("INFO", "💤 No pending sprints. Sleeping 5s...")
                        time.sleep(5)
                        continue

                self.log("SYSTEM", f"📢 Found Sprint: {next_sprint.name}")
                
                if not self.auto_approve:
                    # User Gate
                    print(f"   Execute {next_sprint.name}? [Y/n]: ", end="", flush=True)
                    confirm = sys.stdin.readline().strip().lower()
                    if confirm == 'n':
                        self.log("WARNING", "Skipping sprint (User aborted).")
                        if self.autostop:
                            break
                        time.sleep(10)
                        continue
                
                # EXECUTE
                self._process_sprint(next_sprint)
                
            except KeyboardInterrupt:
                self.log("SYSTEM", "\n🛑 Supervisor actions stopped by user.")
                break
            except Exception as e:
                self.log("ERROR", f"Supervisor Crash: {e}")
                if self.autostop:
                    break
                time.sleep(5)

    def _process_sprint(self, sprint_path: Path):
        self.log("INFO", f"⚡ Executing Sprint: {sprint_path.name}")
        
        # 1. Update Status to IN_PROGRESS
        self._update_status(sprint_path, "IN_PROGRESS")
        
        # 2. Run Executor Logic
        try:
            success = self.executor.execute(sprint_path)
            
            if not success:
                self.log("ERROR", "❌ Execution Failed (Some tasks failed)")
                self._update_status(sprint_path, "FAILED")
                return
            
            # 3. Find and Run Verification Script
            self.log("INFO", "🔍 Searching for verification script...")
            verify_script = self._find_verify_script(sprint_path)
            
            if verify_script:
                self.log("INFO", f"🧪 Running Verification: {verify_script}")
                # Ensure executable
                ver_cmd = ["python3", str(verify_script)]
                ver_res = subprocess.run(ver_cmd, capture_output=True, text=True, cwd=self.project_root)
                
                if ver_res.returncode == 0:
                    self.log("SUCCESS", f"✅ Verification Passed:\n{ver_res.stdout.strip()}")
                    self._update_status(sprint_path, "DONE")
                    self._git_commit(sprint_path.name)
                else:
                    self.log("ERROR", f"❌ Verification Failed:\n{ver_res.stdout}\n{ver_res.stderr}")
                    self._update_status(sprint_path, "VERIFY_FAILED")
            else:
                self.log("WARNING", "⚠️ No verification script found in sprint definition.")
                self.log("SUCCESS", "✅ Marked DONE (Unverified)")
                self._update_status(sprint_path, "DONE")
                self._git_commit(sprint_path.name)

        except Exception as e:
            self.log("ERROR", f"Process Error: {e}")
            self._update_status(sprint_path, "ERROR")

    def _find_verify_script(self, sprint_path: Path):
        """Parse sprint file to find 'verify_*.py' filename"""
        content = sprint_path.read_text()
        # Look for **File**: `path/to/verify_foo.py`
        matches = re.findall(r'\*\*File\*\*: `(.*verify_.*\.py)`', content)
        if matches:
            # Use the last one found (most specific?) or first? Usually specific sprints have one.
            return matches[-1]
        return None

    def _update_status(self, file_path: Path, new_status: str):
        """Regex replace Status: ... with Status: NEW_STATUS"""
        try:
            content = file_path.read_text()
            # Replace Status: X or **Status**: X
            new_content = re.sub(
                r'((\*\*Status\*\*|Status):\s*)([A-Z_]+)', 
                f'\\1{new_status}', 
                content, 
                count=1
            )
            file_path.write_text(new_content)
            self.log("SYSTEM", f"📝 Updated status to {new_status}")
        except Exception as e:
            self.log("ERROR", f"Failed to update status: {e}")

    def _git_commit(self, task_name: str):
        """Auto Commit"""
        try:
            subprocess.run(["git", "add", "."], check=True, stdout=subprocess.DEVNULL)
            msg = f"feat(auto): Complete {task_name}"
            subprocess.run(["git", "commit", "-m", msg], stdout=subprocess.DEVNULL)
            self.log("SUCCESS", f"💾 Git Committed: {msg}")
        except:
            pass # Git might fail if no changes or no repo, ignore

if __name__ == "__main__":
    target_dir = "docs/dev/sprints"
    auto = False
    cont = False
    
    if "--auto" in sys.argv:
        auto = True
    
    if "--continuous" in sys.argv:
        cont = True
        
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        target_dir = sys.argv[1]
        
    # Default is autostop=True unless --continuous is specified
    sup = SupervisorOrchestrator(target_dir, auto_approve=auto, autostop=(not cont))
    sup.run_loop()
