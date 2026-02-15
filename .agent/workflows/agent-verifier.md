---
description: Verify the end-to-end implementation of a spec against quality gates
---
# 🛡️ `/agent-verifier` Workflow (The Quality Gate)

Use this workflow to comprehensively verify a sprint or feature **BEFORE** marking it as DONE. This acts as the automated Quality Assurance (QA) layer.

## 📋 Manifest
- **Input**: Implemented Code (`src/`, `tests/`)
- **Output**: `docs/verification/report_*.md`
- **Next Step**: Merge / Deploy

---

## 🧱 Gate 0: Sprint Artifact Validation (Pre-Execution)

**Input**: The detailed sprint file from `/agent-detail`.

Ensure the Blueprint is "Qwen-Ready" before execution:

### 0.1 Contract Integrity
```bash
# 1. Check for Contract Section
grep -q "CONTRACT & BLUEPRINT" [sprint_file.md]

# 2. Check for Schema/Context (Crucial for precision)
# Backend: Look for Schema Reference
# Frontend: Look for API Contract or Tailwind Specs
```

### 0.2 Atomic Integrity
- Ensure only **ONE** implementation file is listed in `FILES TO CREATE`.
- Ensure Verification Script is present.

**If Gate 0 Fails**: Return to `/agent-detail` to fix the blueprint. Do NOT execute.

---

## 🏗️ Gate 1: Structural & Static Analysis

Ensure the code is clean, typed, and formatted.

### 1.1 Python Code Checklist
```bash
# Style & Error Checking
uv run ruff check src/ tests/

# Type Checking (Strict)
uv run mypy src/

# Formatting Check
uv run ruff format --check src/ tests/
```

### 1.2 Web Code Checklist (if Frontend)
```bash
# Linting
npm run lint

# Type Checking
npm run type-check
```

**Result**: All commands MUST exit with code 0.

---

## 🧪 Gate 2: Functional Integrity (Testing)

Ensure the code works as intended via TDD artifacts.

### 2.1 Test Suite Execution
```bash
# Run all tests with coverage report
uv run pytest --cov=src --cov-report=term-missing tests/
```
**Constraint**: Coverage must be > 80% for new code.

### 2.2 Micro-Sprint Validation
Verify the 1:1 Test-to-Implementation rule:
1. List all `src/*.py` files modified.
2. Ensure corresponding `tests/test_*.py` exists.
3. Ensure verification logic in Sprint MD was executed.

---

## 🏗️ Gate 3: Architectural Audit (Librarian)

Ask the Librarian to review the changes against project standards.

```bash
uv run python .agent/workflows/automation/scripts/ask_librarian.py \
  "Review src/[module].py. Does it violate Clean Architecture (e.g. Domain importing Infrastructure)? Check ARCHITECTURE.md."
```

**Manual Check**: If Librarian flags a potential violation, specific approval is needed.

---

## 📝 Gate 4: Documentation & Memory

Ensure the work is documented for the future.

1. **Spec Update**: Is the Spec MD updated with any implementation details/changes?
2. **Decision Log**: Are major decisions logged in `.agent/memory/decision_log.md`?
3. **Active Context**: Is `.agent/memory/active_context.md` ready for the next task?

---

## 📊 Output: Verification Report

Create a report at `docs/verification/report_sprint[ID].md`:

```markdown
# ✅ Verification Report: Sprint [ID]

**Date**: YYYY-MM-DD
**Feature**: [Name]
**Verifier**: Agent-Verifier

## 1. Quality Gates
- [x] Static Analysis (Ruff/Mypy)
- [x] Test Suite (Pass: 12, Fail: 0, Cov: 95%)
- [x] Architecture Review

## 2. Artifacts Checked
- Spec: `docs/specs/...`
- Sprint: `docs/dev/sprints/...`

## 3. Issues / Tech Debt
- [ ] None
- [ ] [Issue description if minor debt allowed]

**Status**: READY FOR MERGE
```

---

## Triggering This Workflow

**User**: "/agent-verifier Sprint 4.1"

**AI Actions**:
1. Run Gate 1 (Lint/Type).
2. Run Gate 2 (Test).
3. Query Librarian (Gate 3).
4. Check Docs (Gate 4).
5. Generate Report.

---

*Trust, but Verify.*
