---
description: Special Role for Root Cause Analysis (RCA) and systematic bug fixing
---
# 🕵️‍♀️ `/agent-debug` Workflow (The Detective)

This is a **Special Operations** role. Its goal is not just to fix the bug, but to understand **WHY** it happened and ensure it never happens again.

**Philosophy**: "If you can't reproduce it, you can't fix it."

---

## 🛑 The Golden Rule
**NEVER** apply a fix without a failing test case (Reproduction Script) first.

---

## Steps

### 1️⃣ The Reproduction (The "red" Phase)

Before touching source code, you must prove the bug exists.

**Action**: Create `tests/reproduce_issue_[ID].py`.
```python
# reproduction_script.py
# Goal: This script MUST fail if the bug is present.
def test_bug_scenario():
    result = buggy_function()
    assert result == "Correct", f"Expected Correct, got {result}"
```

**Constraint**: If you cannot create a reproduction script, you are not allowed to proceed to Step 2. Stop and ask the user for more logs.

### 2️⃣ The Analysis (Root Cause Analysis - RCA)

Use the **5 Whys** method to dig deep. Document this in `docs/debugging/incident_[ID].md`.

**Run Librarian**:
```bash
uv run python .agent/workflows/automation/scripts/ask_librarian.py "Show me recent changes to [Module] and any related known issues."
```

**Create Incident Report**:
```markdown
# Incident: [Bug Name]
**Date**: YYYY-MM-DD
**Severity**: High/Medium/Low

## 1. The Symptom
[What did the user see? e.g., "500 Error on Login"]

## 2. The Reproduction
- Script: `tests/reproduce_issue_123.py`
- Confirmed Failure: ✅ Yes

## 3. Root Cause Analysis (5 Whys)
1. **Why?** Login failed with 500. -> *Because UserID was null.*
2. **Why?** UserID was null. -> *Because Session wasn't initialized.*
3. **Why?** Session failing. -> *Because Redis connection timeout.*
4. **Why?** Redis timeout. -> *Because config pointed to wrong port.*
5. **ROOT CAUSE**: Environment variable `REDIS_PORT` is hardcoded in `config.py`.

## 4. Proposed Fix
- Move `REDIS_PORT` to `.env`.
- Update `config.py` to use `os.getenv`.
```

### 3️⃣ The Fix (The "Green" Phase)

**Action**: Implement the solution defined in the RCA.
- **Rule**: Minimal changes. Do not refactor unrelated code.

### 4️⃣ The Verification

**Action**: Run the reproduction script again.
```bash
python tests/reproduce_issue_[ID].py
```
- **Pass**: ✅.
- **Fail**: ❌ Go back to Step 2.

### 5️⃣ The Regression Check

**Action**: Run the full test suite.
```bash
uv run pytest
```
- Ensure we didn't break anything else.

---

## 🔗 Handoff

Once fixed:
- **Git Commit**: `fix: [Bug Name] (closes #[ID])`
- **Cleanup**: You may delete the reproduction script OR promote it to a permanent regression test in `tests/`.

---

## Trigger
- **User**: "/agent-debug Login is broken"
- **Supervisor**: (Auto-triggers on Verification Failure during a sprint)
