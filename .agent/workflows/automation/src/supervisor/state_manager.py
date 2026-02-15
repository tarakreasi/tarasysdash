"""
Sprint State Manager
Handles reading and writing sprint state from current_sprint.md
"""
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from ..core.config import PROJECT_ROOT, AGENT_DIR, SPRINTS_DIR


class SprintStatus(Enum):
    """Sprint execution status"""
    IDLE = "IDLE"
    SCANNING = "SCANNING"
    PLANNING = "PLANNING"
    BUILDING = "BUILDING"
    VERIFYING = "VERIFYING"
    HEALING = "HEALING"
    REVIEW = "REVIEW"
    COMPLETED = "COMPLETED"
    ERROR_HALT = "ERROR_HALT"
    WAITING_USER = "WAITING_USER"


@dataclass
class Task:
    """Represents a single task in the backlog"""
    name: str
    completed: bool
    description: str = ""
    
    def __repr__(self):
        status = "✓" if self.completed else "○"
        return f"{status} {self.name}"


@dataclass
class SprintState:
    """Complete sprint state"""
    name: str
    objective: str
    status: SprintStatus
    tasks: List[Task]
    
    @property
    def progress(self) -> float:
        """Calculate progress percentage"""
        if not self.tasks:
            return 0.0
        completed = sum(1 for t in self.tasks if t.completed)
        return (completed / len(self.tasks)) * 100
    
    @property
    def pending_tasks(self) -> List[Task]:
        """Get list of pending tasks"""
        return [t for t in self.tasks if not t.completed]
    
    @property
    def completed_tasks(self) -> List[Task]:
        """Get list of completed tasks"""
        return [t for t in self.tasks if t.completed]


class StateManager:
    """Manages sprint state persistence"""
    
    def __init__(self, project_root: str = None):
        """
        Args:
            project_root: Optional override for project root
                         If not provided, uses config.PROJECT_ROOT
        """
        if project_root:
            self.project_root = Path(project_root)
            self.agent_dir = self.project_root / ".agent"
            self.sprints_dir = self.project_root / "docs" / "dev" / "sprints"
        else:
            # Use paths from config
            self.project_root = PROJECT_ROOT
            self.agent_dir = AGENT_DIR
            self.sprints_dir = SPRINTS_DIR
        
        self.current_sprint_file = self.agent_dir / "current_sprint.md"
        
    def read_current_sprint(self) -> SprintState:
        """
        Read and parse current sprint state from current_sprint.md
        
        Returns:
            SprintState object
            
        Raises:
            FileNotFoundError: If current_sprint.md doesn't exist
        """
        if not self.current_sprint_file.exists():
            raise FileNotFoundError(
                f"Sprint file not found: {self.current_sprint_file}"
            )
        
        content = self.current_sprint_file.read_text()
        return self._parse_sprint(content)
    
    def _parse_sprint(self, content: str) -> SprintState:
        """Parse markdown content into SprintState"""
        lines = content.strip().split('\n')
        
        # Parse header
        name = lines[0].replace('# Current Sprint:', '').strip()
        
        # Parse objective and status
        objective = ""
        status = SprintStatus.IDLE
        
        for line in lines[1:]:
            if line.startswith('**Objective**:'):
                objective = line.split('**Objective**:', 1)[1].strip()
            elif line.startswith('**Status**:'):
                status_str = line.split('**Status**:', 1)[1].strip()
                try:
                    status = SprintStatus(status_str)
                except ValueError:
                    status = SprintStatus.IDLE
        
        # Parse tasks
        tasks = []
        in_backlog = False
        current_task = None
        current_description = []
        
        for line in lines:
            # Flexible detection of Backlog section (handles emojis)
            if line.startswith('##') and 'Backlog' in line:
                in_backlog = True
                continue
            
            if in_backlog:
                # Stop if we hit a new major section (Level 2 header)
                # But allow Level 3+ headers (###, ####) for grouping
                if line.startswith('## ') and 'Backlog' not in line:
                    break
                    
                if line.strip().startswith('- ['):
                    # Save previous task if any
                    if current_task:
                        current_task.description = "\n".join(current_description).strip()
                        tasks.append(current_task)
                        
                    completed = line.strip().startswith('- [x]')
                    # Handle cases like "- [ ] **Title**"
                    task_name = line.split(']', 1)[1].strip()
                    # clean bold markers if present
                    task_name = task_name.replace('**', '')
                    
                    current_task = Task(name=task_name, completed=completed)
                    current_description = []
                elif current_task:
                    # Append description lines to current task
                    current_description.append(line)
        
        # Save last task
        if current_task:
             current_task.description = "\n".join(current_description).strip()
             tasks.append(current_task)
        
        return SprintState(
            name=name,
            objective=objective,
            status=status,
            tasks=tasks
        )
    
    def update_sprint_status(self, status: SprintStatus):
        """Update sprint status in current_sprint.md"""
        content = self.current_sprint_file.read_text()
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if line.startswith('**Status**:'):
                lines[i] = f'**Status**: {status.value}'
                break
        
        self.current_sprint_file.write_text('\n'.join(lines))
    
    def mark_task_complete(self, task_name: str):
        """Mark a specific task as complete"""
        content = self.current_sprint_file.read_text()
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if task_name in line and line.strip().startswith('- [ ]'):
                lines[i] = line.replace('- [ ]', '- [x]', 1)
                break
        
        self.current_sprint_file.write_text('\n'.join(lines))
    
    
    
    def advance_to_next_sprint(self) -> bool:
        """
        Advance to the next sprint in queue.
        1. Identifies content of current sprint.
        2. Scans docs/dev/sprints/ for matching file.
        3. Finds next file alphabetically.
        4. Overwrites current_sprint.md with next file's content.
        
        Returns:
            True if advanced, False if no more sprints.
        """
        import re
        
        # 1. Identify current from file content (read existing)
        try:
            current_sprint = self.read_current_sprint()
            current_name = current_sprint.name
        except:
            current_name = ""
            
        # 2. List all sprint files
        # We assume standard naming: sprintX_Y_name.md
        if not self.sprints_dir.exists():
            return False
            
        sprint_files = sorted(
            [f for f in self.sprints_dir.glob("*.md") if f.name.startswith("sprint")],
            key=lambda x: x.name
        )
        
        if not sprint_files:
            return False
            
        # 3. Find current index
        current_index = -1
        
        # Heuristic: Try to match by reading the Title inside the files or by filename if known
        # Since we only have the Name from current_sprint.md, we scan files to match the header.
        for i, fpath in enumerate(sprint_files):
            content = fpath.read_text()
            # Extract header
            header_match = re.search(r'# Sprint [0-9.]+: (.*)', content)
            if header_match:
                # Reconstruct full name logic from _parse_sprint
                # Note: _parse_sprint expects '# Current Sprint: ...' but definitions usually just '# Sprint ...' 
                # or maybe they just have '# Sprint 1.3: ...'
                # Let's normalize comparison.
                
                # Check if current_name corresponds to this file
                # current_name from _parse is "Sprint 1.3 (Sprint Queuing)"
                # file header might be "Sprint 1.3: Sprint Queuing"
                
                # Loose matching
                file_title_line = content.split('\n')[0].replace('# ', '').strip()
                
                # If current_sprint.md has "Current Sprint: Sprint 1.3...", 
                # and file has "Sprint 1.3...", we match if we strip "Current Sprint: "
                
                # Let's try to match filename to the "Reference" link in current_sprint.md
                # This is more robust.
                pass
        
        # Robust Match: Look at the "Reference" link in current_sprint.md
        current_content = self.current_sprint_file.read_text()
        match_ref = re.search(r'\[.*\]\(docs/dev/sprints/(.*\.md)\)', current_content)
        
        if match_ref:
            current_filename = match_ref.group(1)
            # SYNC BACK: Update the original file with completed state
            try:
                # We want to save the final state of current_sprint (which is COMPLETED)
                # back to the source file, removing the "Current Sprint: " prefix if present.
                
                # 1. Prepare content to save
                final_state_content = current_content
                if final_state_content.startswith('# Current Sprint: '):
                    final_state_content = final_state_content.replace('# Current Sprint: ', '# ', 1)
                
                # 2. Add verification note or ensure STATUS is COMPLETED
                # (It should be REVIEW from the supervisor loop, but let's encourage completion)
                if '**Status**: REVIEW' in final_state_content:
                     final_state_content = final_state_content.replace('**Status**: REVIEW', '**Status**: COMPLETION')
                
                # 3. Write back to source file
                source_path = self.sprints_dir / current_filename
                if source_path.exists():
                    source_path.write_text(final_state_content)
                    print(f"💾 Synced completion status back to: {current_filename}")
            except Exception as e:
                print(f"⚠️ Failed to sync back sprint state: {e}")

            # Find index of this filename
            for i, fpath in enumerate(sprint_files):
                if fpath.name == current_filename:
                    current_index = i
                    break
        
        # If we couldn't find by ref, try by name (fallback)
        if current_index == -1:
             for i, fpath in enumerate(sprint_files):
                if current_name in fpath.read_text(): # Very loose
                    current_index = i
                    break
        
        # 4. Advance
        next_index = current_index + 1
        if next_index < len(sprint_files):
            next_file = sprint_files[next_index]
            
            # Read new content
            new_content = next_file.read_text()
            
            # Transform content for current_sprint.md
            # 1. Add "Current Sprint: " prefix to title if missing
            lines = new_content.split('\n')
            if lines[0].startswith('# Sprint'):
                lines[0] = lines[0].replace('# Sprint', '# Current Sprint: Sprint')
            
            # 2. Ensure Status is IDLE or PLANNING
            # (Usually definitions are PLANNING)
            
            # 3. Write to current_sprint.md
            final_content = '\n'.join(lines)
            self.current_sprint_file.write_text(final_content)
            
            print(f"⏩ Advanced to next sprint: {next_file.name}")
            return True
            
        print("⏹️ No next sprint found in queue.")
        return False
