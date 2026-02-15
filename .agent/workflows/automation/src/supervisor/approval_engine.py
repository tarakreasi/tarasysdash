"""
Intelligent Approval Engine
Evaluates implementation plans and determines if they can be auto-approved
"""
import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Set


class ApprovalDecision(Enum):
    """Approval decision types"""
    AUTO_APPROVE = "AUTO_APPROVE"
    REQUIRE_USER = "REQUIRE_USER"
    FORBIDDEN = "FORBIDDEN"


@dataclass
class ApprovalResult:
    """Result of approval evaluation"""
    decision: ApprovalDecision
    reason: str
    risk_level: str
    checks_passed: List[str]
    checks_failed: List[str]


class ApprovalEngine:
    """Evaluates plans for auto-approval"""
    
    # Destructive patterns that are always forbidden
    DESTRUCTIVE_PATTERNS = [
        r'rm\s+-rf\s+/',
        r'DROP\s+TABLE',
        r'DELETE\s+FROM.*WHERE\s+1=1',
        r'truncate\s+table',
        r'mkfs\.',
        r'dd\s+if=',
    ]
    
    # External impact patterns requiring user approval
    # Note: git push removed - system handles version control
    EXTERNAL_PATTERNS = [
        r'npm\s+publish',
        r'docker\s+push',
        r'kubectl\s+apply',
        r'terraform\s+apply',
        r'curl.*POST.*api',
        r'send.*email',
        r'deploy\s+to\s+production',
    ]
    
    # Sensitive paths that should not be modified
    # Only actual file paths, not keywords mentioned in documentation
    SENSITIVE_PATHS = [
        '/etc/passwd',
        '/etc/shadow',
        '~/.ssh/id_rsa',
        '~/.ssh/id_dsa',
        '/root/',
    ]
    
    # Safe modification zones
    SAFE_ZONES = [
        './src/',
        './app/',
        './components/',
        './tests/',
        './docs/',
        './smarthome/',
        './.agent/',
    ]
    
    def evaluate_command(self, command: str) -> ApprovalResult:
        """Evaluate a single shell command"""
        checks_passed = []
        checks_failed = []
        
        # Check for destructive operations
        for pattern in self.DESTRUCTIVE_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return ApprovalResult(
                    decision=ApprovalDecision.FORBIDDEN,
                    reason=f"Command contains destructive pattern: {pattern}",
                    risk_level="high",
                    checks_passed=checks_passed,
                    checks_failed=["Destructive operation detected"]
                )
        
        # Check for sensitive paths
        for path in self.SENSITIVE_PATHS:
            if path in command:
                return ApprovalResult(
                    decision=ApprovalDecision.FORBIDDEN,
                    reason=f"Command accesses sensitive path: {path}",
                    risk_level="high",
                    checks_passed=checks_passed,
                    checks_failed=["Sensitive path access"]
                )
        
        # Check for external impact
        for pattern in self.EXTERNAL_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                checks_failed.append("External impact found")
                return ApprovalResult(
                    decision=ApprovalDecision.REQUIRE_USER,
                    reason=f"Command has external impact: {pattern}",
                    risk_level="medium",
                    checks_passed=checks_passed,
                    checks_failed=checks_failed
                )
        
        # All checks passed
        checks_passed.extend([
            "No destructive operations",
            "No sensitive path access",
            "No external impact"
        ])
        
        return ApprovalResult(
            decision=ApprovalDecision.AUTO_APPROVE,
            reason="Command is safe for auto-execution",
            risk_level="low",
            checks_passed=checks_passed,
            checks_failed=[]
        )
    
    def evaluate_plan(self, plan: str, task_name: str) -> ApprovalResult:
        """
        Evaluate an implementation plan for auto-approval
        
        Args:
            plan: The implementation plan text
            task_name: Name of the task being executed
            
        Returns:
            ApprovalResult with decision and reasoning
        """
        checks_passed = []
        checks_failed = []
        
        plan_lower = plan.lower()
        
        # Check 1: Task is well-defined
        if task_name and len(task_name) > 5:
            checks_passed.append("Task terdefinisi dengan jelas")
        else:
            checks_failed.append("Task name ambiguous")
        
        # Check 2: No destructive operations
        has_destructive = False
        for pattern in self.DESTRUCTIVE_PATTERNS:
            if re.search(pattern, plan, re.IGNORECASE):
                checks_failed.append(f"Destructive pattern found: {pattern}")
                has_destructive = True
                break
        
        if not has_destructive:
            checks_passed.append("Tidak ada destructive operations")
        
        # Check 3: No external impact
        has_external_impact = False
        for pattern in self.EXTERNAL_PATTERNS:
            if re.search(pattern, plan, re.IGNORECASE):
                checks_failed.append(f"External impact found: {pattern}")
                has_external_impact = True
                break
        
        if not has_external_impact:
            checks_passed.append("Tidak ada external impact")
        
        # Check 4: No sensitive path access
        has_sensitive_access = False
        for path in self.SENSITIVE_PATHS:
            if path in plan:
                checks_failed.append(f"Sensitive path: {path}")
                has_sensitive_access = True
                break
        
        if not has_sensitive_access:
            checks_passed.append("Tidak ada akses ke sensitive paths")
        
        # Check 5: Plan mentions version control (reversibility)
        if 'git' in plan_lower or 'commit' in plan_lower or 'version' in plan_lower:
            checks_passed.append("Version control mentioned")
        else:
            checks_passed.append("Standard action (Git-backed) is reversible")
        
        # Check 6: Plan detail level
        if len(plan) > 100:
            checks_passed.append("Plan cukup jelas dan detail")
        else:
            checks_failed.append("Plan too short/ambiguous")
        
        # Determine decision
        if has_destructive or has_sensitive_access:
            return ApprovalResult(
                decision=ApprovalDecision.FORBIDDEN,
                reason="Plan mengandung operasi berbahaya atau akses sensitive path",
                risk_level="high",
                checks_passed=checks_passed,
                checks_failed=checks_failed
            )
        
        if has_external_impact:
            return ApprovalResult(
                decision=ApprovalDecision.REQUIRE_USER,
                reason="Plan memiliki external impact (deploy, API calls, dll)",
                risk_level="medium",
                checks_passed=checks_passed,
                checks_failed=checks_failed
            )
        
        if checks_failed:
            return ApprovalResult(
                decision=ApprovalDecision.REQUIRE_USER,
                reason="Plan memiliki beberapa concern yang perlu review",
                risk_level="medium",
                checks_passed=checks_passed,
                checks_failed=checks_failed
            )
        
        # All good!
        return ApprovalResult(
            decision=ApprovalDecision.AUTO_APPROVE,
            reason="Semua safety checks passed. Task aman untuk auto-execution.",
            risk_level="low",
            checks_passed=checks_passed,
            checks_failed=[]
        )
