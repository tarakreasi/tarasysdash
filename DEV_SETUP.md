# TaraSysDash - Development Setup Guide (Linux)

## Prerequisites Installation

### 1. Install Go (1.21+)
```bash
# Download Go 1.21
wget https://go.dev/dl/go1.21.5.linux-amd64.tar.gz

# Remove old installation (if any)
sudo rm -rf /usr/local/go

# Extract to /usr/local
sudo tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc

# Verify installation
go version
```

### 2. Install Node.js (20+) via NVM (Recommended)
```bash
# Install NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Reload shell
source ~/.bashrc

# Install Node.js 20
nvm install 20
nvm use 20

# Verify installation
node --version
npm --version
```

**Alternative: Install via apt (Ubuntu/Debian)**
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

---

## Running the Application

### Terminal 1: Backend Server

```bash
cd /home/twantoro/tarasysdash

# Optional: Set SMTP credentials for email alerts
export SMTP_USER="your-email@gmail.com"
export SMTP_PASS="your-app-password"
export ALERT_RECIPIENTS="admin@example.com"

# Run server
go run cmd/server/main.go
```

**Expected Output:**
```
{"time":"...","level":"INFO","msg":"Server executing on :8080"}
```

Backend will be available at: `http://localhost:8080`

---

### Terminal 2: Frontend Dashboard

```bash
cd /home/twantoro/tarasysdash/web

# Install dependencies (first time only)
npm install

# Start dev server
npm run dev
```

**Expected Output:**
```
  VITE v7.x.x  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

Dashboard will be available at: `http://localhost:5173`

---

### Terminal 3: Agent (Metrics Collector)

```bash
cd /home/twantoro/tarasysdash

# Run agent with rack location
go run cmd/agent/main.go --rack="Development Rack"
```

**Expected Output:**
```
{"level":"INFO","msg":"Starting tara-agent..."}
{"level":"INFO","msg":"Handshake successful! Token obtained."}
{"level":"INFO","msg":"Metrics sent successfully"}
```

---

## Quick Start Commands

**One-liner to start backend:**
```bash
cd /home/twantoro/tarasysdash && go run cmd/server/main.go
```

**One-liner to start frontend:**
```bash
cd /home/twantoro/tarasysdash/web && npm run dev
```

**One-liner to start agent:**
```bash
cd /home/twantoro/tarasysdash && go run cmd/agent/main.go --rack="Rack A"
```

---

## Verifying the Setup

1. **Check Backend Health:**
   ```bash
   curl http://localhost:8080/health
   # Expected: {"status":"ok"}
   ```

2. **Check Agents:**
   ```bash
   curl http://localhost:8080/api/v1/agents | jq
   ```

3. **Open Dashboard:**
   - Navigate to `http://localhost:5173`
   - You should see the TaraSysDash interface
   - Servers should appear in the right sidebar

---

## Troubleshooting

### "Command 'go' not found"
```bash
# Check if Go is in PATH
which go
# If not found, add to PATH
export PATH=$PATH:/usr/local/go/bin
```

### "vite: not found"
```bash
# Install Node.js dependencies
cd /home/twantoro/tarasysdash/web
npm install
```

### Port Already in Use
```bash
# Check what's using port 8080
sudo lsof -i :8080
# Kill the process if needed
sudo kill -9 <PID>
```

### SQLite Database Issues
```bash
# Remove old database
rm /home/twantoro/tarasysdash/tara.db*
# Restart server (it will recreate the DB)
```

---

## Optional: Using Makefile

The project includes a `Makefile` for common tasks:

```bash
# Build server
make build-server

# Build Linux agent
make build-agent-linux

# Build Windows agent (cross-compile)
make build-agent-windows

# Clean binaries
make clean

# Run full dev environment
make dev
```

---

## Production Build

### Backend
```bash
go build -o bin/server ./cmd/server
./bin/server
```

### Frontend
```bash
cd web
npm run build
# Output will be in web/dist/
```

### Agent (Windows)
```bash
GOOS=windows GOARCH=amd64 go build -o bin/agent.exe ./cmd/agent
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SMTP_HOST` | SMTP server hostname | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP server port | `587` |
| `SMTP_USER` | SMTP username/email | - |
| `SMTP_PASS` | SMTP password/app password | - |
| `ALERT_RECIPIENTS` | Email for alerts | - |

---

## Next Steps

1. ✅ Install Go and Node.js (see above)
2. ✅ Start backend server
3. ✅ Start frontend dashboard
4. ✅ Start an agent
5. ✅ Open `http://localhost:5173` in browser
6. ✅ Verify agent appears in sidebar

Happy monitoring! 🚀
