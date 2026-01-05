# 🚀 Sprint 1: Foundation & Core Agent

**Goal:** Establish the Go project structure and implement the `tara-agent` capable of collecting system metrics (CPU, Memory, Disk, Net) and handling graceful shutdowns.

## 📅 Timeline & Scope
- **Focus:** Backend (Go)
- **Deliverable:** A compiled binary `tara-agent` that logs system stats to stdout (JSON format).
- **Anti-goals:** No HTTP ingestion (Sprint 2), no persistent storage, no dashboard.

## 🛠 Technical Specification

### 1. Project Structure (Standard Go Layout)
We will adopt the `cmd/` and `internal/` pattern to enforce separation of concerns.
```
taraSysDash/
├── cmd/
│   └── agent/
│       └── main.go       # Entry point
├── internal/
│   ├── collector/        # Stats gathering logic
│   ├── config/           # Configuration management
│   └── logger/           # Structured logging wrapper
├── go.mod
├── Makefile              # Build automation
└── README.md
```

### 2. Core Components

#### A. Configuration Manager (`internal/config`)
- **Library:** `github.com/spf13/viper` or stdlib `os.Getenv` (Keep it simple for now).
- **Requirements:**
    - `AGENT_INTERVAL`: Poll duration (default: 1s).
    - `LOG_LEVEL`: debug/info/warn.

#### B. Metrics Collector (`internal/collector`)
- **Library:** `github.com/shirou/gopsutil/v3`
- **Interfaces:**
    ```go
    type MetricProvider interface {
        GetCPU() (float64, error)
        GetMemory() (*MemoryStats, error)
        GetDisk() (*DiskStats, error)
    }
    ```
- **Data Point Schema (JSON):**
    ```json
    {
      "agent_id": "uuid-v4",
      "timestamp": 1704067200,
      "metrics": {
        "cpu_usage_percent": 12.5,
        "memory_used_bytes": 102400,
        "memory_total_bytes": 8192000,
        "disk_free_percent": 45.2
      }
    }
    ```

#### C. Main Loop & Concurrency
- Use `time.Ticker` for periodic collection.
- Implement `os.Signal` handling (SIGINT, SIGTERM) for graceful shutdown.
- Use Go Context to propagate cancellation.

### 3. Development Workflow

#### Dependencies
```bash
go mod init github.com/tarakreasi/taraSysDash
go get github.com/shirou/gopsutil/v3
```

#### Quality Assurance
- **Linting:** `golangci-lint` must pass.
- **Testing:** Unit tests for `collector` using interfaces to mock system calls.

## ✅ Definition of Done (DoD)
1.  [ ] `go mod init` created.
2.  [ ] Project structure set up.
3.  [ ] `collector` package implements CPU/Mem/Disk fetching.
4.  [ ] `main.go` runs a loop, collects stats, logs JSON to console.
5.  [ ] `Ctrl+C` stops the agent gracefully (no abrupt exit).
6.  [ ] `Makefile` has `build` and `run` targets.
