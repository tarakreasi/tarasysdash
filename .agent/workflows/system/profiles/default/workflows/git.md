# Git Workflow Standards

## 1. Commit Messages (Conventional Commits)
Format: `<type>(<scope>): <description>`

- **Types**:
    - `feat`: New feature.
    - `fix`: Bug fix.
    - `docs`: Documentation only.
    - `style`: Formatting, missing semi-colons, etc.
    - `refactor`: Code change that neither fixes a bug nor adds a feature.
    - `test`: Adding missing tests of correcting existing tests.
    - `chore`: Infrastructure, build process, or aux tool changes.

## 2. Artifact Synchronization
**CRITICAL**: Before every commit, Agent Artifacts MUST be synced to the repository history.
- Source: `<appDataDir>/brain/<conversation-id>/*.md`
- Target: `docs/logs/agent/*.md`

## 3. Branching (Simplified)
- **Master/Main**: Production-ready code.
- **Feature Branches**: `feat/feature-name` (Optional for solo dev, but recommended).
