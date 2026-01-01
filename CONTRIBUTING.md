# Contributing to taraSysDash

Thank you for your interest in contributing to `taraSysDash`! This document outlines the standards and workflows for this project.

## Development Workflow

1.  **Fork & Clone**: Fork the repository and clone it locally.
2.  **Branching**: Create a new branch for your feature or fix.
    - Feature: `feat/your-feature-name`
    - Fix: `fix/bug-description`
3.  **Commit Messages**: We follow [Conventional Commits](https://www.conventionalcommits.org/).
    - `feat: ...` for new features.
    - `fix: ...` for bug fixes.
    - `docs: ...` for documentation.
    - `chore: ...` for maintenance tasks.

## Code Style

- **Go**: Always run `go fmt ./...` before committing.
- **Linting**: Run `make lint` to check for issues (uses `golangci-lint` if installed).
- **Naming**: Follow standard Go naming conventions (PascalCase for exported, camelCase for internal).

## Running Locally

### Backend
```bash
# Install dependencies
go mod download

# Run Server
go run cmd/server/main.go
```

### Agent
```bash
# Run Agent
SERVER_URL=http://localhost:8080 ./bin/tara-agent
```

## Pull Requests

- Describe your changes clearly.
- Link to any related issues.
- Ensure all tests pass (manual verification expected for now).
