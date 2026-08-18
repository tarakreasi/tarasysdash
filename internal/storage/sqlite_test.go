package storage

import (
	"context"
	"fmt"
	"path/filepath"
	"sync"
	"testing"
	"time"
)

func setupTestStore(t *testing.T) *SQLiteStore {
	t.Helper()
	dbPath := filepath.Join(t.TempDir(), "test_tara.db")
	store, err := NewSQLiteStore(dbPath)
	if err != nil {
		t.Fatalf("Failed to initialize test SQLite store: %v", err)
	}
	return store
}

func TestSQLiteStore_AgentLifecycle(t *testing.T) {
	store := setupTestStore(t)
	ctx := context.Background()

	// 1. Register Agent
	agent := &Agent{
		ID:           "srv-web-01",
		Hostname:     "web-node-1",
		IPAddress:    "192.168.1.10",
		OS:           "linux",
		RackLocation: "Rack-A",
	}

	if err := store.RegisterAgent(ctx, agent); err != nil {
		t.Fatalf("RegisterAgent failed: %v", err)
	}

	// 2. Token Association
	tokenHash := "mock-token-hash-12345"
	if err := store.UpdateAgentToken(ctx, agent.ID, tokenHash); err != nil {
		t.Fatalf("UpdateAgentToken failed: %v", err)
	}

	foundID, err := store.GetAgentIDByTokenHash(ctx, tokenHash)
	if err != nil {
		t.Fatalf("GetAgentIDByTokenHash failed: %v", err)
	}
	if foundID != agent.ID {
		t.Errorf("expected agent ID %s, got %s", agent.ID, foundID)
	}

	// 3. Update Metadata
	if err := store.UpdateAgentMetadata(ctx, agent.ID, "Rack-B", 42.5, 14); err != nil {
		t.Fatalf("UpdateAgentMetadata failed: %v", err)
	}

	// 4. Update Hostname
	if err := store.UpdateAgentHostname(ctx, agent.ID, "web-node-renamed"); err != nil {
		t.Fatalf("UpdateAgentHostname failed: %v", err)
	}

	// 5. List and Verify
	agents, err := store.ListAgents(ctx)
	if err != nil {
		t.Fatalf("ListAgents failed: %v", err)
	}
	if len(agents) != 1 {
		t.Fatalf("expected 1 agent, got %d", len(agents))
	}
	if agents[0].Hostname != "web-node-renamed" || agents[0].RackLocation != "Rack-B" {
		t.Errorf("agent metadata mismatch: %+v", agents[0])
	}

	// 6. Filter by Rack
	rackBAgents, err := store.ListAgentsByRack(ctx, "Rack-B")
	if err != nil {
		t.Fatalf("ListAgentsByRack failed: %v", err)
	}
	if len(rackBAgents) != 1 {
		t.Errorf("expected 1 agent in Rack-B, got %d", len(rackBAgents))
	}
}

func TestSQLiteStore_SaveAndGetMetrics(t *testing.T) {
	store := setupTestStore(t)
	ctx := context.Background()

	agentID := "srv-db-01"
	_ = store.RegisterAgent(ctx, &Agent{ID: agentID, Hostname: "db-node"})

	metric := &Metric{
		Timestamp:        time.Now().Unix(),
		CPUUsagePercent:  35.5,
		MemoryUsedBytes:  4 * 1024 * 1024 * 1024,
		MemoryTotalBytes: 16 * 1024 * 1024 * 1024,
		DiskUsage: []DiskStat{
			{Path: "/", TotalBytes: 100 * 1024 * 1024 * 1024, UsedBytes: 40 * 1024 * 1024 * 1024, FreePercent: 60.0},
		},
		BytesIn:       1024000,
		BytesOut:      512000,
		LatencyMs:     12.4,
		UptimeSeconds: 3600,
		ProcessCount:  120,
		Temperature:   48.0,
		Services: []ServiceStatus{
			{Name: "postgresql", Status: "running", Running: true},
		},
	}

	if err := store.SaveMetric(ctx, agentID, metric); err != nil {
		t.Fatalf("SaveMetric failed: %v", err)
	}

	// Retrieve recent metrics
	metrics, err := store.GetRecentMetrics(ctx, agentID, 10)
	if err != nil {
		t.Fatalf("GetRecentMetrics failed: %v", err)
	}
	if len(metrics) != 1 {
		t.Fatalf("expected 1 metric, got %d", len(metrics))
	}
	if metrics[0].CPUUsagePercent != 35.5 {
		t.Errorf("expected CPU 35.5, got %f", metrics[0].CPUUsagePercent)
	}
}

func TestSQLiteStore_ConcurrencyStressTest(t *testing.T) {
	store := setupTestStore(t)
	ctx := context.Background()

	const concurrentAgents = 30
	const metricsPerAgent = 10

	var wg sync.WaitGroup
	errCh := make(chan error, concurrentAgents*metricsPerAgent)

	// Pre-register agents
	for i := 0; i < concurrentAgents; i++ {
		agentID := fmt.Sprintf("stress-agent-%02d", i)
		_ = store.RegisterAgent(ctx, &Agent{
			ID:           agentID,
			Hostname:     fmt.Sprintf("host-%02d", i),
			RackLocation: fmt.Sprintf("Rack-%d", i%3),
		})
	}

	// Concurrently save metrics from 30 agents
	startTime := time.Now()
	for i := 0; i < concurrentAgents; i++ {
		wg.Add(1)
		go func(agentIdx int) {
			defer wg.Done()
			agentID := fmt.Sprintf("stress-agent-%02d", agentIdx)

			for m := 0; m < metricsPerAgent; m++ {
				metric := &Metric{
					Timestamp:        time.Now().Unix() + int64(m),
					CPUUsagePercent:  float64(10 + (agentIdx+m)%80),
					MemoryUsedBytes:  uint64((agentIdx + 1) * 1024 * 1024),
					MemoryTotalBytes: 8 * 1024 * 1024 * 1024,
					DiskUsage: []DiskStat{
						{Path: "/", TotalBytes: 50 * 1024 * 1024 * 1024, UsedBytes: 20 * 1024 * 1024 * 1024, FreePercent: 60.0},
					},
					BytesIn:   uint64(m * 1000),
					BytesOut:  uint64(m * 500),
					LatencyMs: float64(m * 2),
				}

				if err := store.SaveMetric(ctx, agentID, metric); err != nil {
					errCh <- fmt.Errorf("agent %s metric %d failed: %w", agentID, m, err)
					return
				}
			}
		}(i)
	}

	wg.Wait()
	close(errCh)

	duration := time.Since(startTime)
	t.Logf("✅ 300 Concurrent writes from 30 agents completed in %v", duration)

	// Check if any error occurred
	for err := range errCh {
		t.Fatalf("Concurrent stress test encountered error: %v", err)
	}

	// Verify total agents
	agents, err := store.ListAgents(ctx)
	if err != nil {
		t.Fatalf("ListAgents after stress test failed: %v", err)
	}
	if len(agents) != concurrentAgents {
		t.Errorf("expected %d agents, found %d", concurrentAgents, len(agents))
	}
}

func TestSQLiteStore_DeleteOldMetrics(t *testing.T) {
	store := setupTestStore(t)
	ctx := context.Background()

	agentID := "cleanup-agent"
	_ = store.RegisterAgent(ctx, &Agent{ID: agentID, Hostname: "cleanup-host"})

	// Insert fresh metric
	nowMetric := &Metric{
		Timestamp:       time.Now().Unix(),
		CPUUsagePercent: 10.0,
	}
	if err := store.SaveMetric(ctx, agentID, nowMetric); err != nil {
		t.Fatalf("SaveMetric failed: %v", err)
	}

	// Run cleanup with 7 days retention
	if err := store.DeleteOldMetrics(ctx, agentID, 7); err != nil {
		t.Fatalf("DeleteOldMetrics failed: %v", err)
	}

	// Fresh metric should remain
	metrics, err := store.GetRecentMetrics(ctx, agentID, 10)
	if err != nil {
		t.Fatalf("GetRecentMetrics failed: %v", err)
	}
	if len(metrics) != 1 {
		t.Errorf("expected 1 metric remaining, got %d", len(metrics))
	}
}
