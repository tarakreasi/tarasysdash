# 🚀 Quick Start Guide - Sprint Supervisor

## 5-Minute Setup

### 1. Check Dependencies
```bash
cd /home/twantoro/project/taraSlides/.agent/automation

# Pastikan Python 3.12+ installed
python3 --version

# Pastikan virtual environment exists
ls -la .venv/
```

### 2. Activate Environment
```bash
source .venv/bin/activate
```

### 3. Test Installation
```bash
# Run tests
python -m pytest tests/test_supervisor.py -v

# Should show: 11 passed ✅
```

### 4. Check Current Sprint Status
```bash
python supervisor_cli.py status
```

Output expected:
```
Current Sprint: Sprint X.X (Sprint Name)
Objective: ...
Status: ...
Progress: XX.X%

Tasks:
  ✓ Completed Task 1
  ○ Pending Task 2
  ...
```

### 5. Try Approval Engine
```bash
# Test safe command
python supervisor_cli.py approve --command "ls -la"
# Expected: AUTO_APPROVE ✅

# Test dangerous command
python supervisor_cli.py approve --command "rm -rf /"
# Expected: FORBIDDEN 🚫
```

## First Autonomous Run

### Prerequisites
Pastikan ada sprint aktif dengan pending tasks di `.agent/current_sprint.md`:

```markdown
# Current Sprint: Sprint 2.1 (Example)

**Objective**: Build awesome feature
**Status**: IN_PROGRESS

## Backlog
- [x] Task 1 Done
- [ ] Task 2 Pending  👈 This will be picked
- [ ] Task 3 Also Pending
```

### Start Supervisor
```bash
python supervisor_cli.py start
```

Supervisor akan:
1. ✅ Scan sprint state
2. ✅ Pick "Task 2 Pending"
3. ✅ Generate implementation plan
4. ✅ Check approval policy
5. ⚠️  Ask for approval (jika needed) atau auto-run
6. ✅ Execute task
7. ✅ Mark as done
8. ✅ Loop ke task berikutnya

### Expected Flow (Auto-Approved)
```
🚀 SPRINT SUPERVISOR STARTED
================================================
📡 SCANNING sprint state...
Sprint: Sprint 2.1 (Example)
Progress: 33.3%
Pending tasks: 2

📋 Next Task: Task 2 Pending
🧠 Generating implementation plan...
Plan saved to .agent/implementation_plan.md
🔐 Checking approval policy...
  ✓ Task terdefinisi dengan jelas
  ✓ Tidak ada destructive operations
  ✓ Tidak ada external impact
  ✓ Tidak ada akses ke sensitive paths
Decision: AUTO_APPROVE (Risk: low)
✅ APPROVED: Semua safety checks passed

🔨 BUILDING...
🔍 VERIFYING...
✅ Task completed: Task 2 Pending

↻ Returning to SCAN state...
```

### Expected Flow (User Approval Required)
```
📋 Next Task: Deploy to Production
🧠 Generating implementation plan...
🔐 Checking approval policy...
  ✗ External impact found: deploy
Decision: REQUIRE_USER (Risk: medium)
👤 USER APPROVAL REQUIRED
Reason: Plan memiliki external impact (deploy)

============================================
Task: Deploy to Production

Implementation Plan:
[Plan details here...]
============================================

Approve this plan? (yes/no): _
```

## Monitoring

### Real-time Logs
```bash
# Terminal 1: Run supervisor
python supervisor_cli.py start

# Terminal 2: Watch logs
tail -f supervisor.log
```

### Check Progress Anytime
```bash
# Press Ctrl+C di supervisor untuk pause
# Lalu check status
python supervisor_cli.py status
```

### Generate Report
```bash
python supervisor_cli.py report --save
# Saved to .agent/sprint_report.md
```

## Common Scenarios

### Scenario 1: All Auto-Approved (Zero-Touch)
Perfect untuk:
- Bug fixes di safe zones
- Component creation
- Test writing
- Documentation updates

Supervisor akan execute semua tasks tanpa interrupt user! 🎉

### Scenario 2: Mixed (Semi-Auto)
Untuk sprints dengan mix of safe/risky tasks:
- Safe tasks: Auto-approved
- Risky tasks: Ask user
- Destructive: Auto-blocked

User cukup approve yang risky saja.

### Scenario 3: High-Risk Sprint
Sprint dengan banyak risky operations:
- Supervisor akan frequently ask approval
- User tetap in control
- Safety checks tetap jalan

## Safety First! 🛡️

### Auto-Blocked Operations
Ini akan **NEVER** di-auto-approve:
- ❌ `rm -rf`
- ❌ `DROP TABLE`
- ❌ `TRUNCATE`
- ❌ File di `/etc/`, `~/.ssh/`, `.env`
- ❌ `git push` (kecuali user approve)
- ❌ Production deployment

### Safe for Auto-Approve
Ini **AMAN** untuk auto-run:
- ✅ File edits di `./src/`, `./components/`, `./tests/`
- ✅ Read-only commands (`ls`, `cat`, `grep`)
- ✅ Tests (`npm run test`, `npm run lint`)
- ✅ Git commits (local)
- ✅ Documentation updates

## Keyboard Controls

Saat supervisor running:
- `Ctrl+C`: Pause supervisor (enter WAITING_USER state)
- `yes`/`y`: Approve plan
- `no`/`n`: Reject plan

## Next Steps

Setelah comfortable dengan basics:

1. **Customize Approval Policy**: Edit `src/supervisor/approval_engine.py`
2. **Add Custom Tools**: Add tools untuk verification
3. **Multi-Sprint**: Chain multiple sprints
4. **Integration**: Connect dengan CI/CD pipeline

## Troubleshooting

### "No pending tasks"
✅ Current sprint sudah selesai semua
🔧 Update `current_sprint.md` dengan tasks baru

### "Max retries reached"
❌ Task gagal verify 3x
🔧 Check logs, fix manual, lalu restart

### "Ollama connection failed"
❌ Ollama service not running
🔧 Start: `ollama serve`

### ImportError
❌ Dependencies not installed
🔧 `pip install -e .`

## Get Help

1. Check logs: `cat supervisor.log`
2. Read protocol: `cat .agent/automation/supervisor_protocol.md`
3. Full docs: `cat README_SUPERVISOR.md`

---

**Ready to go autonomous? 🚀**

```bash
python supervisor_cli.py start
```
