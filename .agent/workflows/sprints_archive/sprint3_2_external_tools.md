# Sprint 3.2: External Tools Separation

**Objective**: Clearly separate optional external frameworks from core toolkit.
**Status**: PLANNING

## Backlog
- [ ] Create `OPTIONAL_TOOLS.md` documenting Agent OS and Design OS
- [ ] Add `.toolkitignore` or similar to mark non-essential directories
- [ ] Update root README to explain toolkit scope

## Context
Currently `system/` (Agent OS) and `tools/design-engine/` (Design OS) are mixed with our supervisor code. This sprint creates clear boundaries.

**Decision**: We keep them (they're useful), but document them as "optional enhancements" not "core requirements".
