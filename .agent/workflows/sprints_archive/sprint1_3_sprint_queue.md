# Micro-Sprint 1.3: Sprint Queuing & Auto-Advance

**Objective**: Enable the Supervisor to automatically load the next sprint from `docs/dev/sprints/` upon completion of the current one, allowing for "Batch Planning".

**Status**: PLANNING

## Backlog
- [ ] Update `StateManager` in `src/supervisor/state_manager.py` to include `advance_to_next_sprint()` logic.
- [ ] Update `SprintSupervisor` in `src/supervisor/supervisor.py` to trigger advancement after `REVIEW` state.
- [ ] Create a dummy `sprint1_4_test.md` to verify the transition works.

## Technical Implementation
1.  **Scanning**: `StateManager` lists all `.md` files in `docs/dev/sprints/`.
2.  **Sorting**: Files are sorted alphabetically (e.g., `sprint1_1` < `sprint1_2`).
3.  **Matching**: Identify the current sprint's detailed file.
4.  **Advancing**:
    *   Read content of the *next* file.
    *   Overwrite `current_sprint.md`.
    *   Reset internal state to continue loop.
