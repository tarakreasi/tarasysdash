---
description: The Master Pipeline - Orchestrate the entire Idea to Code process
---
# 🚀 `/idea-to-code` Master Workflow

This is the **Master Pipeline** that links all individual agent workflows into a coherent, end-to-end product development lifecycle. 

Use this to guide a project from a vague "Idea" to "Executable Code".

---

## 🗺️ The Pipeline Map

| Step | Workflow | Input | Output | Purpose |
|------|----------|-------|--------|---------|
| **0** | **`/agent-research`** | PDFs, Docs, Topics | `docs/research/research_*.md` | **Context Loading** (Optional). Understand the domain before planning. |
| **1** | **`/product-planner`** | User Idea / Research | `docs/product/mission.md` | **Scope Definition**. What are we building and why? |
| **2a** | **`/agent-architect`** | Mission + Docs | `ARCHITECTURE.md` | **Greenfield Strategy**. For new projects. |
| **2b** | **`/agent-code`** | Existing Code | `RECOVERY_PLAN.md` | **Brownfield Strategy**. For reviving stalled projects. |
| **3** | **`/agent-design`** | Mission + Docs | `product/sections/` | **Visuals**. Mocks, Prototypes, UI/UX. |
| **4** | **`/agent-research`** | Architecture | `docs/research/technical_*.md` | **Feasibility**. Validate implementation using Agent OS patterns. |
| **5** | **`/agent-spec`** | Mission + Research | `docs/specs/[date]-[name]/` | **Requirements**. Detailed functional specs & test strategy. |
| **6** | **`/agent-init`** | Spec | `sprintX_0_parent.md` | **Project Management**. Create the Sprint Plan. |
| **7** | **`/agent-scrum-master`** | Parent Sprint | `sprintX_Y_Z.md` | **Process Guardian**. Break down sprints & enforce contracts. |
| **8** | **`/agent-microsprint`** | Parent Sprint | `sprintX_Y_Z.md` | **Task Breakdown**. Atomic file-level tasks (Tool used by Scrum Master). |
| **9** | **`/agent-detail`** | Microsprint MD | Executable MD | **Execution Prep**. Add verification scripts for Qwen. |
| **10** | **`/agent-verifier`** | Implemented Code | Verification Report | **Quality Gate**. Run tests, static analysis, and arch checks. |
| **Support** | **`/agent-debug`** | Bug Report | Incident Report | **RCA**. Reproduce -> Analyze -> Fix Loop. |
| **Support** | **`/agent-optimizer`** | Codebase | Refactored Code | **Technical Debt**. Improve code quality and maintainability. |

---

## 🏗️ Directory Structure Standard

This workflow enforces the following project structure. Data lives in `docs/`, Logic lives in `.agent/`.

```
/project-root
├── .agent/                  # 🧠 The Brain
│   ├── workflows/           # Skill definitions (like this file)
│   ├── rules/               # Project-specific Coding Standards
│   └── scripts/             # Automation tools
│
├── docs/                    # 📚 The Memory
│   ├── product/             # Vision, Roadmap, User Personas
│   ├── architecture/        # Stack decisions, System Diagrams
│   ├── research/            # Domain & Technical deep dives
│   ├── specs/               # Validated Specifications 
│   └── dev/                 # Development logs
│       └── sprints/         # Sprint Plans (Parent & Micro)
│
└── src/                     # 💻 The Code (Implementation)
```

---

## 👣 Step-by-Step Execution Guide

### Phase 1: Definition (The "What")

**0. Context Loading (Optional)**
> "I have documents/ideas but no structure."
- **Run**: `/agent-research` (Mode A: Domain)
- **Output**: `docs/research/domain_[topic].md`
- **Use Case**: Ingesting PDFs, Whitepapers, or analyzing competitors.

**1. Product Planning**
> "What are we building?"
- **Run**: `/product-planner`
- **Input**: User Idea OR `docs/research/domain_*.md`.
- **Output**: `docs/product/mission.md`.

**2. Architecture & DNA**
> "How do we build this?"
- **Run**: `/agent-architect` (Greenfield)
- **Input**: Check `.agent/workflows/system/profiles/default/standards/`.
- **Output**: `docs/architecture/ARCHITECTURE.md` and `.agent/rules/CODING_STANDARDS.md`.
- **Critical**: Inherit from Agent OS standards (Vue, CSS, etc.).

**2b. Revival (Legacy Projects)**
> "What is this mess?"
- **Run**: `/agent-code` (Brownfield)
- **Input**: The existing codebase.
- **Output**: `docs/planning/RECOVERY_PLAN.md`.

### Phase 2: Design (The "How")

**3. The Visual Design (Form)**
> "Don't code blindly. See it first."
- **Run**: `/agent-design`
- **Action**:
  - Run `/shape-section` to define the UI flow.
  - Run `/design-screen` to generate component code.
- **Output**: Visual Specs and React Components.

**4. Technical Feasibility Check**
> "Do we know how to implement [Complex Feature] in [Stack]?"
- **Run**: `/agent-research` (Mode B: Technical)
- **Input**: `ARCHITECTURE.md`.
- **Output**: `docs/research/tech_[topic].md`.

**5. Specification**
> "Write the blueprint."
- **Run**: `/agent-spec`
- **Input**:
  - Domain: `docs/research/domain_*.md`
  - Tech: `docs/research/tech_*.md`
  - Arch: `ARCHITECTURE.md`
- **Output**: `docs/specs/[date]-[feature]/spec.md`.
- **Gate**: Must define Test Strategy.

### Phase 3: Execution (The "Build")

**6. Sprint Initialization**
> "Let's plan the work."
- **Run**: `/agent-init`
- **Input**: `spec.md` OR `RECOVERY_PLAN.md`.
- **Goal**: Create the Parent Sprint.

**7. Atomic Decomposition (Scrum Master)**
> "Break it down and guard the contract."
- **Run**: `/agent-scrum-master` (uses `/agent-microsprint` internally).
- **Goal**: Ensure every atomic task is linked to `DOMAIN_CONTRACT.md`.
- **Run**: `/agent-detail` to make it executable.

**8. Verification (The Quality Gate)**
> "Did we build it right?"
- **Run**: `/agent-verifier`
- **Output**: `docs/verification/report_sprint[ID].md`
- **Critical**: Must pass Gate 1 (Lint), Gate 2 (Test), and Gate 3 (Architecture).

---

## 🚦 Quality Gates

**Do NOT proceed if:**
- [ ] **Architecture Missing**: If `CODING_STANDARDS.md` is missing, AI will hallucinate styles.
- [ ] **Ambiguous Spec**: If spec says "Implement Auth" without details, go back to `/agent-research`.
- [ ] **No Verification**: If a sprint lacks a `verify` script, it is not ready for coding.

---

## ⚡ Quick Start Command

```bash
# Start from zero
/product-planner

# Start from existing docs
/agent-research
```
