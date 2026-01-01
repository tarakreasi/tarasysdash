# Deployment: Linux

This guide details how to install the `tara-agent` on Linux (Ubuntu/Debian/RHEL) using Systemd.

## Prerequisites
- Root or Sudo privileges.
- The `agent-linux-amd64` binary.

## Installation Script (`install.sh`)

```bash
#!/bin/bash
set -e

APP_NAME="tara-agent"
INSTALL_DIR="/opt/tara-agent"
BIN_NAME="agent-linux-amd64"
SERVER_URL="http://YOUR_SERVER_IP:8080" # CHANGE THIS

# 1. Prepare Directory
echo "Installing to $INSTALL_DIR..."
sudo mkdir -p $INSTALL_DIR
sudo cp ./$BIN_NAME $INSTALL_DIR/$APP_NAME
sudo chmod +x $INSTALL_DIR/$APP_NAME

# 2. Create Config
echo "Creating config..."
cat <<EOF | sudo tee $INSTALL_DIR/config.env
SERVER_URL=$SERVER_URL
AGENT_ID=$(cat /proc/sys/kernel/random/uuid)
INTERVAL=5
EOF

# 3. Create Systemd Service
echo "Creating systemd service..."
cat <<EOF | sudo tee /etc/systemd/system/$APP_NAME.service
[Unit]
Description=Tara Infrastructure Agent
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/$APP_NAME -config $INSTALL_DIR/config.env
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 4. Enable and Start
echo "Starting service..."
sudo systemctl daemon-reload
sudo systemctl enable $APP_NAME
sudo systemctl restart $APP_NAME

echo "Installation Complete. Status:"
systemctl status $APP_NAME --no-pager
```
