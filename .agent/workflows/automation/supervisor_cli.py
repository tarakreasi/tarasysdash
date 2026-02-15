#!/usr/bin/env python3
"""
Sprint Supervisor CLI
Entry point untuk menjalankan automation supervisor
"""
import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.supervisor.supervisor import SprintSupervisor
from src.supervisor.state_manager import StateManager
from src.core.json_logger import JSONLogger

# Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'


def print_banner():
    """Print supervisor banner"""
    banner = f"""{CYAN}{BOLD}
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        🤖  SPRINT AUTOMATION SUPERVISOR  🤖              ║
║                                                           ║
║     Python-Based Autonomous Sprint Execution Engine      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
{RESET}"""
    print(banner)


def cmd_start(args):
    """Start continuous sprint execution"""
    logger = None
    if args.json:
        # Use JSON Logger
        logger = JSONLogger("supervisor")
    else:
        # Standard human-readable banner
        print_banner()
        print(f"\n{YELLOW}Starting continuous sprint execution...{RESET}\n")
    
    # Pass logger to supervisor (assuming we update Supervisor to accept it or rely on existing logging if None)
    # Since SprintSupervisor handles its own logging setup, we might need to inject this or patch it.
    # For now, let's update SprintSupervisor to accept an optional logger override, 
    # OR we just rely on standard output capture if we are External Agent.
    
    # Actually, the requirement is for the CLI to output JSON. 
    # If the Supervisor class prints to stdout, we need to intercept that or configure it.
    # Let's assume we will pass `json_mode=True` to Supervisor in a future refactor, 
    # but for Micro-Sprint 1.2, let's just ensure the CLI respects the flag if possible.
    
    # NOTE: To fully support this, SprintSupervisor needs to use the JSON logger we create here.
    # We will modify SprintSupervisor to accept `logger` or `json_mode` in the next step/edit.
    # For now, we prepare the CLI.
    
    supervisor = SprintSupervisor(max_retries=args.max_retries, json_mode=args.json)
    
    try:
        supervisor.run_continuous_loop()
    except Exception as e:
        if args.json:
            import json
            print(json.dumps({"status": "FATAL", "error": str(e)}))
        else:
            print(f"\n{RED}Fatal error: {e}{RESET}")
        sys.exit(1)


def cmd_status(args):
    """Show current sprint status"""
    print_banner()
    
    state_manager = StateManager()
    
    try:
        sprint = state_manager.read_current_sprint()
        
        print(f"\n{BOLD}Current Sprint:{RESET} {sprint.name}")
        print(f"{BOLD}Objective:{RESET} {sprint.objective}")
        print(f"{BOLD}Status:{RESET} {sprint.status.value}")
        print(f"{BOLD}Progress:{RESET} {sprint.progress:.1f}%")
        
        print(f"\n{BOLD}Tasks:{RESET}")
        for task in sprint.tasks:
            status = f"{GREEN}✓{RESET}" if task.completed else f"{YELLOW}○{RESET}"
            print(f"  {status} {task.name}")
        
        if sprint.pending_tasks:
            next_task = sprint.pending_tasks[0]
            print(f"\n{BOLD}Next Task:{RESET} {next_task.name}")
        else:
            print(f"\n{GREEN}✅ All tasks completed!{RESET}")
        
    except FileNotFoundError as e:
        print(f"\n{RED}Error: {e}{RESET}")
        sys.exit(1)


def cmd_report(args):
    """Generate sprint report"""
    print_banner()
    
    state_manager = StateManager()
    
    try:
        report = state_manager.create_sprint_report()
        print(report)
        
        if args.save:
            report_file = state_manager.agent_dir / "sprint_report.md"
            report_file.write_text(report)
            print(f"\n{GREEN}Report saved to: {report_file}{RESET}")
    
    except FileNotFoundError as e:
        print(f"\n{RED}Error: {e}{RESET}")
        sys.exit(1)


def cmd_approve(args):
    """Test approval engine"""
    from src.supervisor.approval_engine import ApprovalEngine, ApprovalDecision
    
    print_banner()
    
    engine = ApprovalEngine()
    
    
    # NEW: Handle supervisor interactive approval
    if not args.command and not args.plan_file:
        # Check if we are potentially trying to approve a waiting supervisor
        approved_flag = Path(".agent/automation/.approved")
        if not approved_flag.exists():
            approved_flag.touch()
            print(f"{GREEN}AUTHORIZATION GRANTED.{RESET} Supervisor will resume shortly.")
            return

    if args.command:
        print(f"\n{BOLD}Evaluating command:{RESET} {args.command}\n")
        result = engine.evaluate_command(args.command)
    elif args.plan_file:
        plan_path = Path(args.plan_file)
        if not plan_path.exists():
            print(f"{RED}Plan file not found: {args.plan_file}{RESET}")
            sys.exit(1)
        
        plan_text = plan_path.read_text()
        print(f"\n{BOLD}Evaluating plan from:{RESET} {args.plan_file}\n")
        result = engine.evaluate_plan(plan_text, args.task_name or "")
    else:
        print(f"{RED}Please provide either --command or --plan-file{RESET}")
        sys.exit(1)
    
    # Print result
    decision_color = {
        ApprovalDecision.AUTO_APPROVE: GREEN,
        ApprovalDecision.REQUIRE_USER: YELLOW,
        ApprovalDecision.FORBIDDEN: RED
    }.get(result.decision, RESET)
    
    print(f"{BOLD}Decision:{RESET} {decision_color}{result.decision.value}{RESET}")
    print(f"{BOLD}Reason:{RESET} {result.reason}")
    print(f"{BOLD}Risk Level:{RESET} {result.risk_level}")
    
    if result.checks_passed:
        print(f"\n{BOLD}Checks Passed:{RESET}")
        for check in result.checks_passed:
            print(f"  {GREEN}✓{RESET} {check}")
    
    if result.checks_failed:
        print(f"\n{BOLD}Checks Failed:{RESET}")
        for check in result.checks_failed:
            print(f"  {RED}✗{RESET} {check}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Sprint Automation Supervisor - Python-based autonomous sprint execution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start continuous execution
  python supervisor_cli.py start
  
  # Check current sprint status
  python supervisor_cli.py status
  
  # Generate sprint report
  python supervisor_cli.py report --save
  
  # Test approval for a command
  python supervisor_cli.py approve --command "npm run test"
  
  # Test approval for a plan
  python supervisor_cli.py approve --plan-file .agent/implementation_plan.md --task-name "Create Component"
"""
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Start command
    start_parser = subparsers.add_parser('start', help='Start continuous sprint execution')
    start_parser.add_argument(
        '--max-retries',
        type=int,
        default=3,
        help='Maximum retry attempts for healing (default: 3)'
    )
    start_parser.add_argument(
        '--json',
        action='store_true',
        help='Output logs in JSON format for external agents'
    )
    start_parser.set_defaults(func=cmd_start)
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show current sprint status')
    status_parser.set_defaults(func=cmd_status)
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate sprint report')
    report_parser.add_argument(
        '--save',
        action='store_true',
        help='Save report to file'
    )
    report_parser.set_defaults(func=cmd_report)
    
    # Approve command
    approve_parser = subparsers.add_parser('approve', help='Test approval engine')
    approve_parser.add_argument(
        '--command',
        type=str,
        help='Shell command to evaluate'
    )
    approve_parser.add_argument(
        '--plan-file',
        type=str,
        help='Path to implementation plan file'
    )
    approve_parser.add_argument(
        '--task-name',
        type=str,
        help='Task name (for plan evaluation)'
    )
    approve_parser.set_defaults(func=cmd_approve)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Execute command
    args.func(args)


if __name__ == '__main__':
    main()
