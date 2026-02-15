# Sprint 3.5: Validation & Polish

**Objective**: Test deployment system and finalize documentation.
**Status**: PLANNING

## Backlog
- [ ] Create `tests/test_deployment.sh` for deploy script validation
- [ ] Test toolkit in empty directory (clean install)
- [ ] Update `CHANGELOG.md` with Sprint 3.x series

## Validation Tests

### Test 1: Fresh Deploy
```bash
# Create temp directory
mkdir /tmp/test-toolkit && cd /tmp/test-toolkit
# Deploy
/path/to/new_agent/scripts/deploy.sh .
# Verify structure
[ -d .agent/automation ] && echo "PASS" || echo "FAIL"
```

### Test 2: Existing Git Repo
```bash
# Init repo first
git init test-existing && cd test-existing
# Deploy should not break git
/path/to/new_agent/scripts/deploy.sh .
git status # Should be clean or show only .agent/ changes
```

### Test 3: Python Dependencies
```bash
# After deploy, activate venv
source .agent/automation/.venv/bin/activate
# Run supervisor status (should not crash)
python .agent/automation/supervisor_cli.py status
```

## Success Criteria
- All 3 tests pass
- Documentation is coherent
- Toolkit is portable (no hardcoded paths)
