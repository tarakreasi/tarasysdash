# Tara Agent Installer for Windows
# Run as Administrator

$AgentName = "TaraAgent"
$BinName = "agent-windows-amd64.exe"
$InstallDir = "C:\Program Files\TaraAgent"
$ServerURL = "http://YOUR_SERVER_IP:8080" # CHANGE THIS

# 1. Check Admin
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Error "Please run this script as Administrator!"
    exit 1
}

# 2. Create Directory
Write-Host "Creating Install Directory: $InstallDir"
if (!(Test-Path -Path $InstallDir)) {
    New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
}

# 3. Copy Binary
Write-Host "Copying binary..."
Copy-Item -Path ".\$BinName" -Destination "$InstallDir\tara-agent.exe" -Force

# 4. Create Config
$ConfigContent = @"
server_url=$ServerURL
agent_id=$(New-Guid)
interval=5
"@
Set-Content -Path "$InstallDir\config.env" -Value $ConfigContent

# 5. Create Service
Write-Host "Creating Windows Service..."
sc.exe stop $AgentName 2>$null
sc.exe delete $AgentName 2>$null
Start-Sleep -Seconds 2

# Note: We use sc.exe because it is reliable. 
# Ensure spaces in path are quoted.
$BinPath = "`"$InstallDir\tara-agent.exe`" -config `"$InstallDir\config.env`""
sc.exe create $AgentName binPath= $BinPath start= auto DisplayName= "Tara Infrastructure Agent"

# 6. Set Recovery (Restart on failure)
sc.exe failure $AgentName reset= 86400 actions= restart/60000/restart/60000/restart/60000

# 7. Start
Write-Host "Starting Service..."
sc.exe start $AgentName

Write-Host "Installation Complete! Agent is running."
