# Loop Controller: The Heartbeat

**Function**: State Machine for Continuous Sprint Execution.

## State Map

### STATE: IDLE
- **Trigger**: User command "Start Automation".
- **Transition**: -> `STATE: SCANNING`.

### STATE: SCANNING
- **Action**: detailed read of `.agent/current_sprint.md`.
- **Logic**:
    - **If** unassigned task exists -> `STATE: PLANNING`.
    - **If** all tasks done -> `STATE: REVIEW`.
    - **If** blocked -> `STATE: WAITING_USER`.

### STATE: PLANNING
- **Action**: Generate `implementation_plan.md` for *single* task.
- **Check**: Run `approval_policy.md` check.
- **Transition**: -> `STATE: BUILDING`.

### STATE: BUILDING
- **Action**: Write Code.
- **Mode**: "Blind Mode" (Trust the plan).
- **Transition**: -> `STATE: VERIFYING`.

### STATE: VERIFYING
- **Action**: Run Verification (Tests/Compile).
- **Logic**:
    - **PASS** -> Trigger `Mark Done` -> Return to `STATE: SCANNING`.
    - **FAIL** -> Increment `RetryCount`.
        - If `RetryCount` < 3 -> `STATE: HEALING`.
        - If `RetryCount` >= 3 -> `STATE: ERROR_HALT`.

### STATE: HEALING
- **Action**: Read Error Log -> Propose Fix -> Apply Fix.
- **Transition**: -> `STATE: VERIFYING`.

### STATE: REVIEW (Sprint Complete)
- **Action**: Compile `walkthrough.md`.
- **Output**: "Sprint Complete. Awaiting User Sign-off."
- **Transition**: -> `STATE: IDLE`.
