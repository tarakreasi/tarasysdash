---
description: Analyze existing/stalled projects to create a recovery sprint plan
---
# 🕵️ `/agent-code` Workflow (The Project Reviver)

Use this workflow for **Brownfield Projects**—projects that already exist but are "mangkrak" (stalled), undocumented, or need a major refactor before new work can begin.

---

## 🎯 Goal
Turn an opaque legacy codebase into a **Clear Recovery Plan** that can be fed into `/agent-init`.

---

## Steps

### 1️⃣ Codebase Ingestion (The Scan)
First, we must understand what we have.

1. **Index the Code**:
   ```bash
   # Update the Librarian's view of the current state
   uv run python .agent/workflows/automation/scripts/index_codebase.py
   ```

2. **Structural Audit**:
   ```bash
   # Get a high-level view
   tree -L 2 -I "node_modules|venv|vendor|.git"
   ```

### 2️⃣ The Diagnostic (Health Check)
Determine the state of the project.

**Ask the Librarian:**
```bash
uv run python .agent/workflows/automation/scripts/ask_librarian.py "Analyze the architecture. Is it MVC? Clean Architecture? Spaghetti? summarize the tech stack."
```

**Run Manual Checks:**
- [ ] Does it build? (Try `npm run build` or equivalent)
- [ ] Do tests pass? (Try `npm test` or `pytest`)
- [ ] Are dependencies outdated?

### 3️⃣ Gap Analysis (Mission vs Reality)
Connect with the Product Mission.

1. **Read Mission**: `cat docs/product/mission.md`
2. **Compare**:
   - **Mission says**: "Real-time Chat"
   - **Code has**: "Basic HTTP endpoints"
   - **Gap**: "Missing Websocket implementation"

### 4️⃣ Create Recovery Plan
Create `docs/planning/RECOVERY_PLAN.md`.

```markdown
# Recovery Plan: [Project Name]

## 1. Current State Assessment
- **Health**: [Critical/Stable/Good]
- **Tech Stack**: [Detected Stack]
- **Blocking Issues**:
  - [Build fails]
  - [No database migrations]

## 2. Refactoring Strategy
- [ ] **Phase 1 (Stabilize)**: Fix build, update deps.
- [ ] **Phase 2 (Refactor)**: Move logic to Domain layer.
- [ ] **Phase 3 (Feature)**: Start new work.

## 3. Sprint 0 Recommendation
- **Sprint Goal**: "Make the project build and pass basic tests."
- **Tasks**:
  1. Fix `package.json` scripts.
  2. Dockerize the environment.
  3. Document the setup in `README.md`.
```

---

## 🔗 Handoff
Once `RECOVERY_PLAN.md` is ready:

- **Next Step**: Run `/agent-init`.
- **Instruction**: "Initialize Sprint based on `docs/planning/RECOVERY_PLAN.md` instead of a Spec."

---

## ⚠️ Warning
Legacy code is dangerous.
- **Rule 1**: Do not change logic without a test (even a bad test).
- **Rule 2**: Read `CODING_STANDARDS.md` before refactoring. If it doesn't exist, **create it first** (run `/agent-architect`).
