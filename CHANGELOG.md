# Changelog

All notable changes to taraSysDash will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2026-01-01

### Added - Sprint 8: Backend Network Metrics
- Network metrics collection from `/proc/net/dev`
- Latency measurement via system call timing
- Database schema extensions: `bytes_in`, `bytes_out`, `latency_ms` columns
- GET `/api/v1/metrics/:agent_id/network` endpoint with Mbps calculation

### Added - Sprint 9: Backend Extended APIs
- GET `/api/v1/stats/:agent_id/network` - Network aggregation (avg/peak Mbps)
- GET `/api/v1/stats/:agent_id/latency` - Latency statistics (P95/avg/min/max)
- GET `/api/v1/agents/rack/:rack_id` - Rack-based filtering
- Query optimization for 41-agent scale
- Pagination support via limit parameter

### Added - Sprint 10: Frontend Foundation
- TailwindCSS 3.x integration
- Vue Router 4 with multi-page navigation
- Space Grotesk font from Google Fonts
- Custom dark theme with mockup colors
- Top navigation bar with 4 routes
- Custom scrollbar styling

### Added - Sprint 11: Metric Cards & Charts
- 6 metric cards: CPU Load, Memory, Net In/Out, Latency, Throughput
- Latency multi-line chart with ECharts
- Throughput dual-line chart (HTTP/gRPC)
- Live system logs with terminal styling
- Color-coded log levels (INFO/WARN/ERROR)
- Real-time data integration from backend APIs

### Added - Sprint 12: Server List & Rack Grouping
- Dynamic server loading from `/api/v1/agents`
- Automatic rack grouping by `rack_location`
- Color-coded status badges (green/yellow/red)
- Server metadata display (hostname, rack, temperature)
- Scrollable server sidebar for 41+ servers
- 5-second auto-refresh for server list

### Added - Sprint 13: Production Polish
- Production deployment guide
- Build optimization
- Performance documentation
- Architecture diagrams
- Troubleshooting guide
- Maintenance procedures

### Changed
- Collector refactored with modular helper functions
- Storage layer extended with aggregation methods
- Dashboard layout matching production mockup
- Agent struct updated with network and latency fields

### Fixed
- TypeScript import errors in collector
- Missing sort import for P95 calculation
- Unused parameter warnings
- Build warnings for large chunks

## [0.4.0] - 2025-12-31

### Added - Sprint 6: Production Dashboard UI
- Extended Agent interface with `rack_location`, `temperature`, `status`
- Color-coded status badges (green/red) with smooth transitions
- Metadata display for rack location and temperature
- Real-time updates: agents every 5s, metrics every 3s
- TypeScript lint error fixes

## [0.3.0] - 2025-12-30

### Added - Sprint 5: Backend Extended Metadata
- Database columns: `rack_location` (TEXT), `temperature` (REAL)
- Agent struct fields: `RackLocation`, `Temperature`, `Status`
- Status computation: "offline" if >30s since last update
- PUT `/api/v1/agents/:id/metadata` endpoint
- Enhanced GET `/api/v1/agents` with extended data

## [0.2.0] - 2025-12-29

### Added - Sprint 3: Authentication & Security
- Token-based authentication for agents
- SHA-256 token hashing
- Database column: `token_hash`
- Middleware for protected endpoints
- UpdateAgentToken and GetAgentIDByTokenHash methods

### Added - Sprint 4: Frontend Dashboard & Visualization
- Vue 3 + TypeScript frontend with Vite
- ECharts integration for metrics visualization
- HTTP client with Axios
- Real-time data polling
- Responsive dashboard UI

## [0.1.0] - 2025-12-28

### Added - Sprint 1: Agent Foundation
- Go agent with metrics collection
- CPU, Memory, Disk usage tracking
- gopsutil integration
- Graceful shutdown handling
- Structured logging with slog
- Configuration manager
- Makefile for build automation

### Added - Sprint 2: Backend Server & Storage
- Gin HTTP server
- SQLite storage layer
- RESTful API endpoints
- Database migrations
- Agent registration
- Metrics storage and retrieval

[1.0.0]: https://github.com/tarakreasi/taraSysDash/releases/tag/v1.0.0
[0.4.0]: https://github.com/tarakreasi/taraSysDash/releases/tag/v0.4.0
[0.3.0]: https://github.com/tarakreasi/taraSysDash/releases/tag/v0.3.0
[0.2.0]: https://github.com/tarakreasi/taraSysDash/releases/tag/v0.2.0
[0.1.0]: https://github.com/tarakreasi/taraSysDash/releases/tag/v0.1.0
