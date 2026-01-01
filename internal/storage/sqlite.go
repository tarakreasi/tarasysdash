package storage

import (
	"context"
	"database/sql"
	"log/slog"
	"time"

	_ "modernc.org/sqlite"
)

type Agent struct {
	ID        string    `json:"id"`
	Hostname  string    `json:"hostname"`
	IPAddress string    `json:"ip_address"`
	OS        string    `json:"os"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

type Metric struct {
	Timestamp        int64   `json:"timestamp"`
	CPUUsagePercent  float64 `json:"cpu_usage_percent"`
	MemoryUsedBytes  uint64  `json:"memory_used_bytes"`
	MemoryTotalBytes uint64  `json:"memory_total_bytes"`
	DiskFreePercent  float64 `json:"disk_free_percent"`
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
	query := `
	CREATE TABLE IF NOT EXISTS agents (
		id TEXT PRIMARY KEY,
		hostname TEXT NOT NULL,
		ip_address TEXT,
		os TEXT,
		created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
		updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
	);

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
	`
	_, err := db.Exec(query)
	return err
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
