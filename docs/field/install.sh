#!/bin/bash
set -e

# Configuration
INSTALL_DIR="/opt/taraSysDash"
DATA_DIR="/var/lib/taraSysDash"
BIN_DIR="$INSTALL_DIR/bin"
SERVER_BIN="server"
AGENT_BIN="agent-cli"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== TaraSysDash Linux Installer ===${NC}"

# 1. Check Root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}Error: This script must be run as root${NC}" 
   exit 1
fi

# 2. Check Source Binaries
if [[ ! -f "bin/$SERVER_BIN" || ! -f "bin/$AGENT_BIN" ]]; then
    echo -e "${RED}Error: Binaries not found in ./bin/${NC}"
    echo "Please run 'go build' first or ensure you are in the project root."
    exit 1
fi

# 3. Stop Existing Services
echo "Stopping existing services..."
systemctl stop tara-server || true
systemctl stop tara-agent || true

# 4. Create Directories
echo "Creating directories..."
mkdir -p "$BIN_DIR"
mkdir -p "$DATA_DIR"

# 5. Copy Binaries
echo "Copying binaries..."
cp "bin/$SERVER_BIN" "$BIN_DIR/"
cp "bin/$AGENT_BIN" "$BIN_DIR/"
chmod +x "$BIN_DIR/$SERVER_BIN"
chmod +x "$BIN_DIR/$AGENT_BIN"

# 6. Create Systemd Service: SERVER
echo "Creating tara-server.service..."
cat <<EOF > /etc/systemd/system/tara-server.service
[Unit]
Description=TaraSysDash Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$DATA_DIR
ExecStart=$BIN_DIR/$SERVER_BIN
Restart=always
RestartSec=5
Environment=PORT=8080
# Environment=gin_mode=release

[Install]
WantedBy=multi-user.target
EOF

# 7. Create Systemd Service: AGENT
echo "Creating tara-agent.service..."
cat <<EOF > /etc/systemd/system/tara-agent.service
[Unit]
Description=TaraSysDash Agent
After=network.target

[Service]
Type=simple
User=root
# Adjust arguments as needed needed. Using defaults for local loopback.
# In production, change -server to your actual server IP.
ExecStart=$BIN_DIR/$AGENT_BIN -server http://localhost:8080
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 8. Reload and Enable
echo "Reloading systemd..."
systemctl daemon-reload
systemctl enable tara-server
systemctl enable tara-agent

# 9. Start Services
echo "Starting services..."
systemctl start tara-server
systemctl start tara-agent

echo -e "${GREEN}=== Installation Complete! ===${NC}"
echo "Server Status: systemctl status tara-server"
echo "Agent Status:  systemctl status tara-agent"
echo "Dashboard:     http://localhost:8080"
