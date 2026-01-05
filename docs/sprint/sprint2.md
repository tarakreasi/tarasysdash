# Sprint 2: Critical Alerting (Email/SMTP)

**Goal:** Proactive notification. The system calls the user, not the other way around.

## 1. Backlog Items

### 2.1. Email Notification Engine
-   **Status:** *New Requirement.*
-   **Tasks:**
    -   [Backend] Create `internal/alert` package.
    -   [Backend] Implement SMTP Client (Host, Port, Auth).
    -   [Config] Add ENV Vars: `SMTP_HOST`, `SMTP_USER`, `SMTP_PASS`, `ALERT_RECIPIENTS`.

### 2.2. Critical Threshold Logic
-   **Tasks:**
    -   [Backend] Create a background "Tick" (e.g., every 60s).
    -   [Logic] Check Last Heartbeat (Offline > 60s).
    -   [Logic] Check Disk Space (Any drive < 5%).
    -   [Logic] Check CPU sustained (> 90% for 5 mins).

### 2.3. Anti-Spam (Debounce)
-   **Tasks:**
    -   [Logic] Implement "Cooldown" mechanism. If email sent for Agent-X, wait 60 mins before sending again.
    -   **Template:** "🚨 CRITICAL: Server [Hostname] is [OFFLINE/DISK FULL]"

## 2. Deliverables
-   Backend service capable of sending emails.
-   Verified "Offline" email received when Agent is killed.
