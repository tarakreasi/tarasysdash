# Implementation Plan - Sprint 2.3: Agent Interface (CLI)

**Status**: ACTIVE
**Sprint**: `docs/dev/sprints/sprint_2_3_interface.md`

## Phase 1: Core CLI Logic (`src/main.py`)
1.  **Imports**:
    -   `argparse` for flags.
    -   `src.agents.graph` for the compiled graph.
    -   `langchain_core.messages`.

2.  **Streaming Loop**:
    -   Implement `chat_loop()` function.
    -   Use `graph.stream(..., stream_mode="updates")` to get real-time feedback.
    -   **Parsing**:
        -   If update contains `content`: Print it blue/green.
        -   If update contains `tool_calls`: Print it yellow (e.g., `[TOOL: list_dir]`).

3.  **Argument Parsing**:
    -   `--prompt "Task"`: Single shot execution.
    -   (Default): Interactive chat mode `>`.

## Phase 2: Polish
1.  **Banner**: Print a cool "ANTIGRAVITY AGENT" ASCII art header on startup.
2.  **System Prompt**: Inject a `SystemMessage` at the start of conversation:
    -   "You are an expert autonomous coder running on local hardware."

## Verification
1.  **Manual Test**:
    -   Run `python src/main.py`.
    -   Check if the aesthetic is pleasing and input works.
    -   *Note*: Intelligence will be powered by the 1.5b model (lighter/faster) for now.

**Success Criteria**:
- `src/main.py` is runnable.
- Interface handles user input loop correctly.
- Graceful exit on Ctrl+C.
