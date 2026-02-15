---
description: Inject extreme implementation details and verification scripts into a micro-sprint (Qwen-Executable)
---
# 🔍 `/agent-detail` Workflow (Qwen-Executable)

Use this workflow to transform a high-level micro-sprint into a **machine-readable, deterministic** format that our `execute_sprint.py` script can run without human intervention.

## 📋 Manifest
- **Input**: `sprintX_Y_Z.md` (Draft)
- **Output**: `sprintX_Y_Z.md` (Executable - with Code & Tests)
- **Next Step**: `SupervisorOrchestrator` (Execution)

---

## 🎯 Goal

Make the Sprint MD file **self-contained** and **deterministic**.
1. **No ambiguities** (e.g., "Install Vue" -> "Run exact npm command or manual scaffold").
2. **Code Complete** (The markdown block MUST contain the full working code, no TODOs).
3. **Automated Verification** (A python script that returns exit code 0 if success).

---

## 📋 The "Qwen-Ready" Sprint Template

Your output MD file must follow this structure EXACTLY to be parsed by `execute_sprint.py`.

```markdown
# Sprint X.Y.Z: [Title]

**Parent**: @[Sprint X.0](./sprintX_0_parent.md)
**Objective**: [One sentence]
**Executor**: Qwen
**Status**: PLANNING

## 📁 FILES TO CREATE

| Path | Description |
|------|-------------|
| `path/to/file1.ext` | [Description] |
| `verify_sprint.py` | Verification Script |

## 📋 TASKS

### Task 1: [Action Name]

**File**: `path/to/file1.ext`

**Content**:
```[lang]
[FULL CODE HERE - NO PLACEHOLDERS]
```

### Task 2: [Another Action]

**File**: `path/to/file2.ext`

**Content**:
```[lang]
[FULL CODE HERE]
```

### Task 3: Verification Script

**File**: `verify_sprint.py`

**Content**:
```python
import os
import sys
# ... verification logic ...
if success:
    sys.exit(0)
else:
    sys.exit(1)
```

## ✅ COMPLETION CRITERIA

1. All files created.
2. `python3 verify_sprint.py` returns exit code 0.
```

---

## 📐 Rules of Engagement

### 1. Determinism > Interactivity
- **NEVER** use interactive commands like `npm init`, `composer create-project` (without --no-interaction), or `read input`.
- **PREFER** writing specific config files manually (e.g., writing `package.json` with `cat`) over generating them if generators are flaky.
- **ALWAYS** set `set -e` in shell scripts.

### 2. Code Completeness
- The code inside the `Content` block is what gets written to disk.
- **DO NOT** use `... (rest of code)` or `# TODO`.
- **DO NOT** assume the file exists; always provide the full content or use specific `sed` commands if modifying (but overwriting is safer for automation).

### 3. Verification is Mandatory
- Every sprint MUST produce a `verify_*.py` script.
- This script is the "Test" in TDD.
- It must be self-contained (import only standard libs if possible).

### 4. Schema/Contract Alignment (CRITICAL for AI)
- If a task is for **AI Generation** (not a static Code Block), you MUST provide a `**Context**` or `**Schema**` section.
- Explicitly list **Database Fields** (names, types).
- Explicitly list **API Routes** and **JSON keys**.
- **WHY**: This prevents AI from "hallucinating" extra fields (e.g., adding `user_id` when the database only has `title`).

---

## 🔄 Workflow Steps to Execute /agent-detail

### 1. Context Loading (DNA Check)
Before detailing, you MUST know the rules.
```bash
# 1. Read Automation Rules
cat .agent/rules/CODING_STANDARDS.md

# 2. Read Technical Architecture
cat docs/architecture/ARCHITECTURE.md
```
**Why?**: Your verification scripts must match the project's test runner (e.g., `pytest` vs `unittest`) and language standards.

### 2. Review the Micro-Sprint
Read the high-level plan from `/agent-microsprint` (`docs/dev/sprints/sprintX_Y_Z.md`).

### 3. Technical Checklist (Verify these before writing MD)
- [ ] **Base Classes**: Are `Controller`, `Model`, or `BaseTest` imports included?
- [ ] **Schema**: Are all DB fields/JSON keys explicitly listed?
- [ ] **Standards Compliance**: Does the code follow `CODING_STANDARDS.md`?
- [ ] **CWD**: Does the `verify_*.py` script use `os.path.abspath`?

### 4. Expand Tasks
    - **MANDATORY**: Include a `Local Guardrails` sub-section in the instruction.
    - **STRICT NAMING**: Mention forbidden field names (e.g., "Use title, NOT description").
    - **TECH STACK**: Mention specific implementation rules (e.g., "Use computed for formatting").
4. **Update MD File**: Overwrite the sprint file with this detailed content.
5. **Mark as PLANNING**: Ensure status is PLANNING so the Orchestrator picks it up.
```markdown
### Task 1: [Action]
**Instruction**: 
[General goal]
- 🚫 **FORBIDDEN**: [List common hallucinations]
- ✅ **MANDATORY**: [List specific column names from contract]
```

---

## 🔗 Integration

| Input | Process | Output |
|-------|---------|--------|
| `ARCHITECTURE.md` | **Context** | DNA Compliance |
| `sprintX_Y_Z.md` (Abstract) | **`/agent-detail`** | `sprintX_Y_Z.md` (Executable) |
| `sprintX_Y_Z.md` (Executable) | **`orchestrator.py`** | Working Code on Disk |

---

*If Qwen has to guess, the sprint reflects a failure in planning. Be explicit. Schema context is the key to precision.*
