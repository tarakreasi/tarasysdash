# Sprint 3.4: Integration Examples

**Objective**: Provide real-world examples of toolkit integration scenarios.
**Status**: PLANNING

## Backlog
- [ ] Update `HOW_TO_USE.md` with "Integration Scenarios" section
- [ ] Create `docs/INTEGRATION_EXAMPLES.md` with 3 scenarios
- [ ] Add "Quick Start from Scratch" guide

## Integration Scenarios

### Scenario 1: New Project
```bash
mkdir my-new-project && cd my-new-project
git init
/path/to/new_agent/scripts/deploy.sh .
# Follow prompts, toolkit ready
```

### Scenario 2: Existing Project
```bash
cd existing-project
/path/to/new_agent/scripts/deploy.sh .
# Toolkit added, preserves existing files
```

### Scenario 3: Shared Toolkit (Advanced)
```bash
# Keep toolkit in one place, symlink from multiple projects
ln -s ~/toolkit/.agent ~/project1/.agent
ln -s ~/toolkit/.agent ~/project2/.agent
# Each project has own sprints, shares automation
```
