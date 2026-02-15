# 🔗 Integration Guide - Sprint Supervisor dengan Workflows

## Overview

Sprint Supervisor di-design untuk integrate seamlessly dengan existing workflows:
- `/continuous_sprint` - Autonomous loop execution
- `/micro_sprint_protocol` - High-precision micro-sprint execution
- `/self-healing` - Autonomous debugging loop

Document ini menjelaskan cara menggunakan Python Supervisor sebagai replacement/enhancement untuk script-based automation.

## Migration Path

### Old Way (PHP Scripts)
```bash
# Manual workflow execution
php .agent/automation/scripts/scan_tasks.php
# Output: "Create Component X"

# Manually create implementation_plan.md
# Manually execute plan
# Manually verify
# Manually update task status

php .agent/automation/scripts/update_task.php "Create Component X"
```

### New Way (Python Supervisor)
```bash
# Fully automated
python supervisor_cli.py start

# Supervisor automatically:
# 1. Scans tasks
# 2. Generates plan
# 3. Checks approval
# 4. Executes (future: with agent)
# 5. Verifies
# 6. Updates status
# 7. Loops
```

## Using with `/continuous_sprint` Workflow

### Current Workflow Definition
Location: `.agent/workflows/continuous_sprint.md`

**Old approach** - Manual steps dengan PHP scripts  
**New approach** - Single command with Python supervisor

### Step-by-Step Replacement

#### Old Step 1: SCAN
```bash
# Old
php .agent/automation/scripts/scan_tasks.php
```

#### New Step 1: SCAN
```python
# Python Supervisor (internal)
state_manager = StateManager()
sprint = state_manager.read_current_sprint()
next_task = state_manager.get_next_task()
```

**For manual usage:**
```bash
python supervisor_cli.py status
```

---

#### Old Step 2-5: Manual Execution
Sebelumnya memerlukan manual intervention di setiap step.

#### New Step 2-5: Automated
```bash
# Single command runs entire loop
python supervisor_cli.py start
```

Supervisor automatically:
- ✅ Plans task
- ✅ Checks approval
- ✅ Executes (when agent integrated)
- ✅ Verifies
- ✅ Updates status

---

## Using with `/micro_sprint_protocol`

### Protocol Integration

Micro Sprint Protocol structure:
```
Definition → Plan → Build → Verify
```

Python Supervisor implements sama exact flow:
```python
SCANNING → PLANNING → BUILDING → VERIFYING → REVIEW
```

### Usage Pattern

#### For Micro-Sprint Execution

**Manual micro-sprint:**
```bash
# Read micro-sprint definition
cat docs/sprints/micro/sprint_2.1a.md

# Execute dengan supervisor
python supervisor_cli.py start
```

Supervisor akan:
1. Read sprint backlog dari `current_sprint.md`
2. Execute tasks satu per satu
3. Each task follows: Plan → Build → Verify
4. Auto-mark done when verified

#### For Micro-Sprint Chain

Execute multiple micro-sprints in sequence:

```bash
# Update current_sprint.md to point to micro-sprint
# Run supervisor
python supervisor_cli.py start

# When done, update to next micro-sprint
# Run again
```

**Future enhancement**: Auto-chain micro-sprints

---

## Using with `/self-healing` Workflow

### Self-Healing Integration

Workflow: Run → Fail → Patch → Repeat

Supervisor implements self-healing di **HEALING state**:

```python
STATE: VERIFYING
    ↓ FAIL
STATE: HEALING
    - Read error logs
    - Generate fix proposal
    - Apply fix
    ↓
STATE: VERIFYING (retry)
```

### Configuration

```python
# In supervisor
max_retries = 3  # Default

# Custom retries
python supervisor_cli.py start --max-retries 5
```

### Healing Flow

1. **Task fails verification**
   ```
   🔍 VERIFYING...
   ❌ Tests failed: Button.test.js
   Entering HEALING state (Attempt 1/3)
   ```

2. **Auto-healing attempted**
   ```
   🔧 HEALING...
   Reading error logs...
   Generating fix proposal...
   Applying fix...
   ```

3. **Re-verify**
   ```
   🔍 VERIFYING (retry 1)...
   ✅ Tests passed!
   ```

---

## Advanced Integration Patterns

### Pattern 1: Supervisor as Background Service

Run supervisor as daemon untuk continuous monitoring:

```bash
# Terminal 1: Run supervisor
cd .agent/automation
source .venv/bin/activate
python supervisor_cli.py start > supervisor_output.log 2>&1 &

# Terminal 2: Update sprint tasks live
vim .agent/current_sprint.md
# Add new task → Supervisor auto-picks it up on next loop
```

### Pattern 2: Hybrid Manual + Auto

Selective automation:

```bash
# Check what's pending
python supervisor_cli.py status

# Let supervisor handle safe tasks automatically
python supervisor_cli.py start

# Supervisor will:
# - Auto-execute safe tasks
# - Pause and ask for risky tasks
# - You approve/reject interactively
```

### Pattern 3: Pre-flight Checks

Before starting sprint, validate approval:

```bash
# Test all tasks for approval
cat .agent/implementation_plan.md | while read task; do
  python supervisor_cli.py approve --task-name "$task"
done

# If all auto-approve, run fully autonomous
python supervisor_cli.py start
```

### Pattern 4: Monitoring Dashboard

Real-time monitoring during execution:

```bash
# Terminal 1: Supervisor
python supervisor_cli.py start

# Terminal 2: Live logs
tail -f .agent/automation/supervisor.log | grep "SUCCESS\|ERROR\|APPROVAL"

# Terminal 3: Progress tracking
watch -n 5 'python supervisor_cli.py status'
```

---

## Custom Workflow Creation

### Creating Supervisor-Compatible Workflow

Format workflow markdown dengan annotations:

```markdown
---
description: "My Custom Workflow"
---

# Custom Sprint Workflow

## Step 1: Prepare
// supervisor-auto
Check environment readiness.

## Step 2: Execute
// supervisor-manual
User approval required.

## Step 3: Verify
// supervisor-auto
Run tests and verification.
```

Annotations:
- `// supervisor-auto`: Auto-approved by supervisor
- `// supervisor-manual`: Always ask user
- `// supervisor-skip`: Skip in autonomous mode

### Execute Custom Workflow

```bash
# Point current_sprint to custom workflow
echo "- [ ] Step 1: Prepare" >> .agent/current_sprint.md
echo "- [ ] Step 2: Execute" >> .agent/current_sprint.md
echo "- [ ] Step 3: Verify" >> .agent/current_sprint.md

# Run
python supervisor_cli.py start
```

---

## Environment Variables

Configure supervisor behavior via environment:

```bash
# Max retries for healing
export SUPERVISOR_MAX_RETRIES=5

# Auto-approve all (dangerous! only for dev)
export SUPERVISOR_AUTO_APPROVE_ALL=true

# Require user for all (safe mode)
export SUPERVISOR_REQUIRE_USER_ALL=true

# Log level
export SUPERVISOR_LOG_LEVEL=DEBUG

# Run supervisor
python supervisor_cli.py start
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Autonomous Sprint
on:
  workflow_dispatch:
    inputs:
      sprint_name:
        description: 'Sprint to execute'
        required: true

jobs:
  execute-sprint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      
      - name: Install Dependencies
        run: |
          cd .agent/automation
          pip install -e .
      
      - name: Run Sprint Supervisor
        run: |
          cd .agent/automation
          # In CI, use auto-approve for safe tasks only
          export SUPERVISOR_MAX_RETRIES=3
          python supervisor_cli.py start
      
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: sprint-report
          path: .agent/sprint_report.md
```

---

## API Integration (Future)

Plan untuk REST API wrapper:

```python
# Future: supervisor_api.py
from fastapi import FastAPI
from supervisor import SprintSupervisor

app = FastAPI()

@app.post("/sprint/start")
async def start_sprint():
    supervisor = SprintSupervisor()
    supervisor.run_continuous_loop()
    return {"status": "running"}

@app.get("/sprint/status")
async def get_status():
    state = StateManager().read_current_sprint()
    return {
        "name": state.name,
        "progress": state.progress,
        "pending": len(state.pending_tasks)
    }
```

Usage:
```bash
# Start API server
uvicorn supervisor_api:app

# Trigger sprint from anywhere
curl -X POST http://localhost:8000/sprint/start

# Check status
curl http://localhost:8000/sprint/status
```

---

## Troubleshooting Integration Issues

### Issue: Supervisor tidak pick up new tasks

**Cause**: Sprint state tidak di-refresh  
**Fix**:
```bash
# Ensure current_sprint.md is updated
cat .agent/current_sprint.md

# Restart supervisor
python supervisor_cli.py start
```

### Issue: Approval policy terlalu strict/loose

**Cause**: Default policy mungkin tidak sesuai project  
**Fix**: Customize `src/supervisor/approval_engine.py`

```python
# Add custom safe zones
SAFE_ZONES = [
    './app/',
    './custom_dir/',  # Add your safe directory
]

# Add custom safe commands
safe_commands = [
    'npm run custom-script',  # Add your safe command
]
```

### Issue: Integration dengan existing scripts

**Cause**: PHP scripts masih dipanggil  
**Fix**: Gradually migrate

**Phase 1**: Run both side-by-side
```bash
# Old way still works
php .agent/automation/scripts/scan_tasks.php

# New way also works
python supervisor_cli.py status
```

**Phase 2**: Replace PHP calls in workflows
```bash
# Update .agent/workflows/*.md
# Replace: php .agent/automation/scripts/...
# With: python supervisor_cli.py ...
```

**Phase 3**: Full migration
```bash
# Deprecate PHP scripts
# Use only Python supervisor
```

---

## Best Practices

### 1. Start Small
```bash
# First sprint: Use manual approval
export SUPERVISOR_REQUIRE_USER_ALL=true
python supervisor_cli.py start

# When confident: Enable auto-approve for safe tasks
unset SUPERVISOR_REQUIRE_USER_ALL
python supervisor_cli.py start
```

### 2. Monitor First Runs
```bash
# Watch logs closely for first few sprints
tail -f supervisor.log

# Check approval decisions
grep "APPROVAL" supervisor.log
```

### 3. Customize for Your Project
```python
# Adjust safety policies
# Edit: src/supervisor/approval_engine.py

# Add project-specific safe zones
# Add project-specific safe commands
```

### 4. Backup Before Autonomous Runs
```bash
# Always commit before autonomous run
git add .
git commit -m "Pre-autonomous sprint backup"

# Run supervisor
python supervisor_cli.py start

# If something wrong, easy rollback
git reset --hard HEAD^
```

---

## Summary

**Sprint Supervisor** seamlessly integrates dengan existing workflow system:

✅ **Drop-in Replacement**: Untuk PHP-based automation scripts  
✅ **Workflow Compatible**: Works dengan `/continuous_sprint`, `/micro_sprint_protocol`  
✅ **Hybrid Mode**: Can run manual or fully autonomous  
✅ **Safe by Default**: Built-in protection dengan user override  
✅ **Extensible**: Easy to customize untuk specific project needs  

**Next Steps:**
1. Try first autonomous run: `python supervisor_cli.py start`
2. Monitor behavior & adjust policies
3. Gradually enable more automation
4. Eventually: Zero-touch sprint execution! 🚀
