# User Persona: Field Engineer (VMS Specialist)

## Profile
**Name:** Budi "The Watcher" Santoso  
**Role:** Field Engineer / System Integrator  
**Experience:** 5-10 years in CCTV, Security Systems, and IT Infrastructure.  
**Location:** On-site (Server Room/Command Center) & Remote Access to Sites.

## Responsibilities
Budi is responsible for the uptime and performance of a critical **Video Management System (VMS)** deployment.
-   **Scope:** 3 Physical Server Racks.
-   **Assets:** Total ~52 mixed servers (Recording Servers, NVRs, Management Servers).
-   **OS Breakdown:** Mixed environment of Windows Server 2019/2022 and Ubuntu Linux NVRs.

## Goals
1.  **Zero Downtime Recording:** Ensure video is *always* being written to disk. Gaps in recording are unacceptable.
2.  **Proactive Maintenance:** Identify "hot" disks or memory leaks *before* the server crashes.
3.  **Quick Troubleshooting:** Instantly know if it's Network, CPU, or Disk I/O across mixed OS environments.

## Pain Points
-   **"Blind" Spots:** Cannot physically check 50+ servers continuously. 
-   **Mixed OS Management:** Monitoring Linux NVRs and Windows Recording servers simultaneously is a headache.
-   **Disk Full Surprises:** If any recording partition (C:\ or /) fills up, the system crashes.

## Needs from TaraSysDash
-   **Single Pane of Glass:** See status of ALL 3 racks (Windows & Linux) in one screen.
-   **Cross-Platform Agent:** Lightweight native performance on both Linux and Windows.
-   **Immediate Red Flags:** Visual indicators (Red/Green) for Offline agents or Low Disk (<10%).

## Technical Environment
-   **Network:** Private Isolated Network (LAN/VLAN), no Internet access for servers.
-   **Hardware:** Dell/HP Enterprise Servers, High-performance Storage Arrays (RAID 6/10/60).
-   **Constraints:** Cannot install heavy agents (like SolarWinds/Datadog) due to cost and resource overhead.
