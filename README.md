# taraSysDash

> **Rack-aware infrastructure monitoring dashboard** — built for sysadmins who manage physical server rooms.

[![Go](https://img.shields.io/badge/Go-1.21+-00ADD8?style=flat&logo=go&logoColor=white)](https://golang.org)
[![Vue 3](https://img.shields.io/badge/Vue-3.x-4FC08D?style=flat&logo=vue.js&logoColor=white)](https://vuejs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/tarakreasi/taraysdash)](https://github.com/tarakreasi/taraysdash/releases)

Real-time infrastructure monitoring with production-grade Go backend, embedded Vue 3 frontend, and **rack location management** — all in a single binary.

```bash
# 1. Start server
./bin/server

# 2. Deploy agent to any Linux machine
AGENT_TOKEN=<your-token> ./bin/agent-cli --server=http://YOUR_SERVER:8080 --id=hostname
```

---

## 🎯 Who is this for?

- ✅ Sysadmins managing **5–50 servers** in a physical server room or data center
- ✅ Teams wanting rack-aware grouping **out of the box** — no plugins required
- ✅ Anyone who wants **single-binary deployment** without the Prometheus/Grafana stack
- ❌ Home users with 1–2 servers (use [Beszel](https://github.com/henrygd/beszel))
- ❌ Enterprises needing PromQL or complex custom dashboards (use Grafana)

---

## 🆚 Why taraSysDash?

| Feature | **taraSysDash** | Beszel | Netdata | Prometheus+Grafana |
|---|---|---|---|---|
| **Rack Location Management** | ✅ | ❌ | ❌ | ❌ (plugin) |
| **Single Binary** | ✅ | ✅ | ❌ | ❌ |
| **Agent RAM Usage** | ~15 MB | ~10 MB | ~300 MB | ~500 MB |
| **Setup Time** | ~5 min | ~5 min | ~1 min | Days |
| **Token-based Agent Auth** | ✅ | ❌ | ❌ | ✅ |
| **Visual ECharts Gauges** | ✅ | ❌ | ❌ | ❌ |
| **Embedded Vue 3 Frontend** | ✅ | ✅ | ❌ | ❌ |
| **Multi-disk Visualization** | ✅ | ✅ | ✅ | ✅ |
| **Cluster Global Overview** | ✅ | ❌ | ❌ | ✅ |

> **Key differentiator:** taraSysDash is the only open-source monitoring tool with built-in **Rack Location Management** — grouping and visualizing servers by their physical rack position.

---

## ✨ Features

### Dashboard
- **Real-Time Gauges** — CPU, Memory (GB), Temperature (°C), Network I/O, Disk Usage via ECharts
- **Multi-Disk Support** — Dynamic visualization for all partitions and mount points
- **Global Overview** — Cluster-wide CPU and Memory aggregation trends
- **Rack Management** — Group servers by physical rack location, filter by rack
- **Single Binary Deploy** — Embedded frontend assets in one Go executable for Linux/Windows
- **Service Monitoring** — Track status of critical system services
- **Log Retention** — Configurable per-agent log retention policy

### Backend APIs
- **Network Metrics** — BytesIn/Out (Mbps) from `/proc/net/dev`
- **Latency Stats** — P95/avg/min/max computation
- **Global Aggregation** — Cluster-wide network and CPU/memory averages
- **Rack Filtering** — Group and filter agents by rack location
- **SQLite Storage** — Zero-dependency embedded database

---

## 🚀 Quick Start

### Prerequisites
- Go 1.21 or higher
- Node.js 18+ and npm
- Linux or Windows

### Build from Source

```bash
git clone https://github.com/tarakreasi/taraysdash.git
cd taraysdash

# Build server + agent
make build

# Or manually:
go build -o bin/server cmd/server/main.go
go build -o bin/agent-cli cmd/agent-cli/main.go
```

### Running the System

```bash
# 1. Start server
./bin/server
# → Dashboard at http://localhost:8080

# 2. Deploy agent to each monitored machine
AGENT_TOKEN=<your-token> ./bin/agent-cli \
  --server=http://YOUR_SERVER:8080 \
  --id=web-server-01 \
  --name="Web Server 01" \
  --interval=5
```

### Local Development

```bash
# Runs server + agent + frontend dev server
./run_local.sh
```

### Cross-Platform Build

```bash
# Windows (cross-compile from Linux)
GOOS=windows GOARCH=amd64 go build -o bin/server.exe cmd/server/main.go
GOOS=windows GOARCH=amd64 go build -o bin/agent-cli.exe cmd/agent-cli/main.go
```

### Frontend Only

```bash
cd web
npm install
npm run dev      # Dev server at http://localhost:5173
npm run build    # Production build → web/dist/
```

---

## ⚙️ Configuration

### Environment Variables

```bash
# Server
PORT=8080                             # Server port (default: 8080)

# Agent
AGENT_TOKEN=<your-token>             # Required: Agent authentication token
SERVER_URL=http://localhost:8080     # Required: Backend server URL
POLL_INTERVAL=5                      # Optional: Metrics interval in seconds
```

### Setting Rack Location

```bash
curl -X PUT http://localhost:8080/api/v1/agents/my-server/metadata \
  -H "Content-Type: application/json" \
  -d '{"rack_location": "Rack-01", "hostname": "web-server-01"}'
```

---

## 🔌 API Endpoints

### Public Endpoints
```
GET  /api/v1/agents                      - List all agents
GET  /api/v1/agents/rack/:rack_id        - Filter agents by rack
GET  /api/v1/metrics/:agent_id           - Get metrics history
GET  /api/v1/metrics/:agent_id/network   - Network metrics (Mbps)
GET  /api/v1/metrics/global/history      - Cluster-wide aggregated metrics
GET  /api/v1/stats/:agent_id/network     - Network aggregation (avg/peak)
GET  /api/v1/stats/:agent_id/latency     - Latency stats (P95/avg/min/max)
GET  /health                             - Server health check
```

### Authenticated Endpoints
```
POST /api/v1/metrics                     - Submit metrics (requires AGENT_TOKEN)
PUT  /api/v1/agents/:id/metadata         - Update rack location & hostname
```

---

## 🗂️ Project Structure

```
taraSysDash/
├── cmd/
│   ├── server/         # Backend server entry point
│   └── agent-cli/      # Agent entry point
├── internal/
│   ├── collector/      # Metrics: CPU/Memory/Disk/Network/Latency
│   ├── config/         # Configuration management
│   ├── auth/           # Token generation & validation
│   ├── alert/          # Alert rules engine
│   ├── logger/         # Structured logging
│   └── storage/        # SQLite database layer
├── web/
│   ├── src/
│   │   ├── views/      # Dashboard, Infrastructure, Security views
│   │   ├── components/ # GlobalOverviewCharts, RackSidebar, ServerDetailPanel
│   │   ├── composables/# useDashboard.ts — Vue 3 state management
│   │   └── router/     # Vue Router config
│   └── tailwind.config.js
├── docs/
│   └── API.md          # Full API documentation
└── Makefile            # Build automation
```

---

## 🗄️ Database Schema

### agents
```sql
CREATE TABLE agents (
  id TEXT PRIMARY KEY,
  hostname TEXT NOT NULL,
  ip_address TEXT,
  os TEXT,
  rack_location TEXT DEFAULT '',
  temperature REAL DEFAULT 0.0,
  log_retention_days INTEGER DEFAULT 30,
  token_hash TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### system_metrics
```sql
CREATE TABLE system_metrics (
  time DATETIME NOT NULL,
  agent_id TEXT NOT NULL,
  cpu_usage REAL,
  memory_used INTEGER,
  memory_total INTEGER,
  disk_free_percent REAL,
  bytes_in INTEGER DEFAULT 0,
  bytes_out INTEGER DEFAULT 0,
  latency_ms REAL DEFAULT 0.0,
  disk_usage_json TEXT DEFAULT '[]',
  services_json TEXT DEFAULT '[]',
  uptime_seconds INTEGER DEFAULT 0,
  process_count INTEGER DEFAULT 0,
  temperature REAL DEFAULT 0.0,
  PRIMARY KEY (time, agent_id),
  FOREIGN KEY(agent_id) REFERENCES agents(id)
);
```

---

## ⚡ Performance

| Metric | Value |
|---|---|
| Agent RAM usage | ~15 MB |
| Frontend bundle (gzipped) | 217 KB |
| Metrics update interval | 5 seconds |
| Tested concurrent agents | 41+ |
| Database growth | ~1 MB / agent / day |

---

## 🛠️ Development

```bash
make build          # Build server and agent
make run-server     # Run server
make run-agent      # Run agent
make clean          # Clean build artifacts
```

---

## 📦 Production Deployment

```bash
# 1. Build for target platform
make build

# 2. Copy binaries to servers
scp bin/server user@monitor-server:/opt/tarasysdash/
scp bin/agent-cli user@target-machine:/usr/local/bin/

# 3. Run with systemd (see docs/field/install.sh)
```

---

## 📄 License

MIT — see [LICENSE](LICENSE)

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md)

## Features

### Dashboard
- **Real-Time Gauges** - CPU, Memory (GB), Temperature (°C), Network I/O, and Disk Usage.
- **Multi-Disk Support** - Dynamic visualization for all system partitions and mount points.
- **Global Overview** - Cluster-wide CPU and Memory aggregation trends.
- **Single Binary Deploy** - Embedded frontend assets inside a single Go executable for Linux/Windows.
- **Service Monitoring** - Track status of critical system services.
- **Rack Management** - Automatic server grouping by physical location.
- **Dynamic Stats** - Live agent count and uptime tracking.

### Backend APIs
- **Network Metrics** - BytesIn/Out collection from `/proc/net/dev`
- **Latency Stats** - P95/avg/min/max computation
- **Aggregation** - Network and latency statistics endpoints
- **Rack Filtering** - Group and filter servers by rack location
- **SQLite Storage** - Lightweight database with extended schema

## Tech Stack

### Backend
- **Go 1.21+** - High-performance backend
- **Gin** - HTTP web framework
- **SQLite** - Embedded database
- **gopsutil** - System metrics collection

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **TypeScript** - Type-safe development
- **TailwindCSS** - Utility-first CSS
- **ECharts** - Interactive charts
- **Vue Router** - Multi-page navigation
- **Axios** - HTTP client

## Quick Start

### Prerequisites
- Go 1.21 or higher
- Node.js 18+ and npm
- Linux or Windows (for server and agent)

### Multi-Platform Build
```bash
# Build for Linux
go build -o bin/server cmd/server/main.go
go build -o bin/agent-cli cmd/agent-cli/main.go

# Build for Windows (Cross-compile from Linux)
GOOS=windows GOARCH=amd64 go build -o bin/server.exe cmd/server/main.go
GOOS=windows GOARCH=amd64 go build -o bin/agent-cli.exe cmd/agent-cli/main.go
```

### Running the System
1. **Start Server**: `./bin/server` (Linux) or `.\bin\server.exe` (Windows)
2. **Setup Agent**: `./bin/agent-cli --server=http://localhost:8080 --id=my-server --interval=1`
3. **Dashboard**: Open `http://localhost:8080` in your browser.

### Local Development (Recommended)
Use the helper script to run everything (Server, Agent, Frontend):
```bash
./run_local.sh
```

### Manual Run

#### Backend Server
```bash
go build -o bin/server ./cmd/server
./bin/server
# Server starts on :8080
```

#### Agent (CLI Mode)
Note: Use CLI mode to avoid heavy GUI dependencies during dev.
```bash
go build -o bin/agent-cli ./cmd/agent-cli
./bin/agent-cli -server http://localhost:8080 -name "local-dev"
```

### Frontend
```bash
cd web
npm install
npm run dev
# Dashboard at http://localhost:5173
```

### Production Build
```bash
cd web
npm run build
# Static files in web/dist/
```

## API Endpoints

### Public Endpoints
```
GET  /api/v1/agents                    - List all agents
GET  /api/v1/agents/rack/:rack_id      - Filter agents by rack
GET  /api/v1/metrics/:agent_id         - Get metrics history
GET  /api/v1/metrics/:agent_id/network - Network metrics with Mbps
GET  /api/v1/stats/:agent_id/network   - Network aggregation (avg/peak)
GET  /api/v1/stats/:agent_id/latency   - Latency stats (P95/avg/min/max)
```

### Authenticated Endpoints
```
POST /api/v1/metrics                   - Submit metrics (requires token)
PUT  /api/v1/agents/:id/metadata       - Update rack location & temperature
```

## Configuration

### Environment Variables
```bash
# Server
PORT=8080                              # Server port (default: 8080)

# Agent
AGENT_TOKEN=<your-token>               # Required: Agent authentication token
SERVER_URL=http://localhost:8080       # Required: Backend server URL
POLL_INTERVAL=5                        # Optional: Metrics collection interval (seconds)
```

## Project Structure

```
taraSysDash/
├── cmd/
│   ├── server/         # Backend server entry point
│   └── agent/          # Agent entry point
├── internal/
│   ├── collector/      # Metrics collection (CPU/Memory/Disk/Network/Latency)
│   ├── config/         # Configuration management
│   ├── logger/         # Structured logging
│   └── storage/        # SQLite database layer
├── web/
│   ├── src/
│   │   ├── views/      # Dashboard, Deployments, Infrastructure, Security
│   │   ├── router/     # Vue Router configuration
│   │   └── App.vue     # Main app with navigation
│   └── tailwind.config.js
├── docs/
│   ├── API.md          # API documentation
│   └── sprint/         # Sprint planning documents
└── Makefile            # Build automation
```

## Database Schema

### agents
```sql
CREATE TABLE agents (
  id TEXT PRIMARY KEY,
  hostname TEXT NOT NULL,
  ip_address TEXT,
  os TEXT,
  rack_location TEXT DEFAULT '',
  temperature REAL DEFAULT 0.0,
  log_retention_days INTEGER DEFAULT 30,
  token_hash TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```


### system_metrics
```sql
CREATE TABLE system_metrics (
  time DATETIME NOT NULL,
  agent_id TEXT NOT NULL,
  cpu_usage REAL,
  memory_used INTEGER,
  memory_total INTEGER,
  disk_free_percent REAL,
  bytes_in INTEGER DEFAULT 0,
  bytes_out INTEGER DEFAULT 0,
  latency_ms REAL DEFAULT 0.0,
  disk_usage_json TEXT DEFAULT '[]',
  services_json TEXT DEFAULT '[]',
  uptime_seconds INTEGER DEFAULT 0,
  process_count INTEGER DEFAULT 0,
  temperature REAL DEFAULT 0.0,
  PRIMARY KEY (time, agent_id),
  FOREIGN KEY(agent_id) REFERENCES agents(id)
);
```

## Development

### Build Commands
```bash
make build          # Build both server and agent
make run-server     # Run server
make run-agent      # Run agent
make clean          # Clean build artifacts
```

### Frontend Development
```bash
cd web
npm run dev         # Development server with HMR
npm run build       # Production build
npm run preview     # Preview production build
```

## Production Deployment

See [Deployment Guide](/.gemini/antigravity/brain/795691a1-f569-44bc-bdbc-2beb68f9aa95/deployment_guide.md) for detailed instructions.

### Quick Deploy
1. Build binaries for target OS
2. Deploy server with database
3. Deploy agents to all servers (41+)
4. Configure rack metadata
5. Serve frontend from `web/dist/`

## Performance

- **Build Time** - Frontend: ~5.8s
- **Bundle Size** - Gzipped: 217KB (total)
- **Update Interval** - 5 seconds
- **Supported Scale** - 41+ concurrent agents
- **Database Growth** - ~1MB per agent per day

## License

MIT

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## Changelog

See [CHANGELOG.md](CHANGELOG.md)