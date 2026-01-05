# taraSysDash

Real-time infrastructure monitoring dashboard for data centers with production-grade backend APIs and modern Vue 3 frontend.

## Features

### Dashboard
- **6 Metric Cards** - CPU (with Temp), Memory, Disk, Network I/O (Rate), Uptime, Processes
- **Service Monitoring** - Track status of critical services
- **Performance Charts** - Latency multi-line chart, HTTP/gRPC throughput visualization
- **Live System Logs** - Terminal-style log display with color-coded levels
- **Server Management** - 41+ server support with automatic rack grouping
- **Auto-Refresh** - 5-second update interval for real-time monitoring

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
- Linux system (for agent)

### Backend Server
```bash
# Build server
go build -o bin/tara-server cmd/server/main.go

# Run server
./bin/tara-server
# Server starts on :8080
```

### Agent
```bash
# Build agent
go build -o bin/tara-agent cmd/agent/main.go

# Run agent
export AGENT_TOKEN=your-secure-token
export SERVER_URL=http://localhost:8080
./bin/tara-agent
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