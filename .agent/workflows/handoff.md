---
description: Protocol for AI-to-AI Session Handoff
---

# 🔄 Handoff Protocol (`/handoff`)

This workflow ensures smooth transitions between AI agents working on the same project.

## When to Use This Workflow

- End of work session (human going offline)
- Switching AI agents (different model/provider)
- Context window exhausted
- Major milestone completion

## Handoff Checklist

### Phase 1: Document Current State
- [ ] Create/Update `SESSION_HANDOFF.md` with:
  - Current sprint status
  - Recent achievements
  - Known issues
  - File structure overview
  - Critical decisions made

### Phase 2: Sync All Changes
```bash
# Sync toolkit
rsync -av --update --delete new_agent/ .agent/

# Commit everything
git add -A
git commit -m "chore: Session handoff - [brief status]"
git status  # Verify clean
```

### Phase 3: Prepare Next Steps
- [ ] Identify next sprint/task clearly
- [ ] Document any blockers or dependencies
- [ ] List files next agent should read first

### Phase 4: Validation
```bash
# Verify toolkit still works
cd new_agent/automation
.venv/bin/python -m pytest tests/ -v

# Check supervisor can start
.venv/bin/python supervisor_cli.py status
```

## Handoff Document Template

```markdown
# Session Handoff - [DATE]

## Current Status
- Active Sprint: [Sprint X.Y - Name]
- Status: [PLANNING | IN_PROGRESS | COMPLETED]
- Git HEAD: [commit hash]

## Recent Work
- [Bullet points of what was accomplished]

## Next Steps
1. [Immediate next task]
2. [Following task]

## Blockers/Notes
- [Any issues or important context]

## How to Resume
1. Read [file1.md]
2. Run [command]
3. Continue with [task]
```

## For Incoming Agent

### Quick Start
1. **Read**: `SESSION_HANDOFF.md` (always start here)
2. **Verify**: Run `git log -1` and `git status`
3. **Understand**: Read indicated sprint file
4. **Execute**: Follow documented next steps

### If Confused
Priority read order:
1. `SESSION_HANDOFF.md` - Current state
2. `.agent/workflows/agent.md` - Your role
3. `SPRINT_GUIDE.md` - How sprints work
4. Current sprint file in `docs/dev/sprints/`

## Best Practices

### DO:
- Always sync and commit before handoff
- Document WHY decisions were made, not just WHAT
- List files modified in commit message
- Update CHANGELOG for major milestones

### DON'T:
- Leave uncommitted changes
- Skip documentation updates
- Assume next agent has your context
- Forget to test before handoff

## Integration with Toolkit

This handoff protocol is part of the core toolkit workflow system:
- **Trigger**: Manual (human-initiated)
- **Outputs**: `SESSION_HANDOFF.md`, git commit
- **Consumer**: Next AI agent or human developer
