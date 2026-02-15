# Sprint 3.0: Toolkit Integration & Cleanup Strategy

**Objective**: Optimize `new_agent` structure for seamless integration as a reusable toolkit across projects.

**Status**: PLANNING

## Analysis Summary

### Current State Discovery:
1. **Core Supervisor** (~2200 LOC Python):
   - Deterministic execution engine ✅
   - Auto-git, Auto-advance, Always-On ✅
   - JSON output for machine integration ✅

2. **External Components** (Not Ours):
   - `system/` - Agent OS by Builder Methods (spec-driven workflows)
   - `tools/design-engine/` - Design OS (UI planning tool)
   - These are **third-party frameworks** we inherited

3. **Documentation Scattered**:
   - `PM.md` - Old autonomous mode docs (partially obsolete)
   - `IMPROVEMENT_PROPOSAL.md` - Multi-agent vision (not implemented)
   - `automation/README.md` - Outdated Quick Start
   - `HOW_TO_USE.md` - Current but needs update

4. **Nested `.agent` Issue**:
   - `new_agent/.agent/` exists inside toolkit folder
   - Should be flat: toolkit goes INTO `.agent/`, not contain it

## Execution Plan (Micro-Sprints)

This master sprint is divided into 5 micro-sprints for manageable execution:

1. **Sprint 3.1: Documentation Architecture** 
   - Create ARCHITECTURE.md
   - Update PM.md to deterministic mode
   - Archive IMPROVEMENT_PROPOSAL.md

2. **Sprint 3.2: External Tools Separation**
   - Document Agent OS and Design OS as optional
   - Create boundaries between core and extras

3. **Sprint 3.3: Deployment System**
   - Build deploy.sh automation
   - Create INSTALL.md guide
   - Add validation scripts

4. **Sprint 3.4: Integration Examples**
   - Real-world usage scenarios
   - Update HOW_TO_USE.md
   - Quick start guides

5. **Sprint 3.5: Validation & Polish**
   - Test deployment in clean environments
   - Final documentation review
   - CHANGELOG update

## Integration Vision

### What This Toolkit Provides:
1. **Automated Project Manager**: Sprint planning → Git commits
2. **Verification Engine**: File existence, build checks
3. **JSON API**: Machine-readable for external AI integration
4. **Workflow System**: `/sprint` and `/agent` protocols

### What Users Bring:
1. Their own codebase
2. Their sprint definitions (`docs/dev/sprints/*.md`)
3. External AI (like me) to write actual code

### Separation of Concerns:
```
User's Project Root/
├── .agent/                    # ← Toolkit deployment
│   ├── automation/            # Our supervisor
│   ├── workflows/             # Our protocols
│   └── current_sprint.md      # State file
├── docs/dev/sprints/          # User's sprint plans
├── src/                       # User's code
└── [their project files]
```

## Context
This sprint prepares `new_agent` to become a **portable, reusable toolkit** rather than a standalone project. Think of it as "Git for Sprint Management" - users install it once, use it everywhere.
