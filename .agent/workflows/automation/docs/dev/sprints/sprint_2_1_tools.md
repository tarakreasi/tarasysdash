# Sprint 2.1: Agent Tooling (The Hands)

**Objective**:
Build the set of robust, safe tools that the Autonomous Agent will use to interact with the filesystem and environment.

**Role**: Security Engineer
**Pre-requisites**: Sprint 1.3 (LLM functional)
**Status**: COMPLETE

## 1. Scope of Work
### A. File System Tools (`src/tools/fs.py`)
- [ ] **`read_file`**: Safe reading of text files (limit size to prevent context overflow).
- [ ] **`write_file`**: Atomic writing to files (create parent dirs).
- [ ] **`list_dir`**: Recursive or flat listing.

### B. Execution Tools (`src/tools/shell.py`)
- [ ] **`run_shell`**: A restricted shell executor.
    -   **Constraint**: Timeout enforcement (e.g., 10s).
    -   **Constraint**: Block dangerous commands (`rm`, `mv` on critical paths) if possible, or just rely on user confirmation mechanism later.

### C. Tool Registry
- [ ] **Export**: Expose these as LangChain `StructuredTool` objects so the LLM can bind to them.

## 2. Compliance Gates
- **Safety**: Tools must not allow escaping the project root (Directory Traversal prevention).
- **Type Hints**: All tools must use Pydantic models for arguments.

## 3. Deliverables
- `src/tools/fs.py`
- `src/tools/shell.py`
- `tests/test_tools.py` (Unit tests for safety)
