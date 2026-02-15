---
description: Transform research findings into a structured spec document ready for sprint creation
---
# 📝 `/agent-spec` Workflow (Enhanced Edition)

Use this workflow to convert raw research (`docs/research/`) into a formal specification (`docs/specs/`) that is **ready for sprint planning**.

This workflow integrates best practices from **Agent OS Specification System**.

## 📋 Manifest
- **Input**: `docs/research/tech_[topic].md` (Feasibility)
- **Output**: `docs/specs/[date]-[name]/spec.md`
- **Next Step**: `/agent-init`

## Prerequisites
- **Domain Context**: `docs/research/domain_[topic].md` (from Start).
- **Technical Context**: `docs/research/tech_[topic].md` (from Feasibility).
- **Architecture**: `docs/architecture/ARCHITECTURE.md`.

---

## Phase Overview

| Phase | Purpose | Output |
|-------|---------|--------|
| **1. Initialize** | Create folder structure | `docs/specs/[date]-[name]/` |
| **2. Research** | Clarify requirements with questions | `planning/requirements.md` |
| **3. Write** | Create main specification | `spec.md` |
| **4. Verify** | Validate alignment | `verification/spec-verification.md` |

---

## Phase 1: Initialize Spec Structure

### 1.1 Determine Spec Name
- Derive a `kebab-case` name from the topic (e.g., `librarian-vector-search`).
- Prefix with today's date for chronological sorting.

### 1.2 Create Folder Structure
```bash
TODAY=$(date +%Y-%m-%d)
SPEC_NAME="[kebab-case-name]"
SPEC_PATH="docs/specs/${TODAY}-${SPEC_NAME}"

mkdir -p $SPEC_PATH/planning/visuals
mkdir -p $SPEC_PATH/implementation
mkdir -p $SPEC_PATH/verification

echo "Created spec folder: $SPEC_PATH"
```

### 1.3 Save Raw Idea
Create `planning/initialization.md`:
```markdown
# Spec Initialization: [Spec Name]

## Source
## Source
- Domain Research: `docs/research/domain_[topic].md`
- Tech Research: `docs/research/tech_[topic].md`
- Architecture: `docs/architecture/ARCHITECTURE.md`
- External Documents: [List any external inputs]

## Raw Idea
[Copy the user's original description or research summary here verbatim]

## Initial Observations
- [Key point 1 from research]
- [Key point 2 from research]
```

---

## Phase 2: Research & Clarify Requirements

### 2.1 Analyze Context
Before asking questions, gather context:
```bash
### 2.1 Analyze Context
Before asking questions, gather context from upstream agents:
```bash
# 1. Product Context (from Product Planner)
cat docs/product/mission.md 2>/dev/null || echo "No mission doc"

# 2. Technical Context (from Agent Architect)
cat docs/architecture/ARCHITECTURE.md 2>/dev/null || echo "No architecture doc"

# 3. Coding Standards (from Agent Architect/OS)
ls .agent/rules/CODING_STANDARDS.md 2>/dev/null || echo "CRITICAL: No standards found"

# 4. Query Librarian for related code
uv run python .agent/workflows/automation/scripts/ask_librarian.py "Existing patterns for [feature]"
```
```

### 2.2 Generate Clarifying Questions
Ask 4-8 targeted, **NUMBERED** questions:

```markdown
Based on your idea for [spec name], I have some clarifying questions:

1. I assume [specific assumption]. Is that correct, or [alternative]?
2. I'm thinking [specific approach]. Should we [alternative]?
3. For [feature], would you prefer [option A] or [option B]?
...
[Last question]: Are there any features explicitly OUT OF SCOPE?

**Existing Code Reuse:**
Are there existing features with similar patterns we should reference?
- Similar UI components to re-use?
- Related backend logic or services?
- Existing models with similar functionality?

Please provide file/folder paths if they exist.

**Visual Assets Request:**
Do you have any mockups, wireframes, or screenshots?
If yes, place them in: `[spec-path]/planning/visuals/`
```

**OUTPUT questions and WAIT for user response.**

### 2.3 Process Answers

1. Store user's answers.
2. **MANDATORY Visual Check** (even if user says no visuals):
```bash
ls -la [spec-path]/planning/visuals/ 2>/dev/null | grep -E '\.(png|jpg|jpeg|gif|svg|pdf)$' || echo "No visual files found"
```
3. Document paths to similar features for later reference.
4. Ask follow-up questions if needed (max 1-3).

### 2.4 Save Requirements
Create `planning/requirements.md`:

```markdown
# Spec Requirements: [Spec Name]

## Initial Description
[From initialization.md]

## Requirements Discussion

### First Round Questions

**Q1:** [Question]
**Answer:** [User's exact answer]

**Q2:** [Question]
**Answer:** [User's exact answer]

### Existing Code to Reference
| Feature | Path | How to Reuse |
|---------|------|--------------|
| [Name] | `path/to/file` | [Extend/Copy pattern] |

### Visual Assets
**Files Found:** [from bash check]
- `filename.png`: [Description of what it shows]

**Visual Insights:**
- [Design patterns identified]
- [Fidelity level: high/low]

## Requirements Summary

### Functional Requirements
- [Core functionality]

### Non-Functional Requirements
- **Performance**: [Constraint]
- **Security**: [Constraint]

### Scope Boundaries
**In Scope:**
- [Feature A]

**Out of Scope:**
- [Feature B - explicitly excluded]
```

---

## Phase 3: Write Specification

### 3.1 Search for Reusable Code
Before writing, search for existing patterns:
```bash
uv run python .agent/workflows/automation/scripts/ask_librarian.py "Components similar to [feature]"
```

### 3.2 Create `spec.md`
**DO NOT write actual code.** Only describe requirements clearly.

```markdown
# Specification: [Feature Name]

**Version**: 1.0
**Date**: YYYY-MM-DD
**Status**: DRAFT | READY | APPROVED
**Research Sources**: `docs/research/domain_*.md`, `docs/research/tech_*.md`

---

## 1. Goal
[1-2 sentences describing the core objective. Be specific.]

## 2. User Stories
- As a [user type], I want to [action] so that [benefit].
- As a [user type], I want to [action] so that [benefit].

## 3. Functional Requirements

### 3.1 [Requirement Name]
- [Specific sub-requirement or behavior]
- [Technical approach if known]

### 3.2 [Requirement Name]
- [Specific sub-requirement]

## 4. Non-Functional Requirements
- **Performance**: [Constraint]
- **Security**: [Constraint]
- **Compatibility**: [Constraint]

## 5. Visual Design
[If mockups provided]

**`planning/visuals/[filename]`**
- [Up to 8 bullets describing UI elements]

## 6. Existing Code to Leverage
| File/Module | Purpose | How to Reuse |
|-------------|---------|--------------|
| `path/to/file.py` | [What it does] | [Extend/Import] |

## 7. Dependencies
- [External library needed]
- [Related spec that must complete first]

## 8. Out of Scope
- [Feature explicitly NOT included]
- [Edge case for later]

## 9. Acceptance Criteria
- [ ] [Testable condition #1]
- [ ] [Testable condition #2]
- [ ] [Testable condition #3]

## 10. Test Strategy (TDD)

### 10.1 Test Categories
| Category | Description | Sprint Target |
|----------|-------------|---------------|
| Unit Tests | Individual functions/methods | Per micro-sprint |
| Integration Tests | Component interactions | Parent sprint level |
| E2E Tests | User flows | Final sprint |

### 10.2 Test Files to Create
| Test File | Tests For | Priority |
|-----------|-----------|----------|
| `tests/test_[module1].py` | [Module 1] | P0 (First) |
| `tests/test_[module2].py` | [Module 2] | P1 |

### 10.3 Test-First Rules
1. **Write test BEFORE implementation**
2. Each micro-sprint creates test file first
3. Implementation must pass all tests
4. No merge without green tests

## 11. Sprint Decomposition Guide

### 11.1 Granularity Rules
**Target: 80-120 lines per micro-sprint**

| Content | Max Lines | Max Items |
|---------|-----------|-----------|
| Tasks | 60 lines | 3 tasks |
| Files | - | 3 files |
| Test cases | - | 5 tests |

### 11.2 Sprint Breakdown Pattern
```
Sprint X.0: [Parent - Overview only]
├── Sprint X.1: Setup & Dependencies
├── Sprint X.2.1: Create test_module_a.py (Test First)
├── Sprint X.2.2: Create module_a.py (Pass Tests)
├── Sprint X.3.1: Create test_module_b.py
├── Sprint X.3.2: Create module_b.py
└── Sprint X.4: Integration & Final Tests
```

### 11.3 Micro-Sprint Naming
```
sprintX_Y_Z_description.md

X = Major version (feature group)
Y = Minor version (module)
Z = Patch (test vs implementation)
    .1 = Test file
    .2 = Implementation
    .3 = Integration
```

---

## Next Steps
→ Ready for `/agent-init` to create Parent Sprint.
```

---

## Phase 4: Verify Specification

### 4.1 Structural Verification
Check that all files exist:
```bash
ls -la [spec-path]/
ls -la [spec-path]/planning/
```

### 4.2 Content Validation
Verify:
- [ ] All user answers from Q&A are accurately captured in `requirements.md`.
- [ ] Visual assets (if found) are referenced in spec.
- [ ] Out of scope items match what user stated.
- [ ] No features added beyond requirements.
- [ ] Existing code reuse opportunities are documented.

### 4.3 Create Verification Report
Save to `verification/spec-verification.md`:

```markdown
# Specification Verification Report

## Summary
- **Overall Status**: ✅ Passed | ⚠️ Issues Found | ❌ Failed
- **Date**: [Date]
- **Spec**: [Name]
- **Reusability Check**: ✅ Passed | ⚠️ Concerns

## Checks Performed

### Check 1: Requirements Accuracy
✅ All user answers captured
✅ Reusability opportunities documented

### Check 2: Visual Assets
✅ Found [X] files, all referenced

### Check 3: Scope Alignment
✅ Features match requirements
✅ Out of scope correctly excluded

### Check 4: Reusability
⚠️ [Any missed opportunities]

## Issues Found
[List any discrepancies]

## Conclusion
[Ready for implementation? / Needs revision?]
```

---

## Self-Review Checklist (Before Marking READY)

- [ ] Goal is specific and measurable.
- [ ] User stories cover primary use cases.
- [ ] Functional requirements are implementable.
- [ ] Existing code consulted via Librarian.
- [ ] Out of scope explicitly defined.
- [ ] Acceptance criteria are testable.
- [ ] Visual assets analyzed and referenced.
- [ ] Verification report created.

---

## Output Structure

```
docs/specs/
└── [YYYY-MM-DD]-[feature-name]/
    ├── planning/
    │   ├── initialization.md     # Raw idea
    │   ├── requirements.md       # Gathered requirements
    │   └── visuals/              # Mockups, screenshots
    ├── spec.md                   # Main specification
    ├── implementation/           # (Filled later during sprints)
    └── verification/
        └── spec-verification.md  # Verification report
```

---

## Linking to Sprint Pipeline

Once spec status is **READY**:
1. **`/agent-init`** — Create Parent Sprint referencing this spec.
2. **`/agent-microsprint`** — Breakdown into executable steps.
3. **`/agent-detail`** — Add verification scripts.

---

## Example Usage

**User Prompt**:
> "/agent-spec based on my research about Librarian vector search"

**AI Actions**:
1. Read `docs/research/research_librarian_*.md`.
2. Create `docs/specs/2026-01-16-librarian-vector-search/`.
3. Initialize with folder structure.
4. Ask clarifying questions.
5. Save requirements after user answers.
6. Write `spec.md` with all sections.
7. Perform verification checks.
8. Report summary and set status to DRAFT (awaiting approval).

---

*A good spec is the difference between chaos and clarity. Write it well.*
