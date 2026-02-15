# Sprint 2.3: Agent Interface (The Mouth)

**Objective**:
Create the Command Line Interface (CLI) to interact with the agent. This is the entry point for the user.

**Role**: Application Developer
**Pre-requisites**: Sprint 2.2
**Status**: COMPLETE

## 1. Scope of Work
### A. Main Entry Point (`src/main.py`)
- [ ] **CLI Argument Parser**:
    -   `--task`: The prompt.
    -   `--model`: Override model selection.
    -   `--verbose`: Show internal thought process.
- [ ] **Interactive Mode**: A simple `while True` loop for chat-like interaction.

### B. Streaming Output
- [ ] **Pretty Printing**: Stream tokens to console in real-time so it feels responsive.
- [ ] **Tool usage display**: Show when a tool is being called (e.g., `[RUNNING COMMAND: ls -F]`).

## 2. Compliance Gates
- **UX**: Latency between "Enter" and "First Token" must be minimized.
- **Error Handling**: Graceful exit on Ctrl+C.

## 3. Deliverables
- `src/main.py`
- Verified end-to-end "Hello World" task execution.
