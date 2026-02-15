#!/usr/bin/env python3
"""
Demo Script - Sprint Supervisor
Menunjukkan cara kerja approval engine dengan berbagai skenario
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.supervisor.approval_engine import ApprovalEngine, ApprovalDecision

# Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'


def print_header(title):
    print(f"\n{CYAN}{BOLD}{'='*60}")
    print(f"{title:^60}")
    print(f"{'='*60}{RESET}\n")


def print_result(result):
    decision_color = {
        ApprovalDecision.AUTO_APPROVE: GREEN,
        ApprovalDecision.REQUIRE_USER: YELLOW,
        ApprovalDecision.FORBIDDEN: RED
    }.get(result.decision, RESET)
    
    print(f"{BOLD}Decision:{RESET} {decision_color}{result.decision.value}{RESET}")
    print(f"{BOLD}Reason:{RESET} {result.reason}")
    print(f"{BOLD}Risk:{RESET} {result.risk_level}\n")
    
    if result.checks_passed:
        print(f"{GREEN}Checks Passed:{RESET}")
        for check in result.checks_passed:
            print(f"  ✓ {check}")
    
    if result.checks_failed:
        print(f"\n{RED}Checks Failed:{RESET}")
        for check in result.checks_failed:
            print(f"  ✗ {check}")


def demo_commands():
    """Demo approval untuk berbagai commands"""
    print_header("DEMO 1: Command Approval")
    
    engine = ApprovalEngine()
    
    test_cases = [
        ("ls -la", "List files (safe)"),
        ("npm run test", "Run tests (safe)"),
        ("git push origin main", "Push to remote (external impact)"),
        ("rm -rf /tmp/cache", "Delete temp (destructive)"),
        ("cat /etc/passwd", "Read sensitive file (forbidden)"),
        ("npm install express", "Install dependency (should ask)"),
    ]
    
    for command, description in test_cases:
        print(f"{BOLD}Command:{RESET} {command}")
        print(f"{BOLD}Description:{RESET} {description}")
        result = engine.evaluate_command(command)
        print_result(result)
        print("-" * 60)


def demo_plans():
    """Demo approval untuk berbagai implementation plans"""
    print_header("DEMO 2: Plan Approval")
    
    engine = ApprovalEngine()
    
    # Plan 1: Safe component creation
    plan1 = """
# Implementation Plan: Create Button Component

Create a new reusable Button component.

Steps:
1. Create file: ./components/Button.vue
2. Add template with props (label, variant, onClick)
3. Add styling with CSS modules
4. Create unit test: ./tests/Button.test.js
5. Update component index: ./components/index.js

All files in safe zone (./components/, ./tests/)
Changes tracked in Git
No external dependencies needed
No destructive operations
"""
    
    print(f"{BOLD}Scenario:{RESET} Create Safe Component\n")
    print(plan1)
    result = engine.evaluate_plan(plan1, "Create Button Component")
    print_result(result)
    print("-" * 60)
    
    # Plan 2: Database migration (risky)
    plan2 = """
# Implementation Plan: Migrate Database

Migrate database schema to new version.

Steps:
1. Create migration file
2. Run: php artisan migrate:fresh
3. Seed new data
4. Update models
"""
    
    print(f"{BOLD}Scenario:{RESET} Database Migration (Risky)\n")
    print(plan2)
    result = engine.evaluate_plan(plan2, "Migrate Database")
    print_result(result)
    print("-" * 60)
    
    # Plan 3: Ambiguous plan
    plan3 = "Maybe we should probably do something with the API endpoint?"
    
    print(f"{BOLD}Scenario:{RESET} Ambiguous Plan\n")
    print(plan3)
    result = engine.evaluate_plan(plan3, "Fix API")
    print_result(result)
    print("-" * 60)


def demo_safety_boundaries():
    """Demo safety boundaries"""
    print_header("DEMO 3: Safety Boundaries")
    
    engine = ApprovalEngine()
    
    print(f"{GREEN}{BOLD}✅ SAFE ZONES (Auto-Approved):{RESET}")
    safe_operations = [
        "./app/Components/Button.php",
        "./resources/views/home.blade.php",
        "./tests/Feature/AuthTest.php",
        "npm run test",
        "git commit -m 'Add feature'",
    ]
    
    for op in safe_operations:
        print(f"  ✓ {op}")
    
    print(f"\n{RED}{BOLD}🚫 FORBIDDEN ZONES:{RESET}")
    forbidden_operations = [
        "/etc/hosts",
        "~/.ssh/id_rsa",
        ".env (credential files)",
        "rm -rf (destructive)",
        "DROP TABLE (data loss)",
    ]
    
    for op in forbidden_operations:
        print(f"  ✗ {op}")
    
    print(f"\n{YELLOW}{BOLD}⚠️  REQUIRE USER APPROVAL:{RESET}")
    require_user = [
        "git push (external)",
        "npm install (dependencies)",
        "Deploy to production",
        "Send emails/notifications",
        "Modify root configs (webpack, vite)",
    ]
    
    for op in require_user:
        print(f"  ⚠  {op}")


def demo_decision_tree():
    """Show decision tree flowchart"""
    print_header("DEMO 4: Decision Tree")
    
    flowchart = f"""
{CYAN}┌─────────────────────────────────────────┐
│  New Task from Sprint Backlog           │
└──────────────┬──────────────────────────┘
               │
               ▼
{YELLOW}┌─────────────────────────────────────────┐
│  Generate Implementation Plan           │
└──────────────┬──────────────────────────┘
               │
               ▼
       ┌───────┴────────┐
       │ Check Approval │
       └───────┬────────┘
               │
       ┌───────┴────────┐
       │                │
       ▼                ▼
{RED}  FORBIDDEN    {YELLOW}REQUIRE_USER{RESET}      {GREEN}AUTO_APPROVE{RESET}
       │                │                 │
       ▼                ▼                 ▼
{RED}   HALT          {YELLOW}Ask User        {GREEN}Execute{RESET}
                       │                 │
                   ┌───┴───┐             ▼
                   ▼       ▼         {CYAN}Verify{RESET}
                {GREEN}YES{RESET}     {RED}NO{RESET}          │
                   │       │         ┌───┴───┐
                   │       ▼         ▼       ▼
                   │   {RED}HALT{RESET}    {GREEN}PASS{RESET}   {RED}FAIL{RESET}
                   │               │       │
                   ▼               ▼       ▼
               {CYAN}Execute{RESET}      {GREEN}Mark Done{RESET} {YELLOW}Retry{RESET}
                   │               │
                   ▼               ▼
               {CYAN}Verify{RESET}       {BOLD}NEXT TASK{RESET}
    """
    
    print(flowchart)


def main():
    """Run all demos"""
    print(f"""
{CYAN}{BOLD}
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     🎬  SPRINT SUPERVISOR - APPROVAL DEMO  🎬            ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
{RESET}
    """)
    
    demo_commands()
    input(f"\n{BOLD}Press Enter to continue to Plan Demo...{RESET}")
    
    demo_plans()
    input(f"\n{BOLD}Press Enter to continue to Safety Boundaries...{RESET}")
    
    demo_safety_boundaries()
    input(f"\n{BOLD}Press Enter to see Decision Tree...{RESET}")
    
    demo_decision_tree()
    
    print(f"\n{GREEN}{BOLD}Demo Complete! ✅{RESET}")
    print(f"\n{CYAN}Try it yourself:{RESET}")
    print(f"  python supervisor_cli.py approve --command \"npm run test\"")
    print(f"  python supervisor_cli.py start\n")


if __name__ == '__main__':
    main()
