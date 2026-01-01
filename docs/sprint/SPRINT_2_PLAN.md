# 🚀 Sprint 2: Ingestion Engine & Storage (SQLite Edition)

**Goal:** Implement the "Tara Core" ingestion service to receive JSON streams from agents and persist them into a local SQLite database.

## 📅 Timeline & Scope
- **Focus:** Backend (Go) & Database (SQLite)
- **Deliverable:**
    - A running `tara-server` HTTP service.
    - SQLite database file `tara.db` with `agents` and `system_metrics` tables.
    - `tara-agent` updated to send data to `tara-server`.
- **Anti-goals:** No Authentication (Sprint 3), No Dashboard (Sprint 4), No Postgres (Moved to later sprint/prod).

## 🛠 Technical Specification

### 1. Database Schema (SQLite)
We will use a local file `tara.db`.

#### Table: `agents`
Stores metadata about registered agents.
```sql
CREATE TABLE IF NOT EXISTS agents (
    id TEXT PRIMARY KEY, -- SQLite uses TEXT for UUIDs usually
    hostname TEXT NOT NULL,
    ip_address TEXT,
    os TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### Table: `system_metrics`
Stores time-series data.
```sql
CREATE TABLE IF NOT EXISTS system_metrics (
    time DATETIME NOT NULL,
    agent_id TEXT NOT NULL,
    cpu_usage REAL,
    memory_used INTEGER,
    memory_total INTEGER,
    disk_free_percent REAL,
    PRIMARY KEY (time, agent_id),
    FOREIGN KEY(agent_id) REFERENCES agents(id)
);
```

### 2. Backend Service (`cmd/server`)

#### A. HTTP Server
- **Framework:** `github.com/gin-gonic/gin`
- **Endpoints:**
    - `POST /api/v1/metrics`: Accepts JSON payload from agent.
    - `GET /health`: Health check.

#### B. Storage Layer (`internal/storage`)
- **Driver:** `github.com/mattn/go-sqlite3` (Standard, robust) OR `modernc.org/sqlite` (CGO-free).
- **Decision:** Let's use `modernc.org/sqlite` to keep the server easy to compile and run anywhere without CGO.
- **Interface:**
    ```go
    type MetricStore interface {
        SaveMetric(ctx context.Context, agentID string, m *Metric) error
        RegisterAgent(ctx context.Context, agent *Agent) error
    }
    ```

### 3. Agent Update (`cmd/agent`)
- Update `agent` to make HTTP POST requests.

### 4. Development Workflow
- **No Docker needed for DB!** Just run the binary.
- **Dependencies:**
    ```bash
    go get github.com/gin-gonic/gin
    go get modernc.org/sqlite
    ```

## ✅ Definition of Done (DoD)
1.  [ ] `tara-server` creates `tara.db` on startup if missing.
2.  [ ] Schema migrations run automatically.
3.  [ ] `tara-server` accepts POST requests.
4.  [ ] `tara-agent` successfully sends metrics.
5.  [ ] Data verified in `tara.db` using `sqlite3` CLI or viewer.
