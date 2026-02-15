# Sprint 2.2: LangGraph Brain (The Cortex)

**Objective**:
Design and implement the State Graph that drives the agent's decision-making loop.

**Role**: AI Architect
**Pre-requisites**: Sprint 2.1 (Tools)
**Status**: PROPOSED

## 1. Scope of Work
### A. State Definition (`src/agents/state.py`)
- [ ] **`AgentState`**: A TypedDict containing:
    -   `messages`: List[BaseMessage] (Chat History)
    -   `current_step`: int (Loop counter)
    -   `scratchpad`: str (Internal monologue)

### B. Graph Topology (`src/agents/graph.py`)
- [ ] **Nodes**:
    -   `reason`: LLM decides what to do next.
    -   `action`: Executes the selected tool (using Sprint 2.1 tools).
- [ ] **Edges**:
    -   Conditional edge from `reason` -> `action` (if tool call) OR `end` (if answer).
    -   Edge from `action` -> `reason` (Loop back).

### C. LLM Binding
- [ ] Bind `qwen2.5-coder:7b` (or 1.5b) to the tools defined in Sprint 2.1.

## 2. Compliance Gates
- **Loop Limit**: Graph must abort after N steps (e.g., 10) to prevent infinite billable/compute loops.
- **Persistence**: Usage of `MemorySaver` (checkpointer) to enable "Time Travel" debugging.

## 3. Deliverables
- `src/agents/state.py`
- `src/agents/graph.py`
