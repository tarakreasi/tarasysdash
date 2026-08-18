#!/usr/bin/env bash
# ==============================================================================
# taraSysDash Agent - Automated One-Line Installer for Linux
# https://github.com/tarakreasi/tarasysdash
# ==============================================================================
set -e

GITHUB_REPO="tarakreasi/tarasysdash"
BIN_NAME="tara-agent"
INSTALL_DIR="/usr/local/bin"
SERVICE_FILE="/etc/systemd/system/tara-agent.service"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================================${NC}"
echo -e "${BLUE}        🚀 taraSysDash Agent One-Line Installer       ${NC}"
echo -e "${BLUE}======================================================${NC}"

# 1. Require Root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}❌ Please run as root (use sudo).${NC}"
  exit 1
fi

# 2. Parse Arguments
SERVER_URL=""
AGENT_TOKEN=""
AGENT_ID=""
VERSION="latest"

while [[ $# -gt 0 ]]; do
  case $1 in
    -s|--server)
      SERVER_URL="$2"
      shift 2
      ;;
    -t|--token)
      AGENT_TOKEN="$2"
      shift 2
      ;;
    --id)
      AGENT_ID="$2"
      shift 2
      ;;
    -v|--version)
      VERSION="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: curl -sSL https://raw.githubusercontent.com/$GITHUB_REPO/main/scripts/install-agent.sh | sudo bash -s -- [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  -s, --server  <URL>      Backend Server URL (e.g. http://192.168.1.100:8080)"
      echo "  -t, --token   <TOKEN>    Agent Authentication Token"
      echo "      --id      <AGENT_ID> Unique Agent ID (default: system hostname)"
      echo "  -v, --version <VERSION>  Version tag to install (default: latest)"
      echo "  -h, --help               Show this help message"
      exit 0
      ;;
    *)
      echo -e "${YELLOW}Unknown option: $1${NC}"
      shift
      ;;
  esac
done

# 3. Interactive Prompts if parameters are missing
if [ -z "$SERVER_URL" ]; then
  read -rp "Enter Backend Server URL (e.g. http://192.168.1.100:8080): " SERVER_URL
fi

if [ -z "$AGENT_TOKEN" ]; then
  read -rp "Enter AGENT_TOKEN: " AGENT_TOKEN
fi

if [ -z "$SERVER_URL" ] || [ -z "$AGENT_TOKEN" ]; then
  echo -e "${RED}❌ SERVER_URL and AGENT_TOKEN are required to proceed.${NC}"
  exit 1
fi

# 4. Detect Architecture
ARCH_RAW=$(uname -m)
case "$ARCH_RAW" in
  x86_64|amd64)
    ARCH="amd64"
    ;;
  aarch64|arm64)
    ARCH="arm64"
    ;;
  *)
    echo -e "${RED}❌ Unsupported architecture: $ARCH_RAW. Supported: amd64, arm64${NC}"
    exit 1
    ;;
esac

echo -e "📦 Detected System Architecture: ${GREEN}linux_${ARCH}${NC}"

# 5. Resolve Download URL
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

if [ "$VERSION" = "latest" ]; then
  DOWNLOAD_URL="https://github.com/$GITHUB_REPO/releases/latest/download/tara-agent_linux_${ARCH}.tar.gz"
else
  DOWNLOAD_URL="https://github.com/$GITHUB_REPO/releases/download/$VERSION/tara-agent_linux_${ARCH}.tar.gz"
fi

echo -e "⬇️  Downloading tara-agent from: ${BLUE}$DOWNLOAD_URL${NC}"

if command -v curl >/dev/null 2>&1; then
  curl -sSL -f "$DOWNLOAD_URL" -o "$TMP_DIR/tara-agent.tar.gz" || {
    echo -e "${RED}❌ Download failed. Check your network or if version '$VERSION' exists on GitHub Releases.${NC}"
    exit 1
  }
elif command -v wget >/dev/null 2>&1; then
  wget -q "$DOWNLOAD_URL" -O "$TMP_DIR/tara-agent.tar.gz" || {
    echo -e "${RED}❌ Download failed. Check your network or if version '$VERSION' exists on GitHub Releases.${NC}"
    exit 1
  }
else
  echo -e "${RED}❌ Neither curl nor wget is installed.${NC}"
  exit 1
fi

# 6. Extract and Install Binary
tar -xzf "$TMP_DIR/tara-agent.tar.gz" -C "$TMP_DIR"
if [ ! -f "$TMP_DIR/tara-agent" ]; then
  echo -e "${RED}❌ Binary tara-agent not found in archive.${NC}"
  exit 1
fi

install -m 755 "$TMP_DIR/tara-agent" "$INSTALL_DIR/$BIN_NAME"
echo -e "✅ Installed binary to: ${GREEN}$INSTALL_DIR/$BIN_NAME${NC}"

# 7. Create systemd Service
AGENT_ARGS=""
if [ -n "$AGENT_ID" ]; then
  AGENT_ARGS="--id=$AGENT_ID"
fi

cat <<EOF > "$SERVICE_FILE"
[Unit]
Description=taraSysDash Monitoring Agent
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
User=root
Environment=SERVER_URL=$SERVER_URL
Environment=AGENT_TOKEN=$AGENT_TOKEN
ExecStart=$INSTALL_DIR/$BIN_NAME $AGENT_ARGS
Restart=always
RestartSec=5s
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF

echo -e "⚙️  Created systemd service: ${GREEN}$SERVICE_FILE${NC}"

# 8. Reload & Start Service
systemctl daemon-reload
systemctl enable tara-agent.service
systemctl restart tara-agent.service

echo -e ""
echo -e "${GREEN}======================================================${NC}"
echo -e "${GREEN}  🎉 tara-agent successfully installed & started!     ${NC}"
echo -e "${GREEN}======================================================${NC}"
echo -e "Check service status:  ${YELLOW}systemctl status tara-agent${NC}"
echo -e "View live agent logs:  ${YELLOW}journalctl -u tara-agent -f${NC}"
echo -e ""
