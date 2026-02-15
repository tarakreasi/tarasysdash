# Automation Approval Policy

This document defines the **Rules of Engagement** for the Automation Layer.

## 1. Syntax & Linting
- **Policy**: `STRICT`.
- **Action**: If a file fails `lint` or `type-check`, the automation MUST pause and fix it. It cannot call a task "Done" with lint errors.

## 2. Test Coverage
- **Policy**: `LOOSE`.
- **Action**: Tests are encouraged but not blocking *unless* specialized in the Sprint Plan.
- **Exception**: "Core Physics" logic (Zoom/Pan) MUST pass regression tests.

## 3. UI/Visuals
- **Policy**: `HUMAN_REVIEW`.
- **Action**: The Automation Layer cannot "see" generic aesthetics.
- **Protocol**: After implementing a UI component, the Automation MUST:
    1.  Generate a screenshot (if capable) or description.
    2.  Ask the User: "Does this look right?"
    3.  **Wait** for explicit UI approval.

## 4. Dependencies
- **Policy**: `ASK_FIRST`.
- **Action**: Do not install new `npm` or `composer` packages without checking if they are heavy or redundant.

## 5. File System
- **Policy**: `ISOLATED`.
- **Action**: Modification inside `./app`, `./resources`, `./tests` is **ALLOWED**.
- **Action**: Modification of root configs (`vite.config.js`, `webpack.mix.js`) requires **CAUTION**.
- **Action**: Modification of system files (`/etc/`, `/var/`) is **FORBIDDEN**.
