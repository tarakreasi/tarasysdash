# 🛠️ Optional External Tools

The **Semi-Agentic Toolkit** is designed to be lean regardless of the specific frameworks used. However, it ships with two powerful (optional) external frameworks:

---

## 1. Agent OS (`system/`)
*Source: Builder Methods (Brian Casel)*

**What is it?**
A comprehensive suite of "Spec-Driven Workflows" for Cursor/Claude. It defines a rigorous process for specifying products before building them.

**Key Features:**
- **Product Specs**: Templates for PRDs, Roadmaps, and Tech Stacks.
- **Profiles**: Pre-configured behavior for AI agents (e.g., "Senior React Dev").
- **Protocols**: Strict rules for creating implementation plans.

**Integration Status:**
- The Toolkit treats Agent OS workflows as additional data.
- You can put Agent OS specs in `docs/dev/specs/` and reference them in your Sprints.

**How to Use:**
Read `system/README.md`.

---

## 2. Design OS (`tools/design-engine/`)
*Source: Builder Methods (Brian Casel)*

**What is it?**
A UI design engine that bridges the gap between Figma and Code. It helps you design data models and UI components before writing implementation code.

**Key Features:**
- **Data Modeling**: Define entities/relationships first.
- **Component Export**: Generate Tailwind/HTML/React component code.
- **Visual Design**: Define tokens (colors, typography) systematically.

**Integration Status:**
- Located in `tools/design-engine/`.
- Use this to generate your frontend assets *before* starting a Frontend Sprint.

**How to Use:**
Read `tools/design-engine/README.md`.

---

## ⚠️ Important Note
These tools are **Third-Party Frameworks** included for convenience. 
- The **Core Toolkit** (Supervisor, Automation) does NOT depend on them.
- You can delete `system/` and `tools/` if you want a minimal installation.
