---
description: Use proactively to create product documentation including mission, and roadmap
---
# 💡 `/product-planner` Workflow (The Idea Shaper)

Use this workflow **FIRST** when you have a vague idea or a new project request. It acts as the "Translator" between User Intent and Technical Architecture.

---

## 🎯 Goal
Transform a raw prompt (e.g., "I want a finance app") into a structured **Product Brief** (`docs/product/mission.md`).

## 📋 Manifest
- **Input**: User Idea OR `docs/research/domain_*.md`
- **Output**: `docs/product/mission.md` (& `roadmap.md`)
- **Next Step**: `/agent-architect`

---

## Steps

### 1️⃣ The Socratic Interview & Context Check
First, check if pre-planning research was done (Step 0):
```bash
ls docs/research/domain_*.md 2>/dev/null || echo "No domain research found."
```
- **If Found**: Read it. This contains the "Problem Space" analysis.
- **If Missing**: Start understanding. Ask the user 3-5 critical questions:

1.  **The "Why"**: What is the core problem we are solving?
2.  **The "Who"**: Who is the primary user? (e.g., "Freelancers" vs "Enterprises")
3.  **The "Constraint"**: Are there budget/time/hardware limits? (e.g., "Must run on a Raspberry Pi")
4.  **The "Vibe"**: What is the desired look & feel? (e.g., "Corporate" vs "Playful")

**Wait for the user's answers.**

### 2️⃣ Define the MVP (The Scope Hammer)
Based on the answers, define the **Minimum Viable Product**.
- Identify the **Core Loop** (The one thing the user does 80% of the time).
- Ruthlessly move nice-to-haves to "Phase 2".

### 3️⃣ Generate the Brief
Create folder `docs/product/` and file `docs/product/mission.md`.

**Template**:
```markdown
# Product Mission: [Project Name]

## 1. Vision Statement
[A single powerful sentence describing what we are building and why.]

## 2. Target Audience
- **Primary**: [User Persona 1]
- **Secondary**: [User Persona 2]

## 3. Core Value Proposition
- [Benefit 1]
- [Benefit 2]

## 4. MVP Scope (Phase 1)
- [Feature A]
- [Feature B]
- [Feature C]

## 5. Technical Constraints (Input for Architect)
*These will determine the stack.*
- **Scale**: [e.g. Low traffic, Single user]
- **Platform**: [e.g. Web, Mobile, CLI]
- **Performance**: [e.g. Real-time required?]
- **Storage**: [e.g. Local-only vs Cloud]

## 6. Future Roadmap (Out of Scope)
- [Feature X]
- [Feature Y]
```

---

## 🔗 Handoff
Once `docs/product/mission.md` is created:
- **Next Step**: Run `/agent-architect` and tell it to "Read the Product Mission".

---

*A clear mission saves 100 hours of coding.*
