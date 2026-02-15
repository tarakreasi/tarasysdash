# Sprint 3.3: Deployment System

**Objective**: Create automated deployment scripts for installing toolkit to new projects.
**Status**: PLANNING

## Backlog
- [ ] Create `INSTALL.md` with manual installation steps
- [ ] Create `scripts/deploy.sh` for automated deployment
- [ ] Add `scripts/validate.sh` to check Python deps and paths

## Technical Approach
```bash
# scripts/deploy.sh usage:
./scripts/deploy.sh /path/to/target/project

# What it does:
# 1. Copy automation/ to target/.agent/automation/
# 2. Copy workflows/ to target/.agent/workflows/
# 3. Create target/docs/dev/sprints/ if needed
# 4. Setup .venv and install deps
# 5. Run validate.sh
```

## Validation Checklist
- [ ] Python 3.12+
- [ ] Git installed
- [ ] Required Python packages
- [ ] Correct directory structure
