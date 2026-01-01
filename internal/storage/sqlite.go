package storage

import (
	"context"
	"database/sql"
	"log/slog"
	"time"

	_ "modernc.org/sqlite"
)

type Agent struct {
	ID           string    `json:"id"`
	Hostname     string    `json:"hostname"`
	IPAddress    string    `json:"ip_address"`
	OS           string    `json:"os"`
	RackLocation string    `json:"rack_location"`
	Temperature  float64   `json:"temperature"`
	Status       string    `json:"status,omitempty"`
	CreatedAt    time.Time `json:"created_at"`
	UpdatedAt    time.Time `json:"updated_at"`
}

type Metric struct {
	Timestamp        int64   `json:"timestamp"`
	CPUUsagePercent  float64 `json:"cpu_usage_percent"`
	MemoryUsedBytes  uint64  `json:"memory_used_bytes"`
	MemoryTotalBytes uint64  `json:"memory_total_bytes"`
	DiskFreePercent  float64 `json:"disk_free_percent"`
	BytesIn          uint64  `json:"bytes_in"`
	BytesOut         uint64  `json:"bytes_out"`
	LatencyMs        float64 `json:"latency_ms"`
}

type SQLiteStore struct {
	db *sql.DB
}

func NewSQLiteStore(dbPath string) (*SQLiteStore, error) {
	db, err := sql.Open("sqlite", dbPath)
	if err != nil {
		return nil, err
	}

	if err := db.Ping(); err != nil {
		return nil, err
	}

	if err := runMigrations(db); err != nil {
		return nil, err
	}

	return &SQLiteStore{db: db}, nil
}

func runMigrations(db *sql.DB) error {
	queries := []string{
		`CREATE TABLE IF NOT EXISTS agents (
			id TEXT PRIMARY KEY,
			hostname TEXT NOT NULL,
			ip_address TEXT,
			os TEXT,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
		);`,
		`CREATE TABLE IF NOT EXISTS system_metrics (
			time DATETIME NOT NULL,
			agent_id TEXT NOT NULL,
			cpu_usage REAL,
			memory_used INTEGER,
			memory_total INTEGER,
			disk_free_percent REAL,
			PRIMARY KEY (time, agent_id),
			FOREIGN KEY(agent_id) REFERENCES agents(id)
		);`,
		// Sprint 3: Add token_hash
		`ALTER TABLE agents ADD COLUMN token_hash TEXT;`,
		// Sprint 5: Add rack_location
		`ALTER TABLE agents ADD COLUMN rack_location TEXT DEFAULT '';`,
		// Sprint 5: Add temperature
		`ALTER TABLE agents ADD COLUMN temperature REAL DEFAULT 0.0;`,
	}

	for _, query := range queries {
		_, err := db.Exec(query)
		// Ignore errors for ALTER TABLE (column might already exist)
		if err != nil && (query == queries[2] || query == queries[3] || query == queries[4]) {
			slog.Info("Migration step executed (ignoring potential duplicate column error)", "query", query, "error", err)
		} else if err != nil {
			return err
		}
	}
	return nil
}

func (s *SQLiteStore) RegisterAgent(ctx context.Context, agent *Agent) error {
	query := `
	INSERT INTO agents (id, hostname, ip_address, os, updated_at)
	VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
	ON CONFLICT(id) DO UPDATE SET
		hostname=excluded.hostname,
		ip_address=excluded.ip_address,
		os=excluded.os,
		updated_at=CURRENT_TIMESTAMP;
	`
	_, err := s.db.ExecContext(ctx, query, agent.ID, agent.Hostname, agent.IPAddress, agent.OS)
	if err != nil {
		slog.Error("Failed to register agent", "error", err)
	}
	return err
}

func (s *SQLiteStore) SaveMetric(ctx context.Context, agentID string, m *Metric) error {
	query := `
	INSERT INTO system_metrics (time, agent_id, cpu_usage, memory_used, memory_total, disk_free_percent)
	VALUES (?, ?, ?, ?, ?, ?);
	`
	t := time.Unix(m.Timestamp, 0)
	_, err := s.db.ExecContext(ctx, query, t, agentID, m.CPUUsagePercent, m.MemoryUsedBytes, m.MemoryTotalBytes, m.DiskFreePercent)
	if err != nil {
		slog.Error("Failed to save metric", "error", err)
	}
	return err
}

func (s *SQLiteStore) GetAgentIDByTokenHash(ctx context.Context, hash string) (string, error) {
	var id string
	query := `SELECT id FROM agents WHERE token_hash = ?`
	err := s.db.QueryRowContext(ctx, query, hash).Scan(&id)
	if err != nil {
		return "", err
	}
	return id, nil
}

func (s *SQLiteStore) UpdateAgentToken(ctx context.Context, agentID, hash string) error {
	query := `UPDATE agents SET token_hash = ? WHERE id = ?`
	_, err := s.db.ExecContext(ctx, query, hash, agentID)
	return err
}

func (s *SQLiteStore) ListAgents(ctx context.Context) ([]Agent, error) {
	query := `SELECT id, hostname, ip_address, os, rack_location, temperature, created_at, updated_at FROM agents ORDER BY updated_at DESC`
	rows, err := s.db.QueryContext(ctx, query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var agents []Agent
	for rows.Next() {
		var a Agent
		if err := rows.Scan(&a.ID, &a.Hostname, &a.IPAddress, &a.OS, &a.RackLocation, &a.Temperature, &a.CreatedAt, &a.UpdatedAt); err != nil {
			return nil, err
		}
		// Compute status: offline if not updated in last 30 seconds
		if time.Since(a.UpdatedAt) > 30*time.Second {
			a.Status = "offline"
		} else {
			a.Status = "online"
		}
		agents = append(agents, a)
	}
	return agents, rows.Err()
}

func (s *SQLiteStore) UpdateAgentMetadata(ctx context.Context, agentID, rackLocation string, temperature float64) error {
	query := `UPDATE agents SET rack_location = ?, temperature = ? WHERE id = ?`
	_, err := s.db.ExecContext(ctx, query, rackLocation, temperature, agentID)
	return err
}

func (s *SQLiteStore) GetRecentMetrics(ctx context.Context, agentID string, limit int) ([]Metric, error) {
	query := `
		SELECT cpu_usage, memory_used, memory_total, disk_free_percent, time
		FROM system_metrics
		WHERE agent_id = ?
		ORDER BY time DESC
		LIMIT ?
	`
	rows, err := s.db.QueryContext(ctx, query, agentID, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var metrics []Metric
	for rows.Next() {
		var m Metric
		var t time.Time
		if err := rows.Scan(&m.CPUUsagePercent, &m.MemoryUsedBytes, &m.MemoryTotalBytes, &m.DiskFreePercent, &t); err != nil {
			return nil, err
		}
		m.Timestamp = t.Unix()
		metrics = append(metrics, m)
	}
	return metrics, rows.Err()
}
