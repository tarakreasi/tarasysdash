---
description: Use proactively to eliminate technical debt, improve performance, and enforce standards
---
# 🧹 `/agent-optimizer` Workflow (The Boy Scout)

This workflow is dedicated to **Maintenance & Improvement**. It changes the *structure* of code without changing its *behavior*.

**Philosophy**: "Leave the code better than you found it."

---

## 🎯 When to Use
- A file has grown too large (>300 lines).
- Variable names are confusing (e.g., `x`, `data`).
- Logic is duplicated across multiple files (DIY principle).
- Performance is slow (need to introduce caching/async).
- You are not fixing a bug, you are preventing future ones.

---

## Steps

### 1️⃣ The Baseline (Safety Net)

**Rule**: You cannot refactor code that doesn't have tests.

**Action**: Run the existing tests for the target module.
```bash
uv run pytest tests/test_[module].py
```
- **If Pass**: Proceed.
- **If Fail**: STOP. Run `/agent-debug` to fix it first.
- **If Checksum Missing**: Create a "snapshot test" or "characterization test" to capture current behavior.

### 2️⃣ The Strategy (The "What")

Ask the Librarian for help or rely on `CODING_STANDARDS.md`.

```bash
# Check if we violate standards
uv run python .agent/workflows/automation/scripts/ask_librarian.py "Review [file] against .agent/rules/CODING_STANDARDS.md. List top 3 refactoring opportunities."
```

Create `docs/optimization/plan_[ID].md`:
```markdown
# Optimization Plan: [Module Name]

## Goal
[e.g., Reduce Complexity / Improve Naming / Extract Class]

## Proposed Changes
1. Rename `process_data` to `calculate_monthly_revenue` (Clarity).
2. Extract the SQL query builder into `QueryBuilder` class (SRP).
3. Type hint all functions (Safety).

## Risk Assessment
- **High**: Changing the public API signature? (Avoid if possible)
- **Low**: Internal implementation details only.
```

### 3️⃣ The Refactor (The "Clean" Phase)

**Action**: Apply the changes iteratively.
- **Atomic Commits**: Do one type of refactor at a time (e.g., Rename first, then Extract).

### 4️⃣ The Verification (Regression Check)

**Action**: Run the tests again.
```bash
uv run pytest tests/test_[module].py
```
- **Must Pass**: If it fails, you broke behavior. Revert and try again.

---

## 🔗 Handoff

Once optimized:
- **Git Commit**: `refactor: [What changed] (debt reduction)`
- **Update**: If you changed function signatures, update the `Spec` and `Librarian Index`.

---

## Trigger
- **User**: "/agent-optimizer Clean up `auth_service.py`"
- **Supervisor**: (Auto-triggers if Cyclomatic Complexity > 10)
