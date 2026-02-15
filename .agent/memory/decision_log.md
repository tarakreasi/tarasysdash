# 📚 Decision Log
Record significant architectural choices here.

## [2026-01-16] Workflow Architecture Overhaul
- **Context**: Optimizing agent workflows for precision and scalability.
- **Decision**: Adopt "Active Librarian" memory system and TDD-enforced Micro-sprints.
- **Reason**: Previous workflows allowed vague specs; new system enforces "Silent Execution" by Qwen.
- **Components**:
  - `/agent-research`: Added Clean Architecture template.
  - `/agent-architect`: Defines Split Workflow (BE/FE).
  - `/agent-spec`: Adds TDD Strategy.
  - `/agent-microsprint`: Enforces Test-First pair.
