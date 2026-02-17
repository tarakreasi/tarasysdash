package storage

import (
	"context"
	"database/sql"
	"encoding/json"
	"log/slog"
	"sort"
	"sync"
	"time"

	_ "modernc.org/sqlite"
)

type Agent struct {
	ID               string    `json:"id"`
	Hostname         string    `json:"hostname"`
	IPAddress        string    `json:"ip_address"`
	OS               string    `json:"os"`
	RackLocation     string    `json:"rack_location"`
	Temperature      float64   `json:"temperature"`
	LogRetentionDays int       `json:"log_retention_days"`
	Status           string    `json:"status,omitempty"`
	CreatedAt        time.Time `json:"created_at"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type DiskStat struct {
	Path        string  `json:"path"`
	TotalBytes  uint64  `json:"total_bytes"`
	UsedBytes   uint64  `json:"used_bytes"`
	FreePercent float64 `json:"free_percent"`
}

type Metric struct {
	Timestamp        int64           `json:"timestamp"`
	CPUUsagePercent  float64         `json:"cpu_usage_percent"`
	MemoryUsedBytes  uint64          `json:"memory_used_bytes"`
	MemoryTotalBytes uint64          `json:"memory_total_bytes"`
	DiskUsage        []DiskStat      `json:"disk_usage"` // Replaces DiskFreePercent (deprecated/legacy)
	BytesIn          uint64          `json:"bytes_in"`
	BytesOut         uint64          `json:"bytes_out"`
	LatencyMs        float64         `json:"latency_ms"`
	Services         []ServiceStatus `json:"services"` // JSON stored
	UptimeSeconds    uint64          `json:"uptime_seconds"`
	ProcessCount     int             `json:"process_count"`
	Temperature      float64         `json:"temperature"`
}

// ServiceStatus mirror from collector (avoid cyclic dependency or redefine)
type ServiceStatus struct {
	Name    string `json:"name"`
	Status  string `json:"status"`
	Running bool   `json:"running"`
}

type SQLiteStore struct {
	db *sql.DB
	mu sync.Mutex // Serialize writes to prevent SQLITE_BUSY
}

func NewSQLiteStore(dbPath string) (*SQLiteStore, error) {
	// Optimization: WAL mode + Busy Timeout for high concurrency
	dsn := dbPath + "?_journal_mode=WAL&_busy_timeout=10000"
	db, err := sql.Open("sqlite", dsn)
	if err != nil {
		return nil, err
	}

	if err := db.Ping(); err != nil {
		return nil, err
	}

	// Explicitly set WAL mode
	if _, err := db.Exec("PRAGMA journal_mode=WAL;"); err != nil {
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
		// Phase 1: Add network metrics
		`ALTER TABLE system_metrics ADD COLUMN bytes_in INTEGER DEFAULT 0;`,
		`ALTER TABLE system_metrics ADD COLUMN bytes_out INTEGER DEFAULT 0;`,
		`ALTER TABLE system_metrics ADD COLUMN latency_ms REAL DEFAULT 0.0;`,
		// Sprint 1 (Refactor): Add disk_usage_json
		`ALTER TABLE system_metrics ADD COLUMN disk_usage_json TEXT DEFAULT '[]';`,
		// Sprint 6: Add log_retention_days
		`ALTER TABLE agents ADD COLUMN log_retention_days INTEGER DEFAULT 2;`,
		// Migration Fix: Ensure all agents (new/existing) follow 2-day rule by default
		`UPDATE agents SET log_retention_days = 2 WHERE log_retention_days > 2;`,
		// Sprint 7: Add detailed metrics (services, uptime, procs)
		`ALTER TABLE system_metrics ADD COLUMN services_json TEXT DEFAULT '[]';`,
		`ALTER TABLE system_metrics ADD COLUMN uptime_seconds INTEGER DEFAULT 0;`,
		`ALTER TABLE system_metrics ADD COLUMN process_count INTEGER DEFAULT 0;`,
		`ALTER TABLE system_metrics ADD COLUMN temperature REAL DEFAULT 0.0;`,
	}

	for _, query := range queries {
		_, err := db.Exec(query)
		// Ignore errors for ALTER TABLE (column might already exist)
		// We crudely check for duplicates by ignoring errors on specific queries (indices 2..8)
		if err != nil {
			slog.Info("Migration step note (ignoring potential error)", "query", query, "error", err)
		}
	}
	return nil
}

func (s *SQLiteStore) RegisterAgent(ctx context.Context, agent *Agent) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	query := `
	INSERT INTO agents (id, hostname, ip_address, os, rack_location, updated_at)
	VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
	ON CONFLICT(id) DO UPDATE SET
		hostname=excluded.hostname,
		ip_address=excluded.ip_address,
		os=excluded.os,
		rack_location=excluded.rack_location,
		updated_at=CURRENT_TIMESTAMP;
	`
	_, err := s.db.ExecContext(ctx, query, agent.ID, agent.Hostname, agent.IPAddress, agent.OS, agent.RackLocation)
	if err != nil {
		slog.Error("Failed to register agent", "error", err)
		return err
	}
	slog.Info("New Agent Registered/Updated", "id", agent.ID, "os", agent.OS, "rack", agent.RackLocation)
	return nil
}

func (s *SQLiteStore) SaveMetric(ctx context.Context, agentID string, m *Metric) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	diskJSON, _ := json.Marshal(m.DiskUsage)
	// Fallback for DiskFreePercent (legacy column) - use first disk or 0
	diskFree := 0.0
	if len(m.DiskUsage) > 0 {
		diskFree = m.DiskUsage[0].FreePercent
		// Or try to find "C:" or root? For now first one is fine.
	}

	servicesJSON, _ := json.Marshal(m.Services)

	query := `
	INSERT INTO system_metrics (
		time, agent_id, cpu_usage, memory_used, memory_total, disk_free_percent, 
		bytes_in, bytes_out, latency_ms, disk_usage_json, 
		services_json, uptime_seconds, process_count, temperature
	)
	VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
	`
	t := time.Unix(m.Timestamp, 0).UTC()
	_, err := s.db.ExecContext(ctx, query,
		t, agentID, m.CPUUsagePercent, m.MemoryUsedBytes, m.MemoryTotalBytes, diskFree,
		m.BytesIn, m.BytesOut, m.LatencyMs, string(diskJSON),
		string(servicesJSON), m.UptimeSeconds, m.ProcessCount, m.Temperature,
	)
	if err != nil {
		slog.Error("Failed to save metric", "error", err)
		return err
	}

	// Update agent heartbeat
	_, err = s.db.ExecContext(ctx, "UPDATE agents SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", agentID)
	return err
}

func (s *SQLiteStore) GetAgentIDByTokenHash(ctx context.Context, hash string) (string, error) {
	// Reads do NOT need the exclusive lock in WAL mode
	var id string
	query := `SELECT id FROM agents WHERE token_hash = ?`
	err := s.db.QueryRowContext(ctx, query, hash).Scan(&id)
	if err != nil {
		return "", err
	}
	return id, nil
}

func (s *SQLiteStore) UpdateAgentToken(ctx context.Context, agentID, hash string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	query := `UPDATE agents SET token_hash = ? WHERE id = ?`
	_, err := s.db.ExecContext(ctx, query, hash, agentID)
	return err
}

func (s *SQLiteStore) ListAgents(ctx context.Context) ([]Agent, error) {
	query := `SELECT id, hostname, ip_address, os, rack_location, temperature, log_retention_days, created_at, updated_at FROM agents ORDER BY updated_at DESC`
	rows, err := s.db.QueryContext(ctx, query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var agents []Agent
	for rows.Next() {
		var a Agent
		if err := rows.Scan(&a.ID, &a.Hostname, &a.IPAddress, &a.OS, &a.RackLocation, &a.Temperature, &a.LogRetentionDays, &a.CreatedAt, &a.UpdatedAt); err != nil {
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

func (s *SQLiteStore) UpdateAgentMetadata(ctx context.Context, agentID, rackLocation string, temperature float64, retentionDays int) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	query := `UPDATE agents SET rack_location = ?, temperature = ?, log_retention_days = ? WHERE id = ?`
	_, err := s.db.ExecContext(ctx, query, rackLocation, temperature, retentionDays, agentID)
	return err
}

func (s *SQLiteStore) DeleteOldMetrics(ctx context.Context, agentID string, retentionDays int) error {
	s.mu.Lock() // Potentially long operation, consider handling lock granularity if needed, but for WAL it's mostly fine
	defer s.mu.Unlock()

	cutoff := time.Now().AddDate(0, 0, -retentionDays)
	query := `DELETE FROM system_metrics WHERE agent_id = ? AND time < ?`
	_, err := s.db.ExecContext(ctx, query, agentID, cutoff)
	if err != nil {
		slog.Error("Failed to cleanup old metrics", "agent_id", agentID, "error", err)
	}
	return err
}

func (s *SQLiteStore) GetRecentMetrics(ctx context.Context, agentID string, limit int) ([]Metric, error) {
	query := `
		SELECT 
			cpu_usage, memory_used, memory_total, disk_free_percent, bytes_in, bytes_out, latency_ms, 
			IFNULL(disk_usage_json, '[]') as disk_usage_json, 
			IFNULL(services_json, '[]') as services_json, 
			IFNULL(uptime_seconds, 0) as uptime_seconds,
			IFNULL(process_count, 0) as process_count,
			IFNULL(temperature, 0.0) as temperature,
			time
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
		var diskJSON, servicesJSON string
		var diskFree float64
		if err := rows.Scan(
			&m.CPUUsagePercent, &m.MemoryUsedBytes, &m.MemoryTotalBytes, &diskFree,
			&m.BytesIn, &m.BytesOut, &m.LatencyMs, &diskJSON,
			&servicesJSON, &m.UptimeSeconds, &m.ProcessCount, &m.Temperature,
			&t,
		); err != nil {
			return nil, err
		}
		m.Timestamp = t.Unix()
		// Unmarshal
		if len(diskJSON) > 0 {
			_ = json.Unmarshal([]byte(diskJSON), &m.DiskUsage)
		}
		if len(servicesJSON) > 0 {
			_ = json.Unmarshal([]byte(servicesJSON), &m.Services)
		}
		metrics = append(metrics, m)
	}
	return metrics, rows.Err()
}

type NetworkStats struct {
	TotalBytesIn  uint64  `json:"total_bytes_in"`
	TotalBytesOut uint64  `json:"total_bytes_out"`
	AvgMbpsIn     float64 `json:"avg_mbps_in"`
	AvgMbpsOut    float64 `json:"avg_mbps_out"`
	PeakMbpsIn    float64 `json:"peak_mbps_in"`
	PeakMbpsOut   float64 `json:"peak_mbps_out"`
}

type LatencyStats struct {
	AvgLatency float64   `json:"avg_latency_ms"`
	MinLatency float64   `json:"min_latency_ms"`
	MaxLatency float64   `json:"max_latency_ms"`
	P95Latency float64   `json:"p95_latency_ms"`
	History    []float64 `json:"history"`
}

func (s *SQLiteStore) GetNetworkStats(ctx context.Context, agentID string, limit int) (*NetworkStats, error) {
	query := `
SELECT bytes_in, bytes_out
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

	var stats NetworkStats
	var measurements []struct{ bytesIn, bytesOut uint64 }

	for rows.Next() {
		var m struct{ bytesIn, bytesOut uint64 }
		if err := rows.Scan(&m.bytesIn, &m.bytesOut); err != nil {
			return nil, err
		}
		measurements = append(measurements, m)
	}

	if len(measurements) == 0 {
		return &stats, nil
	}

	stats.TotalBytesIn = measurements[0].bytesIn
	stats.TotalBytesOut = measurements[0].bytesOut

	// Calculate Mbps for each interval
	var mbpsInValues, mbpsOutValues []float64
	for i := 1; i < len(measurements); i++ {
		bytesDiffIn := float64(measurements[i-1].bytesIn - measurements[i].bytesIn)
		bytesDiffOut := float64(measurements[i-1].bytesOut - measurements[i].bytesOut)
		mbpsIn := (bytesDiffIn * 8) / (1024 * 1024)
		mbpsOut := (bytesDiffOut * 8) / (1024 * 1024)
		mbpsInValues = append(mbpsInValues, mbpsIn)
		mbpsOutValues = append(mbpsOutValues, mbpsOut)
	}

	if len(mbpsInValues) > 0 {
		var sumIn, sumOut, maxIn, maxOut float64
		for i, v := range mbpsInValues {
			sumIn += v
			sumOut += mbpsOutValues[i]
			if v > maxIn {
				maxIn = v
			}
			if mbpsOutValues[i] > maxOut {
				maxOut = mbpsOutValues[i]
			}
		}
		stats.AvgMbpsIn = sumIn / float64(len(mbpsInValues))
		stats.AvgMbpsOut = sumOut / float64(len(mbpsOutValues))
		stats.PeakMbpsIn = maxIn
		stats.PeakMbpsOut = maxOut
	}

	return &stats, rows.Err()
}

func (s *SQLiteStore) GetLatencyStats(ctx context.Context, agentID string, limit int) (*LatencyStats, error) {
	query := `
SELECT latency_ms
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

	var stats LatencyStats
	var latencies []float64

	for rows.Next() {
		var lat float64
		if err := rows.Scan(&lat); err != nil {
			return nil, err
		}
		latencies = append(latencies, lat)
	}

	if len(latencies) == 0 {
		return &stats, nil
	}

	stats.History = latencies
	stats.MinLatency = latencies[0]
	stats.MaxLatency = latencies[0]
	var sum float64

	for _, lat := range latencies {
		sum += lat
		if lat < stats.MinLatency {
			stats.MinLatency = lat
		}
		if lat > stats.MaxLatency {
			stats.MaxLatency = lat
		}
	}

	stats.AvgLatency = sum / float64(len(latencies))

	// Calculate P95
	sorted := make([]float64, len(latencies))
	copy(sorted, latencies)
	sort.Float64s(sorted)
	p95Index := int(float64(len(sorted)) * 0.95)
	if p95Index < len(sorted) {
		stats.P95Latency = sorted[p95Index]
	}

	return &stats, rows.Err()
}

type GlobalMetric struct {
	Timestamp int64   `json:"timestamp"`
	AvgCPU    float64 `json:"avg_cpu"`
	AvgMemory float64 `json:"avg_memory"`
}

func (s *SQLiteStore) GetGlobalMetrics(ctx context.Context, limit int) ([]GlobalMetric, error) {
	query := `
		SELECT 
			strftime('%s', substr(time, 1, 19)) / 5 * 5 as timestamp_bucket,
			AVG(cpu_usage) as avg_cpu,
			AVG(memory_used) as avg_mem
		FROM system_metrics
		WHERE time IS NOT NULL
		GROUP BY timestamp_bucket
		HAVING timestamp_bucket IS NOT NULL
		ORDER BY timestamp_bucket DESC
		LIMIT ?
	`
	rows, err := s.db.QueryContext(ctx, query, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var metrics []GlobalMetric
	for rows.Next() {
		var m GlobalMetric
		if err := rows.Scan(&m.Timestamp, &m.AvgCPU, &m.AvgMemory); err != nil {
			return nil, err
		}
		metrics = append(metrics, m)
	}
	return metrics, rows.Err()
}

func (s *SQLiteStore) ListAgentsByRack(ctx context.Context, rackLocation string) ([]Agent, error) {
	query := `SELECT id, hostname, ip_address, os, rack_location, temperature, log_retention_days, created_at, updated_at 
          FROM agents 
          WHERE rack_location = ? 
          ORDER BY updated_at DESC`
	rows, err := s.db.QueryContext(ctx, query, rackLocation)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var agents []Agent
	for rows.Next() {
		var a Agent
		if err := rows.Scan(&a.ID, &a.Hostname, &a.IPAddress, &a.OS, &a.RackLocation, &a.Temperature, &a.LogRetentionDays, &a.CreatedAt, &a.UpdatedAt); err != nil {
			return nil, err
		}
		if time.Since(a.UpdatedAt) > 30*time.Second {
			a.Status = "offline"
		} else {
			a.Status = "online"
		}
		agents = append(agents, a)
	}
	return agents, rows.Err()
}

func (s *SQLiteStore) UpdateAgentHostname(ctx context.Context, agentID, hostname string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	query := `UPDATE agents SET hostname = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?`
	_, err := s.db.ExecContext(ctx, query, hostname, agentID)
	return err
}
