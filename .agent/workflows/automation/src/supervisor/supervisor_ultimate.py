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


class SprintSupervisor:
    """
    The Ultimate Autonomous Supervisor
    
    Combines best features:
    - Backup: Git commits, user approval, state transitions
    - Current: termcolor, enhanced approval, better config
    """
    
    def __init__(self, max_retries: int = None):
        self.state_manager = StateManager()
        self.approval_engine = ApprovalEngine()
        self.llm = get_llm(model=MODEL_SMART, temperature=0.3)
        self.max_retries = max_retries or MAX_RETRIES
        self.last_error: Optional[str] = None
        
        # Setup logging
        self._setup_logging()
        
        # Force CWD to project root
        import os
        os.chdir(self.state_manager.project_root)
        print(colored(f"ℹ️ Set CWD to: {self.state_manager.project_root}", "green"))
    
    def _setup_logging(self):
        """Setup file logging"""
        log_file = Path(__file__).parent.parent.parent / "supervisor.log"
        self.log_file = log_file
        
    def log(self, level: str, message: str):
        """Log message to file and console with colors"""
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
                    self._enter_review_state()
                    break
                
                # Check sprint status
                if sprint.status == SprintStatus.ERROR_HALT:
                    self.log("ERROR", "Sprint in ERROR_HALT state. Manual intervention required.")
                    break
                
                if sprint.status == SprintStatus.WAITING_USER:
                    self.log("WARNING", "Sprint in WAITING_USER state. Waiting for user action.")
                    break
                
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
                    
                    # In autonomous mode, cannot wait for input
                    self._enter_waiting_state()
                    self.log("INFO", "Entering WAITING_USER state. Supervisor paused.")
                    break
                
                # AUTO APPROVED
                self.log("SUCCESS", f"✅ APPROVED: {approval.reason}")
                
                # BUILD: Execute the plan
                self.log("INFO", "🔨 BUILDING...")
                success = self._execute_plan(plan, next_task.name)
                
                if not success:
                    retry_count += 1
                    if retry_count >= self.max_retries:
                        self.log("ERROR", f"Max retries ({self.max_retries}) reached. Halting.")
                        self._enter_error_halt_state()
                        break
                    
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
            # Use AI to generate plan
            context = self._gather_context()
            
            prompt = f"""You are planning the implementation for this task:

SPRINT: {sprint.name}
OBJECTIVE: {sprint.objective}
TASK: {task_name}

CONTEXT:
{context}
{error_context}

Please create a detailed, atomic implementation plan for this specific task.

Rules:
1. FOCUS only on coding and file manipulation.
2. DO NOT include git push, deploy, or release steps. The system handles version control.
3. DO NOT include "pip install" or "npm install" unless strictly necessary for new packages.
4. Use clear, executable steps.

Format: Markdown.
"""
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
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
    
    def _request_approval(self, plan: str, task_name: str):
        """Request approval for plan"""
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
        """Execute plan via LangGraph AI agent"""
        from ..agents.graph import run_agent
        
        self.log("INFO", f"🧠 Executing task via LangGraph: {task_name}")
        
        context = self._gather_context()
        result = run_agent(task_name, plan, context)
        
        # Extract summary from result
        messages = result.get("messages", [])
        if messages:
            last_msg = messages[-1]
            summary = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)
            self.log("SUCCESS", f"🤖 Agent completion summary:\n{summary[:500]}")
        
        # Verify the task
        return self._verify_task(task_name)
    
    def _execute_deterministic(self, plan: str, task_name: str) -> bool:
        """Execute plan using deterministic logic (fallback)"""
        self.log("INFO", f"⚙️ Executing DETERMINISTIC build for: {task_name}")
        
        # Simple deterministic execution (mostly pass-through)
        # This is a fallback when AI is disabled
        
        # For now, just verify
        return self._verify_task(task_name)
    
    def _verify_task(self, task_name: str) -> bool:
        """Verify that the task was completed successfully"""
        self.log("INFO", "🔍 VERIFYING...")
        self.log("INFO", f"🔍 Verifying task: {task_name}")
        
        # Extract file paths from task name if present
        import re
        file_pattern = r'`([^`]+\.[a-zA-Z]+)`'
        files = re.findall(file_pattern, task_name)
        
        if files:
            # Check if files exist
            for file_path in files:
                full_path = self.state_manager.project_root / file_path
                if not full_path.exists():
                    self.log("WARNING", f"⚠️ File not found: {full_path}")
                    self.last_error = f"File {file_path} was not created."
                    return False
                else:
                    self.log("SUCCESS", f"✓ File exists: {full_path}")
        
        # Additional verification could be added here
        # e.g., run tests, check build, etc.
        
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
    
    def _enter_review_state(self):
        """Enter REVIEW state when sprint is complete"""
        self.state_manager.update_sprint_status(SprintStatus.REVIEW)
        self.log("INFO", "Entering REVIEW state")
    
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


# For backwards compatibility
def run_supervisor():
    """Entry point for supervisor execution"""
    supervisor = SprintSupervisor()
    supervisor.run_continuous_loop()
