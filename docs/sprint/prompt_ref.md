# Documentation Refactoring Master Prompt

**Purpose:** Refactor project documentation to align with code reality and "Engineer's Journey" narrative.

---

## 🚀 Quick Start

1. **Read This File First** (you're here)
2. **Read** `verification_protocol.md` for verification rules
3. **Read** `output_guide.md` for sprint format
4. **Execute** the workflow below

---

## The Context

**Role:** You are an expert Technical Writer and Senior Software Engineer.

**Objective:** Refactor the entire `/docs` directory to reflect the code's reality and the project's "Engineer's Journey" narrative.

**The Narrative Persona:**
I am a [Current Role] with a background in [Previous Role] and [Early Role].
*   **Customer Service Mindset:** Focus on reducing user frustration ("Empathy").
*   **Hardware Mindset:** Treat software components like physical parts ("Logic").
*   **Integrator Mindset:** Focus on stability and factual accuracy ("Production First").

**Reference Template:**
*   **Style Guide:** Use `docs/sprint/readme_template.md` as your "Gold Standard" for formatting and tone.
*   **Narrative Adaptation:** The template contains placeholders (e.g., `[Nama Project]`, `[Teknologi Utama]`) that MUST be replaced with project-specific details:
    *   Read `composer.json` / `package.json` to identify actual technologies used
    *   Understand the project's core problem from existing docs
    *   Adapt the "Engineer's Journey" narrative to explain **WHY** these specific technologies were chosen for **THIS** project
    *   Maintain the humble, reflective tone: Focus on learning and constraints, not achievements
    *   **NO EMOJIS:** Do not use emojis in titles, headers, or body text. Use professional formatting (bold/italic) instead.

**Storytelling Innovation:**
*   **Connect Biography to Technology Choice:** For each major technology, explain how the user's past experience (CS/Hardware/Integration) influenced the decision
*   **Example:** "I chose Laravel because its strict structure mirrors the SOPs I use in system integration" NOT "I chose Laravel because it's popular"
*   **Project-Specific Narrative:** Replace generic statements with concrete examples from the actual codebase

---

## 🔄 Workflow

### Phase 1: Audit
1. Scan all `.md` files (exclude `node_modules`, `vendor`)
2. Follow **ALL rules in `verification_protocol.md`**
3. Build consistency map (email, versions, tech stack)

### Phase 2: Planning
1. Identify discrepancies and narrative mismatches
2. Propose Sprint Plan using format from `output_guide.md`
3. **STOP** and wait for user approval

### Phase 3: Execution
1. Execute approved sprints one at a time
2. Create sprint docs in `docs/sprint/sprintN.md`
3. Report completion and wait for "Continue"

### Phase 4: The "Zeroing" (Deep Scan)
**CRITICAL:** Do NOT finish until you perform this step.
1.  **Anti-Sampling:** Never assume "I fixed the header, so the body is fine."
2.  **Pattern Scan:** Use `grep` tools to hunt for forbidden items across ALL target files.
    *   **Emojis:** `[\x{1F600}-\x{1F64F}]`
    *   **Legacy Tech:** "Quill", "Material Icons", "Electric Earth"
    *   **Fancy Punctuation:** Em-dashes (`—`), En-dashes (`–`), Smart Quotes (`“` `”` `‘` `’`), Ellipsis (`…`).
    *   **Strict ASCII:** Use `[^\x00-\x7F]` to find *any* non-standard character.
3.  **Visual Confirmation:** Open the modified files one last time to ensure no formatting broke.
4.  **Self-Correction:** If you find *one* error during this phase, assume there are *ten* more. Restart the scan.

---

## 📂 Scope

**Files to Refactor:**
*   **ALL** `.md` files found in the project root and subdirectories.
*   Scan recursively to find every markdown file.

---

## ⚙️ For Antigravity/Cursor Users

**Output Audit Results to File:**
Create `docs/sprint/.audit_results.md` with:
- Complete file list (grouped by directory)
- Discrepancies found
- Consistency issues
- Proposed Sprint Plan

**Chat Output:** Only show summary stats and request approval.
