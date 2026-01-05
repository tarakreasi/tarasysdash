# Sprint 3: Windows Reliability & Metadata

**Goal:** Make the agent "Smart" about its environment.

## 1. Backlog Items

### 3.1. Windows Service Monitoring
-   **Status:** *New Investigation.*
-   **Tasks:**
    -   [Agent] Research `gopsutil/process` or `golang.org/x/sys/windows/svc`.
    -   [Config] Allow defining "Critical Services" list (e.g., "RecordingServer.exe", "MilestoneService").
    -   [Agent] Report boolean `service_running` status.

### 3.2. Agent Metadata & Identity
-   **Status:** *Basic.*
-   **Tasks:**
    -   [Agent] Improve Hostname/OS detection.
    -   [Agent] Add CLI flag `--rack="Rack A"` during install.
    -   [API] Store and index agents by `rack_location`.

### 3.3. Self-Healing (Nice to have)
-   **Tasks:**
    -   [Agent] Use Windows Service Manager (SCM) to auto-restart the Agent if it crashes.

## 2. Deliverables
-   Agent reports if VMS software is running.
-   Agents are correctly tagged with Rack IDs.
