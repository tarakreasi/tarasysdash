---
description: Initialize a new Parent Sprint based on external documents and Librarian context
---
# 🚀 `/agent-init` Workflow (TDD Edition)

Use this workflow to transform raw ideas or documents into a structured high-level sprint plan.

## 📋 Manifest
- **Input**: `docs/specs/.../spec.md` OR `RECOVERY_PLAN.md`
- **Output**: `docs/dev/sprints/sprintX_0_parent.md` (& `DOMAIN_CONTRACT.md`)
- **Next Step**: `/agent-scrum-master`

## Steps

### 0. Check Architecture & DNA
**CRITICAL**: Before planning, ensure the project's Automation DNA exists.

```bash
ls .agent/rules/CODING_STANDARDS.md
```

- **If missing**: STOP. Run `/agent-architect` first.
- **Reason**: The Executor Script needs these rules to generate valid code.

### 1. Read Foundation
### 1. Read Foundation
- **Input A (Standard)**: Read `docs/specs/YYYY-MM-DD-feature/spec.md`.
- **Input B (Revival)**: Read `docs/planning/RECOVERY_PLAN.md` (from `/agent-code`).
- **Context**: Read `docs/architecture/ARCHITECTURE.md`.
- **Check Test Strategy**: Ensure the Spec/Plan defines the testing approach.

### 2. Consult Librarian
```bash
uv run python .agent/workflows/automation/scripts/ask_librarian.py "Summarize current state of [Topic] in codebase"
```
- Ensure the new plan doesn't conflict with existing implementations.
- Note existing test patterns to follow.

### 3. Create Domain Contract (`docs/specs/DOMAIN_CONTRACT.md`)
   - This file is the **Single Source of Truth** for all subsequent AI generations.
   - MUST include:
     - **Database Schema**: Table names, columns, types (e.g., `transaction_date: date`).
     - **API Contract**: Endpoints, methods, request/response payload structures (wrapped in `data`).
     - **UI Components**: Component hierarchy, props, and state definitions.
     - **Strict Types**: Enum values and constants.

### 4. Generate Parent Sprint

Create `docs/dev/sprints/sprintX_0_parent_name.md`:

```markdown
# Sprint X.0: [Feature Name] (Parent)

**Spec**: @[Spec Document or Recovery Plan]
**Objective**: [High-level goal from spec]
**Status**: PLANNING

---

## 📊 Sprint Overview

| Metric | Target |
|--------|--------|
| Micro-Sprints | 5-8 |
| Files to Create | ~10-15 |
| Test Coverage | 80%+ |

---

## 🧪 Test Strategy

**Test Files**:
- `tests/test_[module1].py`
- `tests/test_[module2].py`

**Approach**: TDD (Test-First per micro-sprint)

---

## 📋 Micro-Sprint Breakdown

### Phase 1: Setup
| Sprint | Description | Files | Type |
|--------|-------------|-------|------|
| X.1 | Environment Setup | 2 | Setup |

### Phase 2: Core Module A
| Sprint | Description | Files | Type |
|--------|-------------|-------|------|
| X.2.1 | Create test_module_a.py | 1 | Test |
| X.2.2 | Create module_a.py | 1 | Impl |

### Phase 3: Core Module B
| Sprint | Description | Files | Type |
|--------|-------------|-------|------|
| X.3.1 | Create test_module_b.py | 1 | Test |
| X.3.2 | Create module_b.py | 1 | Impl |

### Phase 4: Integration
| Sprint | Description | Files | Type |
|--------|-------------|-------|------|
| X.4 | Integration & E2E | 2 | Test+Impl |

---

## ✅ Parent Completion Criteria

- [ ] All micro-sprints COMPLETED
- [ ] All tests passing (`pytest tests/ -v`)
- [ ] Code review completed
- [ ] Documentation updated

---

## 🔗 Dependencies

**Requires**:
- Spec document must be APPROVED

**Produces**:
- Working [feature] implementation
- Test suite with 80%+ coverage
```

---

## 4. Granularity Check

Before finalizing, ensure:

| Check | Requirement |
|-------|-------------|
| Micro-sprint count | 5-10 per parent |
| Lines per micro-sprint | 80-120 max |
| Files per micro-sprint | 1-3 max |
| Tasks per micro-sprint | 2-4 max |
| Test-to-Impl ratio | 1:1 (each impl has test) |

**If any micro-sprint exceeds limits → Split further!**

---

## 5. TDD Pairing Rule

For every implementation sprint, there MUST be a preceding test sprint:

```
❌ WRONG:
Sprint 2.1: Create auth.py

✅ CORRECT:
Sprint 2.1: Create test_auth.py (Test First)
Sprint 2.2: Create auth.py (Pass Tests)
```

---

## 6. Self-Review

Before marking Parent Sprint as READY:

- [ ] Spec document is linked
- [ ] Test strategy is defined
- [ ] Each module has test+impl pair
- [ ] No micro-sprint exceeds 120 lines
- [ ] Dependencies are documented

---

## Related Workflows

| Next | Purpose |
|------|---------|
| `/agent-microsprint` | Create the individual micro-sprint files |
| `/agent-detail` | Add Qwen-optimized execution details |
