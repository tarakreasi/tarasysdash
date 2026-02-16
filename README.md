# taraSysDash

Real-time infrastructure monitoring dashboard for data centers with production-grade backend APIs and modern Vue 3 frontend.

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