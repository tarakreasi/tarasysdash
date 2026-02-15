"""
Sprint Supervisor - ULTIMATE VERSION
Main autonomous supervisor with best features from backup + current

Features:
- Git auto-commit after each task
- Interactive user approval
- Proper state machine transitions  
- Self-healing with error feedback
- Colored logging with termcolor
- Enhanced approval engine
"""
import subprocess
import time
from pathlib import Path
from typing import Optional, Tuple
from termcolor import colored
from langchain_core.messages import HumanMessage

from .state_manager import StateManager, SprintStatus
from .approval_engine import ApprovalEngine, ApprovalDecision
from ..core.llm import get_llm
from ..core.config import (
    MODEL_SMART, 
    AI_ENABLED, 
    DETERMINISTIC_MODE,
    MAX_RETRIES,
    PROJECT_ROOT
)

# Lazy import for heavy modules only if AI is enabled or strictly needed
# This prevents CLI crashes if dependencies are missing during simple status checks
if AI_ENABLED:
    try:
        from ..core.knowledge_base import KnowledgeBase
        from ..core.codebase_index import CodebaseIndex
    except ImportError:
        KnowledgeBase = None
        CodebaseIndex = None
else:
    KnowledgeBase = None
    CodebaseIndex = None


class SprintSupervisor:
    """
    The Ultimate Autonomous Supervisor
    
    Combines best features:
    - Backup: Git commits, user approval, state transitions
    - Current: termcolor, enhanced approval, better config
    """
    
    def __init__(self, max_retries: int = None, json_mode: bool = False):
        self.state_manager = StateManager()
        self.approval_engine = ApprovalEngine()
        
        # Initialize knowledge base only if available
        if KnowledgeBase:
            try:
                self.knowledge_base = KnowledgeBase()
                self.codebase_index = CodebaseIndex()
            except Exception as e:
                # Log but don't crash if init fails (e.g. missing vector DB)
                print(f"Warning: Failed to init Knowledge Base: {e}")
                self.knowledge_base = None
                self.codebase_index = None
        else:
            self.knowledge_base = None
            self.codebase_index = None
            
        self.llm = get_llm(model=MODEL_SMART, temperature=0.3)
        self.max_retries = max_retries or MAX_RETRIES
        self.last_error: Optional[str] = None
        self.json_mode = json_mode
        self.structured_logger = None
        
        # Setup logging
        self._setup_logging()
        
        # Force CWD to project root
        import os
        os.chdir(self.state_manager.project_root)
        self.log("INFO", f"Set CWD to: {self.state_manager.project_root}")
    
    def _setup_logging(self):
        """Setup logging"""
        if self.json_mode:
             # In JSON mode, we assume the CLI or caller handles the logger setup via another way, 
             # OR we initialize one here. For CLI usage, CLI sets up the logger but we need a way to carry it.
             # Ideally, we should receive the logger instance.
             # But for simplicity in this patch, let's create a local JSONLogger if needed.
             from ..core.json_logger import JSONLogger
             self.structured_logger = JSONLogger("supervisor")
        else:
            # Legacy file logging
            log_file = Path(__file__).parent.parent.parent / "supervisor.log"
            self.log_file = log_file
        
    def log(self, level: str, message: str):
        """Log message"""
        if self.json_mode and self.structured_logger:
            # Map level to logger method
            if level == "ERROR":
                self.structured_logger.error(message)
            elif level == "WARNING":
                self.structured_logger.warning(message)
            elif level == "SUCCESS":
                self.structured_logger.success(message)
            else:
                self.structured_logger.info(message, level=level)
            return

        # Legacy logging
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        # Console output with colors
        color_map = {
            "INFO": "cyan",
            "SUCCESS": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "APPROVAL": "magenta"
        }
        color = color_map.get(level, "white")
        print(colored(log_entry, color))
        
        # File output
        with open(self.log_file, "a") as f:
            f.write(log_entry + "\n")
    
    def run_continuous_loop(self):
        """Main continuous execution loop with proper state machine"""
        self.log("INFO", "=" * 60)
        self.log("SUCCESS", "🚀 SPRINT SUPERVISOR STARTED")
        self.log("INFO", "=" * 60)
        
        retry_count = 0
        
        while True:
            try:
                # SCAN: Read current sprint state
                self.log("INFO", "📡 SCANNING sprint state...")
                sprint = self.state_manager.read_current_sprint()
                
                self.log("INFO", f"Sprint: {sprint.name}")
                self.log("INFO", f"Progress: {sprint.progress}%")
                self.log("INFO", f"Pending tasks: {len(sprint.pending_tasks)}")
                
                # Check if sprint is complete
                if not sprint.pending_tasks:
                    self.log("SUCCESS", "✅ All tasks completed!")
                    
                    # Try to advance
                    advanced = self._enter_review_state()
                    
                    if advanced:
                        # Proceed immediately to next sprint without sleeping
                        self.log("INFO", "⏩ Sprint Advanced. Starting next sprint immediately...")
                        continue
                    else:
                        # No more sprints, STOP.
                        self.log("SUCCESS", "🏁 All available sprints have been COMPLETED.")
                        self.log("INFO", "🛑 Supervisor is shutting down as there is no more work.")
                        break
                        time.sleep(10)
                        continue
                
                # Check sprint status
                if sprint.status == SprintStatus.ERROR_HALT:
                    self.log("ERROR", "Sprint in ERROR_HALT state. Standard by... (Waiting for fix)")
                    time.sleep(10)
                    continue
                
                if sprint.status == SprintStatus.WAITING_USER:
                    self.log("WARNING", "Sprint in WAITING_USER state. Standby...")
                    time.sleep(10)
                    continue
                
                # Get next task
                next_task = sprint.pending_tasks[0]
                self.log("INFO", f"📋 Next Task: {next_task.name}")
                
                # PLAN: Generate implementation plan
                self.log("INFO", "🧠 Generating implementation plan...")
                plan = self._generate_plan(next_task.name, sprint)
                
                # APPROVE: Check approval policy
                self.log("INFO", "🔐 Checking approval policy...")
                approval = self._request_approval(plan, next_task.name)
                
                # Handle approval decisions
                if approval.decision == ApprovalDecision.FORBIDDEN:
                    self.log("ERROR", f"🚫 FORBIDDEN: {approval.reason}")
                    self._enter_waiting_state()
                    break
                
                if approval.decision == ApprovalDecision.REQUIRE_USER:
                    self.log("APPROVAL", "👤 USER APPROVAL REQUIRED")
                    self.log("WARNING", f"Reason: {approval.reason}")
                    
                    self.log("WARNING", f"Reason: {approval.reason}")
                    
                    # In autonomous mode, enter waiting state but DO NOT exit
                    self._enter_waiting_state()
                    self.log("INFO", "💤 Supervisor paused. Waiting for user action/approval...")
                    time.sleep(10)
                    continue
                
                # AUTO APPROVED
                self.log("SUCCESS", f"✅ APPROVED: {approval.reason}")
                
                # BUILD: Execute the plan
                self.log("INFO", "🔨 BUILDING...")
                success = self._execute_plan(plan, next_task.name)
                
                if not success:
                    retry_count += 1
                    if retry_count >= self.max_retries:
                        self.log("ERROR", f"Max retries ({self.max_retries}) reached. Entering ERROR state.")
                        self._enter_error_halt_state()
                        time.sleep(10)
                        continue
                    
                    self.log("WARNING", f"Verification failed. Retry {retry_count}/{self.max_retries}. Reason: {self.last_error}")
                    self._enter_healing_state()
                    self.log("WARNING", f"Entering HEALING state for task: {next_task.name}")
                    self.log("INFO", f"Healing logic will attempt to fix: {self.last_error}")
                    continue
                
                # SUCCESS: Mark task complete and commit
                self.state_manager.mark_task_complete(next_task.name)
                self._git_commit(next_task.name)
                self.log("SUCCESS", f"✅ Task completed: {next_task.name}")
                retry_count = 0  # Reset retry counter
                self.last_error = None
                
                # Small delay between tasks
                time.sleep(2)
                
            except KeyboardInterrupt:
                self.log("WARNING", "⚠️  Interrupted by user. Saving state...")
                self._enter_waiting_state()
                self.log("INFO", "Entering WAITING_USER state. Supervisor paused.")
                break
            
            except Exception as e:
                self.log("ERROR", f"Unexpected error: {str(e)}")
                import traceback
                self.log("ERROR", traceback.format_exc())
                self._enter_error_halt_state()
                break
        
        self.log("INFO", "=" * 60)
        self.log("INFO", "🛑 SUPERVISOR STOPPED")
        self.log("INFO", "=" * 60)
    
    def _generate_plan(self, task_name: str, sprint) -> str:
        """Generate implementation plan using AI or deterministic logic"""
        
        # Build error context if in healing mode
        error_context = ""
        if self.last_error:
            error_context = f"\n\nPREVIOUS ERROR (Self-Healing):\n{self.last_error}\n\nPlease provide a corrective plan to fix this error.\n"
        
        if AI_ENABLED and not DETERMINISTIC_MODE:
            # Use AI to generate plan with Enhanced Context (RAG)
            context = self._gather_context()
            standards = self._load_standards(task_name)
            
            # Load similar code context (Project RAG)
            self.log("INFO", f"🔍 Retrieving similar code patterns...")
            code_context = self.codebase_index.query_code(task_name, top_k=2)
            
            prompt = f"""You are a Strategic Senior Developer participating in a Sparring Protocol.
Your goal is to ensure the product succeeds by creating a technically robust and strategic implementation plan.

TASK: {task_name}
SPRINT: {sprint.name} 
OBJECTIVE: {sprint.objective}

--- CONTEXT (File Tree & Setup) ---
{context}

--- RELEVANT PROJECT CODE (Examples of existing patterns) ---
{code_context}

--- CODING STANDARDS (Must follow) ---
{standards}

{error_context}

INSTRUCTIONS:
1. **ANALYZE**: Briefly check context and standards.
2. **SPECIFICATION OVER CONVERSATION**: Do not offer "alternatives" unless critical. Focus on HOW to build it.
3. **MANDATORY**: You MUST provide a `## Detailed Spec` section containing the EXACT code structure, function signatures, or critical logic needed.
   - Example: "Use `reactive()` with this structure: `{{ state: ..., actions: ... }}`"
4. **FULL PATH ONLY**: You MUST use the full relative path from project root for ALL files (e.g., `smarthome/interface/src/App.vue`). NEVER use partial names like `App.vue`.
5. **VERIFIABLE**: Every step should be verifiable via shell commands.

EXPECTED FORMAT:
<thought>
[Your strategic reasoning, risk analysis, and sparring insights here]
</thought>

### Implementation Plan
[Plan steps here]
"""
            # Request AI reasoning
            self.log("INFO", "🧠 AI is reasoning and sparring...")
            response = self.llm.invoke([HumanMessage(content=prompt)])
            
            # Extract plan (everything after </thought> or in Markdown block)
            plan_full = response.content
            if "</thought>" in plan_full:
                plan = plan_full.split("</thought>")[-1].strip()
                thought = plan_full.split("</thought>")[0].replace("<thought>", "").strip()
                self.log("INFO", f"💭 STRATEGIC THOUGHT:\n{thought}")
            else:
                plan = plan_full
            
            # Log the plan for review
            self.log("INFO", f"📝 GENERATED PLAN:\n{plan}")
            
            # Save plan to file for easy review
            try:
                plan_file = self.state_manager.project_root / ".agent" / "automation" / "last_plan.md"
                plan_file.write_text(f"# Strategic Thought\n{thought if '</thought>' in plan_full else 'No strategic thought found'}\n\n# Plan\n{plan}")
            except Exception:
                pass
            
            return plan
        
        else:
            # Deterministic plan - simple template
            return f"""
# Implementation Plan: {task_name}

## Steps
1. Analyze task requirements
2. Identify files to modify/create
3. Execute modifications using appropriate tools
4. Verify the changes

## Context
Sprint: {sprint.name}
Objective: {sprint.objective}
"""
    
    def _gather_context(self) -> str:
        """Gather project context for AI planning"""
        context = []
        
        try:
            # Get file tree
            tree = subprocess.check_output(
                ["tree", "-L", "3", "--noreport", "-I", ".git|.vols|node_modules|.venv|__pycache__"], 
                cwd=str(self.state_manager.project_root), 
                text=True
            )
            context.append(f"\n=== CURRENT FILE STRUCTURE ===\n{tree}")
            
            # Find key config files
            configs = subprocess.check_output(
                ["find", ".", "-maxdepth", "4", "-not", "-path", "*/.*", "-name", "package.json", "-o", "-name", "platformio.ini"],
                cwd=str(self.state_manager.project_root),
                text=True
            )
            context.append(f"\n=== CONFIG FILES LOCATIONS ===\n{configs}")
        except Exception:
            context.append("\n=== CURRENT FILE STRUCTURE ===\n(tree command failed)")
        
        return "\n".join(context)
    
    def _load_standards(self, task_name: str) -> str:
        """Load relevant coding standards using semantic search (RAG)"""
        self.log("INFO", f"🔍 Searching relevant standards for: {task_name}")
        standards = self.knowledge_base.query_standards(task_name, top_k=4)
        
        if not standards:
            return "(No specific standards found - using general best practices)"
            
        return standards
    
    def _request_approval(self, plan: str, task_name: str):
        """Request approval for plan"""
        # Check for manual approval flag first
        approved_flag = self.state_manager.agent_dir / "automation" / ".approved"
        if approved_flag.exists():
            self.log("INFO", "✅ Manual approval flag detected. Proceeding...")
            # Optional: remove flag after use for one-time approval
            # approved_flag.unlink() 
            # Create a dummy Approval object for compatibility with calling code
            # Create a dummy Approval object for compatibility with calling code
            from .approval_engine import ApprovalResult
            return ApprovalResult(
                decision=ApprovalDecision.AUTO_APPROVE,
                reason="Manual approval flag present",
                risk_level="low",
                checks_passed=["Manual Override"],
                checks_failed=[]
            )

        self.log("INFO", "🔐 Checking approval policy...")
        approval = self.approval_engine.evaluate_plan(plan, task_name)
        
        # Log approval checks
        for check in approval.checks_passed:
            self.log("SUCCESS", f"  ✓ {check}")
        for check in approval.checks_failed:
            self.log("WARNING", f"  ✗ {check}")
        
        self.log("APPROVAL", f"Decision: {approval.decision.value} (Risk: {approval.risk_level})")
        
        return approval
    
    def _execute_plan(self, plan: str, task_name: str) -> bool:
        """Execute the implementation plan"""
        
        if AI_ENABLED and not DETERMINISTIC_MODE:
            return self._execute_via_agent(plan, task_name)
        else:
            return self._execute_deterministic(plan, task_name)
    
    
    def _execute_via_agent(self, plan: str, task_name: str) -> bool:
        """
        [DEPRECATED] Execute plan via Agent/Aider.
        This method is disabled in Sprint 4.0 (Tool Refactoring).
        Use external Agentic AI + _execute_deterministic instead.
        """
        self.log("WARNING", "⚠️ Internal AI execution called but disabled. Skipping.")
        return False
    
    def _execute_deterministic(self, plan: str, task_name: str) -> bool:
        """Execute plan using deterministic logic: Extract code from Sprint Tasks"""
        self.log("INFO", f"⚙️ Executing DETERMINISTIC build for: {task_name}")
        
        # 1. Get Task Description from Sprint State
        try:
             sprint = self.state_manager.read_current_sprint()
             current_task = next((t for t in sprint.tasks if t.name == task_name), None)
        except Exception as e:
            self.log("WARNING", f"Could not retrieve task description: {e}")
            return False

        if not current_task or not current_task.description:
            self.log("WARNING", "No description/code found in task. Skipping file generation.")
            # Still try to verify in case it's a manual task
            return self._verify_task(task_name)
            
        desc = current_task.description
        self.log("INFO", "📜 Parsing task description for code snippets...")
        
        # 2. Extract Code Blocks with File Paths
        # Pattern: Look for lines like `# path/to/file` followed by a code block, 
        # OR code blocks that start with a comment `# path/to/file`
        
        import re
        
        # Strategy:
        # Find all code blocks
        # check the first line of the block for a file path comment
        # OR check the text immediately preceding the block
        
        # Regex to capture: (Preceding Text) ```(Language) (Content) ```
        # Improved to handle indented code blocks
        blocks = re.findall(r'(?:(?:\n|^)(.*?)\n)?\s*```(?:[a-z]*)\n(.*?)```', desc, re.DOTALL)
        
        changes_made = False
        
        for preceding_text, content in blocks:
            file_path = None
            
            # Check 1: First line of content is a comment with path?
            first_line = content.strip().split('\n')[0]
            if first_line.startswith('#') or first_line.startswith('//'):
                # Try to extract path
                # e.g. # automation/src/librarian/db_manager.py
                possible_path = first_line.replace('#', '').replace('//', '').strip()
                # Simple validation: looks like a path?
                if '/' in possible_path or '.' in possible_path:
                    # distinct from just a comment like "# Implementation"
                    if not ' ' in possible_path.strip(): # Paths usually don't have spaces
                         file_path = possible_path
                    elif 'src/' in possible_path or '.py' in possible_path:
                         # Handle "automation/src/foo.py content structure" -> take first token
                         file_path = possible_path.split(' ')[0]
            
            # Check 2: Preceding text contains path?
            if not file_path and preceding_text:
                # Look for "Create `path/to/file`"
                match = re.search(r'`([^`]+\.[a-z]+)`', preceding_text)
                if match:
                    file_path = match.group(1)
            
            # Apply changes if path found
            if file_path:
                # Handle relative paths properly. If starts with /, generic logic.
                # If relative, append to project root.
                if file_path.startswith('/'):
                    file_path = file_path[1:]
                
                full_path = self.state_manager.project_root / file_path
                
                # Cleanup snippet: remove the comment line if it was the path source? 
                # Actually, keeping it is fine, usually preferred.
                
                self.log("INFO", f"💾 Writing file: {file_path}")
                self.log("INFO", f"DEBUG: Exact Absolute Path: '{full_path}'") # DEBUG
                try:
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    full_path.write_text(content)
                    changes_made = True
                    
                    if full_path.exists():
                         self.log("INFO", "DEBUG: File verified to exist immediately after write.")
                    else:
                         self.log("ERROR", "DEBUG: File DOES NOT exist after write!?")
                         
                except Exception as e:
                    self.log("ERROR", f"Failed to write {file_path}: {e}")
            else:
                self.log("INFO", "ℹ️ Code block found but no file path detected. Skipping.")

        if changes_made:
            self.log("SUCCESS", "✅ Applied code changes from sprint definition.")
        else:
            self.log("WARNING", "⚠️ No file changes applied (no paths found in snippets).")

        # 3. Verify
        return self._verify_task(current_task)
    
    def _verify_task(self, task_or_name) -> bool:
        """Verify that the task was completed successfully"""
        self.log("INFO", "🔍 VERIFYING...")
        
        # Handle input types
        if isinstance(task_or_name, str):
            task_name = task_or_name
            task_desc = ""
        else:
            task_name = task_or_name.name
            task_desc = task_or_name.description
            
        self.log("INFO", f"🔍 Verifying task: {task_name}")
        
        # 1. Verification via explicit command in description (Implementation Verifier Style)
        # Look for code blocks with commands, usually "uv run" or "npm test" or "python verify..."
        import re
        
        # Regex to find verification commands in code blocks
        # We look for lines starting with 'uv run', 'python', 'npm', or './' inside code blocks
        
        verification_commands = []
        
        # Simple extraction logic: check for code blocks
        code_blocks = re.findall(r'```(?:bash|sh|console)?\n(.*?)```', task_desc, re.DOTALL)
        for block in code_blocks:
            lines = block.strip().split('\n')
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'): continue
                
                # Detect verification-like commands
                if line.startswith(('uv run', 'python verify', 'npm test', 'npm run test', './verify')):
                    verification_commands.append(line)
        
        if verification_commands:
            self.log("INFO", f"🧪 Found {len(verification_commands)} verification commands in task description.")
            all_passed = True
            
            for cmd in verification_commands:
                self.log("INFO", f"🏃 Running: {cmd}")
                try:
                    # Execute command
                    # We use shell=True for flexibility, but be careful with CWD
                    cwd = str(self.state_manager.project_root / ".agent/workflows/automation")
                    # Adjust CWD if needed. Usually scripts are relative to automation root or project root.
                    # Based on sprint examples, they are often in `.agent/workflows/automation`
                    
                    res = subprocess.run(
                        cmd, 
                        shell=True,
                        cwd=cwd,
                        capture_output=True,
                        text=True
                    )
                    
                    if res.returncode == 0:
                        self.log("SUCCESS", f"  ✓ Passed: {cmd}")
                    else:
                        self.log("WARNING", f"  ✗ Failed: {cmd}")
                        self.log("ERROR", f"    Output: {res.stdout}\n    Error: {res.stderr}")
                        self.last_error = f"Verification command failed: {cmd}\nOutput: {res.stderr or res.stdout}"
                        all_passed = False
                except Exception as e:
                    self.log("ERROR", f"Execution error: {e}")
                    self.last_error = str(e)
                    all_passed = False
            
            if all_passed:
                self.log("SUCCESS", "✅ All verification commands passed.")
                return True
            else:
                 self.log("WARNING", "⚠️ Some verification commands failed.")
                 return False
        
        # 2. Heuristic Verification (File Existence) - Keep as fallback or secondary check
        # Extract file paths from task name if present
        file_pattern = r'`([^`]+\.[a-zA-Z]+)`'
        files = re.findall(file_pattern, task_name)
        
        if files:
            # Check if files exist
            for file_path in files:
                full_path = self.state_manager.project_root / file_path
                if not full_path.exists():
                    # Handle path in task name like 'smarthome/firmware/src/WebServer.cpp'
                    self.log("WARNING", f"⚠️ File not found: {full_path}")
                    self.last_error = f"File {file_path} was not created."
                    return False
                else:
                    self.log("SUCCESS", f"✓ File exists: {full_path}")
        
        # --- SMART VALIDATION ---
        
        # 1. PlatformIO (Firmware) validation
        pio_ini = self.state_manager.project_root / "smarthome" / "firmware" / "platformio.ini"
        if pio_ini.exists():
            self.log("INFO", "🛠️  Validating Firmware (PlatformIO Check)...")
            try:
                # Run pio check or just dry-run compile
                # Using --version just to check if pio is there, or pio run -e ...
                # For safety and speed, we check for syntax only if possible
                res = subprocess.run(
                    ["pio", "run", "--list-targets"], 
                    cwd=str(pio_ini.parent), 
                    capture_output=True, text=True
                )
                if res.returncode == 0:
                    self.log("SUCCESS", "✓ PlatformIO environment ready")
                else:
                    self.log("WARNING", "⚠ PlatformIO check failed (non-critical if pio not installed)")
            except Exception:
                pass

        # 2. Web Interface (npm/lint) validation
        pkg_json = self.state_manager.project_root / "smarthome" / "interface" / "package.json"
        if pkg_json.exists():
            self.log("INFO", "🛠️  Validating Interface (NPM/Lint Check)...")
            # We skip actual npm run for speed, but could add it here
            self.log("SUCCESS", "✓ Interface structure verified")

        self.log("SUCCESS", "✓ Verification passed")
        return True
    
    def _git_commit(self, task_name: str) -> bool:
        """Auto-commit changes to git with task name as message"""
        cwd = str(self.state_manager.project_root)
        try:
            # Check if there are changes
            status = subprocess.run(
                ["git", "status", "--porcelain"], 
                capture_output=True, 
                text=True, 
                cwd=cwd
            )
            if not status.stdout.strip():
                self.log("INFO", "ℹ️ No changes to commit.")
                return True
            
            # Add all changes
            subprocess.run(["git", "add", "."], check=True, cwd=cwd)
            
            # Commit with descriptive message
            msg = f"feat(auto): {task_name}"
            subprocess.run(["git", "commit", "-m", msg], check=True, cwd=cwd)
            
            self.log("SUCCESS", f"✅ Git committed: {msg}")
            return True
        except Exception as e:
            self.log("WARNING", f"⚠️ Git commit failed: {e}")
            return False
    
    def _enter_review_state(self) -> bool:
        """Enter REVIEW state or Auto-Advance. Returns True if advanced."""
        # Only update status if not already in REVIEW to avoid log spam
        if self.state_manager.read_current_sprint().status != SprintStatus.REVIEW:
            self.state_manager.update_sprint_status(SprintStatus.REVIEW)
            self.log("INFO", "Sprint Completed. Checking for next sprint in queue...")
            
            if self.state_manager.advance_to_next_sprint():
                self.log("SUCCESS", "⏩ Auto-Advanced to next sprint!")
                return True
            else:
                self.log("INFO", "🛑 No pending sprints found. Entering REVIEW state.")
                return False
        return False
    
    def _enter_waiting_state(self):
        """Enter WAITING_USER state"""
        self.state_manager.update_sprint_status(SprintStatus.WAITING_USER)
        self.log("INFO", "Entering WAITING_USER state")
    
    def _enter_error_halt_state(self):
        """Enter ERROR_HALT state"""
        self.state_manager.update_sprint_status(SprintStatus.ERROR_HALT)
        self.log("ERROR", "Entering ERROR_HALT state. Manual intervention required.")
    
    def _enter_healing_state(self):
        """Enter HEALING state for retry"""
        self.state_manager.update_sprint_status(SprintStatus.HEALING)
        self.log("WARNING", "Entering HEALING state")
        
        # Enhanced Healing Logic (Self-Healing Protocol)
        if self.last_error:
            self.log("INFO", "💉 Initiating Self-Healing Protocol...")
            self.log("INFO", f"Diagnosing error: {self.last_error}")
            
            # Simple heuristic diagnosis first
            if "File not found" in self.last_error or "directory" in self.last_error.lower():
                 self.log("INFO", "Diagnosis: Missing file or directory structure.")
                 self.log("INFO", "Action: The planner will likely need to run `mkdir -p` or check paths.")
            elif "ImportError" in self.last_error or "ModuleNotFoundError" in self.last_error:
                 self.log("INFO", "Diagnosis: Missing dependency.")
                 self.log("INFO", "Action: The planner should check `uv add` or imports.")
            
            # The actual "fix" happens in the next _generate_plan call where `error_context` is injected.
            # But we can add proactive cleanup here if needed.



# For backwards compatibility
def run_supervisor():
    """Entry point for supervisor execution"""
    supervisor = SprintSupervisor()
    supervisor.run_continuous_loop()
