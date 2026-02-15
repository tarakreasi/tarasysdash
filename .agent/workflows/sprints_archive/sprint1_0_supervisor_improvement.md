# Sprint 1.0: Supervisor CLI & Artifacts

**Objective**: Upgrade the Supervisor CLI to provide structured JSON output and generated artifacts, making it the perfect tool for External Agentic AIs.

**Status**: PLANNING

## 1. Context
The current supervisor outputs human-readable logs (colored text). As an automated agent, I need machine-readable output (JSON) to parse the status, errors, and progress without regex magic.

## 2. Technical Strategy
-   **Modify `supervisor_cli.py`**: Add a `--json` flag or default to JSON output when in non-interactive mode.
-   **Artifacts**: Generate `.agent/automation/state.json` after every cycle.
-   **Error Handling**: Ensure exit codes map to specific failure types (1=Config, 2=Verification, 3=System).

## 3. Backlog

### CLI Improvements
- [ ] **Implement JSON Logger**: Create `src/core/json_logger.py` to handle structured logging.
- [ ] **Update Supervisor CLI**: Modify `supervisor_cli.py` to support `--format=json`.

### State Management
- [ ] **State Artifact**: Ensure `StateManager` dumps current state to `.agent/automation/state.json` on every change.
- [ ] **Completion Report**: Generate `artifacts/report_[timestamp].json` upon sprint completion.

### Verification
- [ ] **Strict Config Check**: Add startup check to crash if `AI_ENABLED` is `True` (enforce deterministic mode).
