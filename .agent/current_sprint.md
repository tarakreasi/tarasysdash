# Current Sprint: Sprint 4.3: Auto-Developer Agent

**Parent Sprint**: Sprint 4 (Librarian Agent)
**Objective**: Build the "Brain" of the autonomous agent effectively. It must utilize the Librarian (Sprint 4.2) to understand code and basic file operations to modify it.

**Status**: REVIEW

## 📋 Micro-Sprints Breakdown

This sprint is divided into granular micro-sprints to ensure the "Brain" is built systematically.

### [ ] Sprint 4.3.1: Agent Tooling Layer
**Focus**: capabilities.
- Implement `AgentTools` class.
- Wrap Librarian `query` as a tool: `search_codebase`.
- Implement FileSystem tools: `read_file`, `write_file`, `list_files`.
- **Artifact**: `sprint4_3_1_tools.md`

### [ ] Sprint 4.3.2: Reasoning Engine (The Brain)
**Focus**: Decision making.
- Implement `AgentBrain` or `DeveloperAgent`.
- Define the System Prompt (Persona, Constraints, Output Format).
- Implement the "Think -> Plan -> Act" loop.
- **Artifact**: `sprint4_3_2_reasoning.md`

### [ ] Sprint 4.3.3: Action Executor
**Focus**: Doing the work.
- Parse LLM responses (JSON/XML).
- Execute the selected tools.
- Handle tool output/errors and feed back to Brain.
- **Artifact**: `sprint4_3_3_executor.md`

### [ ] Sprint 4.3.4: CLI & Full Loop Verification
**Focus**: User Interaction.
- Create `dev_agent_cli.py`.
- Verify: "Agent, create a hello_world.py file" -> Agent searches, plans, writes.
- **Artifact**: `sprint4_3_4_integration.md`
