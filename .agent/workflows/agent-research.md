---
description: Gather and synthesize information from documents before starting a task using Clean Architecture principles
---
# 🔬 `/agent-research` Workflow (Clean Architecture Edition)

Use this workflow to deeply analyze documents, external resources, or folders **before** starting any implementation. The goal is to create a structured research summary that serves as a **Technical Blueprint** for future sprints.

This workflow adopts principles from **Design OS** (Systematic Design) and **Agent OS** (Thinking Frameworks).

## 📋 Manifest
- **Mode A (Domain)**: Input=Ideas -> Output=`domain_[topic].md` -> Next=`/product-planner`
- **Mode B (Tech)**: Input=Architecture -> Output=`tech_[topic].md` -> Next=`/agent-spec`

## Steps

### 1️⃣ Identify Research Mode

**Mode A: Domain Discovery (Step 0)**
- **When**: Start of project. No specs yet.
- **Input**: User Brain, PDFs, Whitepapers.
- **Goal**: Understand the *Problem Space*.
- **Output**: `docs/research/domain_[topic].md`.

**Mode B: Technical Feasibility (Step 4)**
- **When**: After Architecture.
- **Input**: `ARCHITECTURE.md` + Feature Requirement.
- **Goal**: Understand the *Solution Space* (Libraries, Patterns).
- **Output**: `docs/research/tech_[topic].md`.

---

### 2️⃣ Gather Sources

**For Mode A (Domain):**
- **Read Docs**: Use `read_file` on uploaded PDFs or text files.
- **Web Search**: "Competitor analysis for [App]", "Industry standards for [Topic]".
- **User Interview**: Ask: "Who is the user?", "What is the pain point?".

**For Mode B (Technical):**
- **Check Constraints**:
  ```bash
  cat docs/architecture/ARCHITECTURE.md
  cat .agent/rules/CODING_STANDARDS.md
  ```
- **Librarian**: `ask_librarian.py "How do we currently handle [X]?"`
- **Agent OS**: `ls .agent/workflows/system/profiles/default/standards/`

---

### 3️⃣ Synthesize Findings (The Senior Engineer Way)

Use the appropriate template for your mode.

#### Template A: Domain Research (`docs/research/domain_[topic].md`)
```markdown
# Domain Research: [Topic]
**Type**: Business / Problem Space

## 1. Problem Statement
[What are we solving?]

## 2. Key Personas
- **[User A]**: Needs X to do Y.
- **[User B]**: Needs Z.

## 3. Market/Industry Standards
- [Standard 1]
- [Regulation 2]

## 4. Requirement Signals
- *Must Have*: ...
- *Should Have*: ...

## 5. Vocabulary (Ubiquitous Language)
- **Term X**: Definition...
```

#### Template B: Technical Strategy (`docs/research/tech_[topic].md`)
```markdown
# Technical Research: [Topic]
**Type**: Implementation / Solution Space
**Context**: [Stack from Architecture]

## 1. Goal
[Implement Feature X using Stack Y]

## 2. Options Analysis
| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| Lib A  | Fast | Big  | ❌ |
| Lib B  | Small| Slow | ✅ |

## 3. Clean Architecture Design
- **Domain**: Entity definitions...
- **Application**: Service layer logic...
- **Infrastructure**: Adapters needed...

## 4. Agent OS Alignment
- Matches `CODING_STANDARDS.md`? Yes/No
- Reuses existing standards? Yes/No

## 5. Prototype / Pseudo-Code
```python
def solution():
    pass
```
```

---

### 4️⃣ Review & Save
1. **Self-Correction**: Does this align with the Project Mission?
2. **Save**: Write to `docs/research/`.
3. **Index**:
   ```bash
   uv run python .agent/workflows/automation/scripts/index_codebase.py
   ```


---

## Related Workflows

| Workflow | Purpose |
|----------|---------|
| `/agent-architect` | High-level system design (Parent of this) |
| `/agent-spec` | Consumes this research to write requirements |

---

*Research is not just reading. It's designing the future.*
