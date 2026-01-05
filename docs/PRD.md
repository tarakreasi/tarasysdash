# Product Requirement Document (PRD): TaraSysDash (VMS Edition)

## 1. Introduction
**TaraSysDash** is a lightweight system monitoring solution designed for critical video surveillance environments. It provides real-time visibility into the health of Windows-based Video Management System (VMS) servers across multiple racks.

## 2. Problem Statement
Field Engineers overseeing large VMS deployments (3+ racks, ~30 servers) struggle to monitor system health manually. RDP-ing into servers is inefficient. Existing tools are either too expensive, too heavy, or require cloud connectivity (which is often restricted).

## 3. Operations & User Persona
-   **Primary User:** Field Engineer ([See User Persona](./user_persona.md))
-   **Environment:** 
    -   OS: Windows Server 2019/2022, Windows 10/11.
    -   Network: High throughput (>1Gbps constant traffic), Air-gapped/Private LAN.
    -   Scale: 3 Racks, mixed roles (Recorder, Management, Storage).

## 4. Functional Requirements

### 4.1. Agent (Windows)
-   **[P0] Low Overhead:** Must consume <1% CPU and <100MB RAM. VMS software is resource-hungry; the agent must be invisible.
-   **[P0] Metric Collection:**
    -   **CPU:** Total Usage %.
    -   **Memory:** Used/Total RAM.
    -   **Disk:** Free space % for ALL mounted drives (C:, D:, E: etc.). *Critical for Recording drives.*
    -   **Network:** Bandwidth usage (Mbps In/Out) per interface. *Critical for verifying camera stream throughput.*
    -   **Uptime:** System uptime.
-   **[P1] Auto-Discovery:** Agent auto-registers with the server via Handshake (Hostname, OS, IP).
-   **[P1] Metadata Tags:** Ability to tag agents with "Rack Location" (e.g., Rack A, U12).
-   **[P2] Service Monitoring:** Check if specific VMS services (e.g., "Milestone Recording Server", "Genetec Server") are running.

### 4.2. Server & API
-   **[P0] Ingestion:** Handle metrics push from 50+ agents every 1-5 seconds.
-   **[P0] Persistence:** Store metrics locally (SQLite WAL mode) with retention policy (e.g., 7 days).
-   **[P1] API:** Expose JSON endpoints for:
    -   Current Snapshot (Live Dashboard).
    -   Historical Trends (Charts).
    -   Rack View (Group by Rack ID).

### 4.3. Dashboard (Web UI)
-   **[P0] Rack View:** Visual representation of servers in their physical racks.
-   **[P0] Email Alerts:**
    -   Send email via external SMTP (e.g., Gmail) when thresholds are breached.
    -   Configurable: SMTP Host, Port, Username, Password (App Password), To/From Address.
    -   **Critical Alerts Only:** Reduce noise. Only send on "Offline" or "Disk < 5%".
    -   **Visual Health Indicators:**
        -   Green: OK.
        -   Yellow: Warning (CPU > 80%, Disk < 10%).
        -   Red: Critical (Offline, Disk < 2%).
-   **[P1] Network Graphs:** Line charts showing incoming throughput (vital to know if cameras are connected).

## 5. Non-Functional Requirements
-   **Reliability:** Agent must auto-restart on failure.
-   **Offline Operation:** System must function 100% without Internet.
-   **Security:** Token-based authentication for Agent-Server communication (Implemented).

## 6. Gap Analysis (Current vs Target)
| Feature | Current Implementation (Codebase) | Target (VMS Edition) | Action |
| :--- | :--- | :--- | :--- |
| **OS Support** | Linux/Windows (Basic) | Windows Server Detailed | Verify Windows specific counters. |
| **Network Metrics** | Schema exists, Collector Logic **MISSING** | **Required** (Mbps In/Out) | Implement network collector logic. |
| **Disk Monitoring** | Root path only | **Multi-Drive Support** | Support iterating all logical drives. |
| **Rack Grouping** | Basic Metadata field | **Rack UI Visualization** | Enhance Frontend & Grouping Logic. |
| **Alerting** | None | **Email Alerts (SMTP/Gmail)** | Implement SMTP sender with Auth. |
