# Deployment: Tara Server on Windows (Native)

This guide details how to host the **TaraSysDash Server** natively on Windows Server 2019/2022 without Docker or VirtualBox.

## Prerequisites
1.  **Binary**: `server-windows-amd64.exe` (Built via `make build-server-windows`).
2.  **Frontend Files**: The `web/dist` folder (if serving frontend from the same binary, though current dev setup uses separate Vite. **For Production**, we usually serve static files or use a reverse proxy. *For this MVP guide, we assume running the backend exe directly*).

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
