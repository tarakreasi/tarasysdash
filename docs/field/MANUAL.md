# Field Engineer Manual: Tara Agent Installation

**Target Audience**: Field Engineers / Technicians
**Goal**: Install the Monitoring Agent on a Windows Server (2019/2022).

---

## 🛑 Preparation (Before you go to site)

1. **Get the Files**:
   You should have a USB drive or a Shared Folder with exactly these 2 files:
   - `agent-windows-amd64.exe` (The program)
   - `install.ps1` (The installer script)

2. **Know the Server IP**:
   - Ask the Network Admin for the **Tara Server IP**.
   - Example: `http://192.168.100.50:8080`

---

## 🚀 Installation Steps (On the Windows Server)

### Step 1: Copy Files
1. Create a folder: `C:\Tara`
2. Copy both `agent-windows-amd64.exe` and `install.ps1` into `C:\Tara`.

### Step 2: Edit Configuration
1. Right-click `install.ps1` -> **Edit** (opens in Notepad or ISE).
2. Look for line 7:
   ```powershell
   $ServerURL = "http://YOUR_SERVER_IP:8080"
   ```
3. Change `YOUR_SERVER_IP` to the actual IP.
   - Example: `$ServerURL = "http://192.168.1.5:8080"`
4. **Save** and Close.

### Step 3: Run Installer
1. Press `Windows Key`, type **PowerShell**.
2. Right-click **Windows PowerShell** -> **Run as Administrator**.
3. Type the following commands:
   ```powershell
   cd C:\Tara
   Set-ExecutionPolicy Unrestricted -Scope Process
   .\install.ps1
   ```
4. Type `Y` (Yes) if asked to confirm execution.

### Step 4: Verify Success
1. You should see "Installation Complete!".
2. Open **Services** (Type `services.msc` in Start Menu).
3. Find **Tara Infrastructure Agent**.
4. Check that **Status** says **Running**.

---

## ❓ Troubleshooting

**"Script cannot be loaded because running scripts is disabled..."**
- Solution: You missed the `Set-ExecutionPolicy` command in Step 3. Run it again.

**"The agent is not showing on the Dashboard"**
- Check if the Server Firewall is blocking Port 8080.
- Try pinging the server: `ping 192.168.1.5`

**"Service starts then stops immediately"**
- The config might be wrong.
- Check the log file in `C:\Program Files\TaraAgent\agent.log`.
