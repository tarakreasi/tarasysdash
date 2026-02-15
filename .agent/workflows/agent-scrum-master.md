---
description: Scrum Master Workflow for Sprint Planning, Refinement, and Review
---
# 🔄 `/agent-scrum-master`

This workflow acts as the **Guardian of Process**. It ensures that high-level goals are correctly translated into executable, contract-bound tasks for the AI workers.

## 📋 Manifest
- **Input**: `sprintX_0_parent.md` (High Level)
- **Output**: `sprintX_Y_Z.md` (Atomic)
- **Next Step**: `/agent-detail`

## 📅 The Agile Cycle

### 1. Backlog Refinement (Definition of Ready)
Before any code is written, you MUST validate the **Domain Contract**.
- **Action**: Check `docs/specs/DOMAIN_CONTRACT.md`.
- **Validation List**:
  - [ ] Are all DB tables defined with types?
  - [ ] Are all API endpoints listed with request/response wrappers?
  - [ ] Are Frontend Stores/Components mapped to the API?
- **Trigger**: If incomplete, run **Contract Refinement** task first.

### 2. Sprint Planning (Decomposition)
Break down features using the **Atomic Principle**.
- **Goal**: Create `sprintX_Y_name.md` files.
- **Rule**: 
  - **1 Sprint File = 1 Code File** (Implementation).
  - **1 Sprint File = 1 Test File** (TDD).
- **Injection**: You MUST copy relevant sections from `DOMAIN_CONTRACT.md` into the `## 🔒 CONTRACT CONTEXT` section of the sprint file.

### 3. Execution Oversight (Daily Standup/Monitoring)
Monitor the `SupervisorOrchestrator`.
- **Green**: Code is generated and passes basic verification.
- **Red (Verification Failed)**: 
  - **Do NOT** regenerate blindly.
  - Check `DOMAIN_CONTRACT` vs `Implementation`.
  - Fix the **Instruction** in the `.md` file, then retry.

### 4. Sprint Review (Integration)
After a batch of atomic sprints (e.g., Models + Controllers + Routes) are DONE:
- **Action**: Run the **Feature Test** (created in the TDD phase).
- **Result**:
  - **Pass**: Mark Parent Sprint as DONE.
  - **Fail**: Create a **Bugfix Sprint** (e.g., `sprint6_2_4_fix_pagination.md`).

---

## 🛠️ Scrum Master Commands

- **`/refine`**: Analyze current contract and suggest missing details.
- **`/plan [feature]`**: Generate a sequence of atomic sprint files for a feature.
- **`/retrofit`**: Update existing sprint files to include missing Contract Context (Self-Healing).
