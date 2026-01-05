# User Persona: Field Engineer (VMS Specialist)

## Profile
**Name:** Budi "The Watcher" Santoso  
**Role:** Field Engineer / System Integrator  
**Experience:** 5-10 years in CCTV, Security Systems, and IT Infrastructure.  
**Location:** On-site (Server Room/Command Center) & Remote Access to Sites.

## Responsibilities
Budi is responsible for the uptime and performance of a critical **Video Management System (VMS)** deployment.
-   **Scope:** 3 Physical Server Racks.
-   **Assets:** Total ~15-30 Windows Servers (Recording Servers, Management Servers, Failover Servers).
-   **OS Breakdown:** Mixed environment of Windows Server 2019, Windows Server 2022, and some legacy Windows 10/11 IoT Enterprise units.

## Goals
1.  **Zero Downtime Recording:** Ensure video is *always* being written to disk. Gaps in recording are unacceptable.
2.  **Proactive Maintenance:** Identify "hot" disks or memory leaks *before* the server crashes.
3.  **Quick Troubleshooting:** When a camera goes black or a server lags, instantly know if it's Network, CPU, or Disk I/O.

## Pain Points
-   **"Blind" Spots:** Cannot physically check 30 servers continuously. RDP-ing into each one to check Task Manager is slow and disruptive.
-   **Disk Full Surprises:** VMS generates massive logs and video files. If the OS drive fills up, the VMS crashes.
-   **Resource Contention:** Windows Updates or Anti-Virus scans sometimes spike CPU/Disk, causing frame drops.
-   **Network Bottlenecks:** High megapixel cameras flood the NIC cards. Saturation leads to video artifacts.

## Needs from TaraSysDash
-   **Single Pane of Glass:** See status of ALL 3 racks in one screen.
-   **Immediate Red Flags:** Visual indicators (Red/Green) for Offline agents, High CPU (>90%), or Low Disk (<10%).
-   **Windows Native Metrics:** Accurate reporting of Windows-specific counters (e.g., Disk Queue Length is vital for VMS).
-   **No-Touch Deployment:** Simple "download and run" agent installation on Windows machines.

## Technical Environment
-   **Network:** Private Isolated Network (LAN/VLAN), no Internet access for servers.
-   **Hardware:** Dell/HP Enterprise Servers, High-performance Storage Arrays (RAID 6/10/60).
-   **Constraints:** Cannot install heavy agents (like SolarWinds/Datadog) due to cost and resource overhead.
