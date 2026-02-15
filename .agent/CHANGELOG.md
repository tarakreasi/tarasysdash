# Changelog

All notable changes to the Semi-Agentic Toolkit.

## Sprint 3.x Series: Toolkit Integration (2026-01-16)

The toolkit has been refactored into a portable, installable product.

### Added
- **Semi-Agentic Architecture**: Defined in `docs/ARCHITECTURE.md`.
- **Deployment System**: `scripts/deploy.sh` for automated installation.
- **Validation**: `tests/test_deployment.sh` and `scripts/validate.sh` for health checks.
- **Workflow Protocols**: Added `/handoff` protocol for AI session management.
- **Documentation**:
    - `INSTALL.md`: Installation guide.
    - `OPTIONAL_TOOLS.md`: Documentation for external frameworks.
    - `INTEGRATION_EXAMPLES.md`: Guides for Greenfield/Brownfield/Shared integration.

### Changed
- **Rebranding**: Renamed project to "Semi-Agentic Toolkit" (v3.0).
- **Core Separation**: Clearly separated `automation` engine from `system` (Agent OS) and `tools` (Design OS).
- **Deployment**: Excludes `__pycache__` and `.venv` during sync.

--- (Previous Entries Below) ---

## Sprint 1.x Series (Supervisor Optimization)
(See previous history)
# Changelog - Sprint 1.x Series (Supervisor Optimization)

All notable changes to the `new_agent` supervisor system.

## Sprint 1.3: Sprint Queuing (2026-01-15)
### Added
- **Auto-Advance**: `StateManager.advance_to_next_sprint()` enables automatic sprint progression
- **Batch Planning**: Create multiple sprint files and supervisor will execute them sequentially
- Files are sorted alphabetically for predictable execution order

### Changed
- Supervisor no longer stops after sprint completion - enters standby mode instead
- Sprint directory path corrected to `docs/dev/sprints/`

## Sprint 1.2: JSON CLI Support (2026-01-15)
### Added
- `--json` flag for `supervisor_cli.py start` command
- `JSONLogger` class in `src/core/json_logger.py` for structured output
- Machine-readable logs for external agent integration

### Changed
- `SprintSupervisor` accepts `json_mode` parameter
- Terminal output switches between human-readable (colored) and JSON based on flag

## Sprint 1.1: Structured Logging (2026-01-15)
### Added
- `src/core/json_logger.py` module
- `JSONFormatter` for consistent log structure
- Timestamp, level, message, and module metadata in all logs

## Sprint 1.0: Supervisor Improvement Foundation (2026-01-15)
### Added
- Sprint definition framework
- Micro-sprint planning methodology
- Documentation consolidation (`SPRINT_GUIDE.md`, workflow files)

### Removed
- Duplicate documentation (`MICRO_SPRINT_GUIDE.md`, `SPRINT_TEMPLATE.md`, `SPRINT_RULES.md`)
- Merged into unified `SPRINT_GUIDE.md` and `.agent/workflows/`

## Sprint 1.4: Always-On Mode (2026-01-15)
### Changed
- **Non-Fatal Errors**: `ERROR_HALT` and `WAITING_USER` states no longer terminate supervisor
- Supervisor enters 10-second sleep/retry loop instead of exiting
- Maximum retries trigger standby mode instead of halt

### Benefits
- Supervisor runs indefinitely as background daemon
- Automatically picks up new sprints or fixes without restart
- True "Always-On" reactive system
