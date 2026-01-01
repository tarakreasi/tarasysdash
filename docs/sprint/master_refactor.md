# The Master Refactor Protocol
> *Lessons learned from the "TaraNote Go" 24-Hour Migration Marathon.*

This document outlines the strategy used to successfully migrate a legacy Laravel application to a high-performance Go backend in a single day. Use this as a blueprint for future refactoring projects (e.g., `taraSysDash`).

---

## 1. The Mindset: "Strictness Meets Speed"

Refactoring often fails because of "scope creep" or "loss of context". To succeed, strict discipline is required.

*   **Don't Fix Logic, Port It:** When migrating, do not try to improve the business logic simultaneously. Clone the behavior first (Sprint 1-4), then optimize (Sprint 5+).
*   **The "Black Box" Approach:** Treat the Frontend as a sacred "Black Box". If you change the Backend, the Frontend shouldn't know. If the Vue app crashes, the Backend migration failed.
*   **RCA (Root Cause Analysis):** Do not guess. Isolate the fault domain. Trace the signal. Resolve the root.

---

## 2. The Artifact Trinity (Context Control)

Never start coding without "The Trinity". These three files keep the AI (and you) focused.

### A. `task.md` (The Compass)
*   **Purpose:** Tracks *granular* progress.
*   **Format:** Nested checklists. Start with high-level Sprints, then break down into micro-tasks.
*   **Rule:** Never start a cursor session without marking `[x]` on what you just finished in the previous session.

### B. `implementation_plan.md` (The Blueprint)
*   **Purpose:** Forces you to "Think before you Code".
*   **Format:**
    1.  **Goal**: One sentence.
    2.  **Proposed Changes**: List exact files and functions.
    3.  **Verification**: How will we know it works?
*   **Rule:** If the AI cannot write a clear Implementation Plan, it does not understand the task. **Do not proceed.**

### C. `walkthrough.md` (The Logbook)
*   **Purpose:** Proof of work and context anchor.
*   **Format:** "What I did" + "What I verified".
*   **Rule:** Update this *after* a task is verified. It helps the AI remember "Oh, we already fixed the Login bug in Sprint 3".

---

## 3. The Migration phases

### Phase 1: The "Handshake" (Contract)
*   **Goal**: Backend A (Legacy) and Backend B (New) must speak the same JSON/Protocol.
*   **Action**:
    *   Setup Framework (Fiber/Gin/Echo).
    *   Setup Database (GORM/Sqlx).
    *   **Crucial**: Implement the *exact* same helper functions (e.g., `route()`, `csrf`, `auth()->user()`).

### Phase 2: The "Clone" (Domains)
*   **Goal**: Port Feature by Feature.
*   **Order**:
    1.  **Auth**: Nothing works without User ID.
    2.  **Core Domain**: The main thing the app does (e.g., "Notebooks").
    3.  **Sub-Domains**: The strict children (e.g., "Notes").

### Phase 3: The "Stress" (QA & Testing)
*   **Goal**: Prove it works better.
*   **Action**:
    *   **Unit Tests**: Use In-Memory DB (`:memory:`). It's fast and proves logic.
    *   **Load Test**: Simple `go` script to hit endpoints 100x concurrently.
    *   **Edge Cases**: Null values, empty strings, wrong types.

---

## 4. Prompting Strategy (How to drive the AI)

You do not need to write code. You need to write **Intent**.

*   **The "Priming" Prompt:**
    > "Read `task.md` and `implementation_plan.md`. We are in Sprint X. The goal is Y. Do not touch Z."

*   **The "Correction" Prompt:**
    > "You broke the Frontend. The Vue app expects `data.data`, but you sent `data`. Fix the JSON structure."

*   **The "Polishing" Prompt:**
    > "Remove all emojis. Use clear, professional logging labels like `[INFO]` and `[ERROR]`. Check `readme_template.md` for the narrative tone."

---

## 5. Documentation as a Product

Code is for machines. Documentation is for humans.

*   **The Narrative**: Don't just list tech stacks. Tell a story. *Why* did you choose Go? (e.g., "Hardware discipline").
*   **The Alignment**: Ensure `README.md` reflects the *current* reality, not the *planned* reality.

---

**"Software is just hardware that you can change instantly. But the discipline to maintain it should remain the same."**
