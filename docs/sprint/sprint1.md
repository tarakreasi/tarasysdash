# Sprint 1: Close the Data Gap (Core Metrics)

**Goal:** Ensure the Agent collects **ALL** vital VMS data (Network + Multi-Disk). Without this, the system is blind.

## 1. Backlog Items

### 1.1. Network Monitoring (High Priority)
-   **Status:** *Missing in codebase.*
-   **Tasks:**
    -   [Backend] Implement `gopsutil/net` in `internal/collector`.
    -   [Backend] Logic to calculate `Mbps` (delta bytes / delta time).
    -   [API] Update `/api/v1/metrics` payload to support `bytes_in`, `bytes_out`.
    -   **Validation:** Verify non-zero values during file transfer on Windows.

### 1.2. Multi-Drive Disk Monitoring
-   **Status:** *Partial (Root only).*
-   **Tasks:**
    -   [Backend] Refactor `SystemMetrics.DiskFreePercent` to `[]DiskStat` (List of drives).
    -   [Backend] Loop through all partitions using `gopsutil/disk`.
    -   [DB] Update SQLite schema (likely a new table `disk_metrics` or JSON column) to store per-drive data.
    -   **Validation:** Agent reports C: (OS) and D: (Recordings) separately.

## 2. Deliverables
-   Agent binary (v0.2.0) with new collectors.
-   API endpoint returning full metrics JSON.
