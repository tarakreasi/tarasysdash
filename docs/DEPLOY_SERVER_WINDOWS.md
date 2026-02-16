# Deployment: Tara Server on Windows (Native)

This guide details how to host the **TaraSysDash Server** natively on Windows Server 2019/2022 without Docker or VirtualBox.

## Prerequisites
1.  **Binary**: `server.exe` (Found in `bin/` directory).
2.  **Self-Contained**: The frontend assets are **embedded** into the binary. You do NOT need extra HTML/JS files for production.

> **Note**: SQLite is embedded. You do not need to install a database server.

## Installation Steps

### 1. Installation
1. Copy this entire folder to the server (e.g., `C:\Temp\TaraInstall`).
2. Open PowerShell as **Administrator**.
3. Run:
   ```powershell
   cd C:\Temp\TaraInstall
   .\install_server.ps1
   ```

### 2. Verify
- Open your browser and go to `http://localhost:8080`.
- You should see the dashboard.

### 3. Troubleshooting
- If the service fails to start, check Event Viewer or ensure port 8080 is free.
