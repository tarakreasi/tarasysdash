# Tara Server Installer for Windows
# Run as Administrator

$ServiceName = "TaraServer"
$BinName = "server-windows-amd64.exe"
$InstallDir = "C:\TaraServer"

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
Copy-Item -Path ".\$BinName" -Destination "$InstallDir\$BinName" -Force

# 4. Create Service
Write-Host "Creating Windows Service..."
sc.exe stop $ServiceName 2>$null
sc.exe delete $ServiceName 2>$null
Start-Sleep -Seconds 2

$BinPath = "$InstallDir\$BinName"
sc.exe create $ServiceName binPath= $BinPath start= auto DisplayName= "Tara System Dashboard Server"

# 5. Set Recovery
sc.exe failure $ServiceName reset= 86400 actions= restart/60000/restart/60000/restart/60000

# 6. Firewall
Write-Host "Opening Port 8080..."
New-NetFirewallRule -DisplayName "Tara Server Web" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow -ErrorAction SilentlyContinue

# 7. Start
Write-Host "Starting Service..."
sc.exe start $ServiceName

Write-Host "Server Installation Complete! Access at http://localhost:8080"
