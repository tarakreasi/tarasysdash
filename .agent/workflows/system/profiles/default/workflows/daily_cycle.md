# Daily Development Cycle ("The Loop")

## 1. Start (Planning)
- **Goal**: Understand the task.
- **Actions**:
    - Review `task.md` (or creating one).
    - Update **Log**: Open `docs/logs/output_log.md` and check previous entry.
    - **Check Constraints**: Verify infrastructure is running (`docker ps`).

## 2. Work (Execution)
- **Goal**: Implement features/fixes.
- **Actions**:
    - Follow `standards/` for coding.
    - Update `task.md` frequently (Task Boundary).
    - Keep changes concentrated (Atomic).

## 3. Verify (Q&A)
- **Goal**: Ensure quality.
- **Actions**:
    - [ ] **Infrastructure Integrity**:
        - [ ] Check File Ownership: Are new files owned by `user` (not `root`)?
        - [ ] Persistence Check: `cat` key files to verify content matches memory.
    - [ ] **Compliance Check** (The Strict Gate):
        - [ ] RLS: Is tenant isolation enforced?
        - [ ] Encryption: Are files encrypted at rest?
        - [ ] Audit: Are logs generated?
    - Run strict linting (`npm run lint`).
    - Run automated tests (`php artisan test`).
    - Verify build (`npm run build`).

## 4. Sync (Completion)
- **Goal**: Documentation first.
- **Actions**:
    - **1. Update Agent Memory (Task)**: Sync `task.md` -> `docs/logs/agent/task_history.md`.
    - **2. Update Agent Memory (Walkthrough)**: Sync `walkthrough.md` -> `docs/logs/agent/walkthrough_history.md`.
    - **3. Update Human Log**: Write daily entry in `docs/logs/output_log.md`.
    - **4. Update Changelog**: Add entry to `CHANGELOG.md`.
    - **5. Commit**: Use Conventional Commits.
    *NOTE: Skipping any of these 5 steps is a violation of protocol.*
