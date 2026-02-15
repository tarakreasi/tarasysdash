---
description: Manage Active Context and Proactive Librarian Memory
---
# 🧠 `/agent-memory` Workflow (Active Librarian)

Use this workflow to maintain "Active Memory" for the agent. This enables the Librarian to be **Proactive** rather than just Reactive.

---

## 🏗️ The Memory Structure

We establish a dedicated memory folder `.agent/memory/` containing 3 layers of context:

1. **`active_context.md`** (Short-term): What are we doing RIGHT NOW?
2. **`decision_log.md`** (Medium-term): Why did we do X?
3. **`project_rules.md`** (Long-term): Coding style, patterns, constrains.

---

## Steps to Activate Memory

### 1️⃣ Refresh Active Context (Start of Task)

When switching tasks or starting a session, run this:

1. **Identify Focus**:
   - Current Sprint: `docs/dev/sprints/sprintX_Y.md`
   - Active File: `src/current_file.py`

2. **Query Librarian (Proactive Fetch)**:
   ```bash
   uv run python .agent/workflows/automation/scripts/ask_librarian.py \
     "Context for [Active File] and [Sprint Goal]. Any dependencies or similar patterns?"
   ```

3. **Update `.agent/memory/active_context.md`**:
   
   ```markdown
   # 🧠 Active Context
   **Last Updated**: [Timestamp]
   **Focus**: [Task Name]
   
   ## 📍 Environment State
   - **Sprint**: [Sprint ID]
   - **Branch**: [Git Branch]
   
   ## 💡 Librarian Insights (Auto-Fetched)
   - **Related Files**: [List from Librarian]
   - **Relevant Docs**: [Docs found]
   - **Suggested Patterns**: [Patterns to use]
   
   ## ⚠️ Immediate Constraints
   - [Constraint 1 from Project Rules]
   - [Constraint 2]
   ```

### 2️⃣ Log Significant Decisions (During Task)

When a major technical decision is made (e.g., "Use Libraries X over Y"), append to `decision_log.md`:

```markdown
## [YYYY-MM-DD] Choice: Use Library X
- **Context**: Need fast JSON parsing.
- **Decision**: Used `orjson`.
- **Reason**: Benchmarks show 2x speedup.
- **Alternatives Rejected**: standard `json`.
```

### 3️⃣ Consult Memory (Before Coding)

**CRITICAL RULE**: Before writing any implementation code (via `/agent-detail`), execute:

```bash
cat .agent/memory/active_context.md
cat .agent/memory/project_rules.md
```

This ensures the agent is "loaded" with the correct context.

---

## 🤖 Automating "The Active Librarian"

To simulate a proactive Librarian, use this loop:

1. **Detection**: User opens a file or edits a sprint.
2. **Trigger**: Run `/agent-memory` refresh step.
3. **Output**: `.agent/memory/active_context.md` is updated.
4. **Notification**: "I've updated the active context with relevant docs for this file."

---

## Example Usage

**User**: "Mulai kerjakan Sprint 4.1.1"

**AI Actions**:
1. Read `sprint4_1_1_env_setup.md`.
2. Ask Librarian: "What is the standard env setup for this project?"
3. Write result to `active_context.md`.
4. Respond: "Context loaded. Librarian found standard setup in `init_template.md`. I will use that."

---

*Memory turns a stateless chatbot into a thoughtful partner.*
