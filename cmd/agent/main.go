package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/tarakreasi/taraSysDash/internal/collector"
	"github.com/tarakreasi/taraSysDash/internal/config"
	"github.com/tarakreasi/taraSysDash/internal/logger"
)

func main() {
	cfg := config.Load()
	logger.Init(cfg.LogLevel)

	logger.Log.Info("Starting tara-agent...", "interval", cfg.AgentInterval)

	col := collector.New()

	ticker := time.NewTicker(cfg.AgentInterval)
	defer ticker.Stop()

	// Graceful shutdown
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		<-sigChan
		logger.Log.Info("Shutting down tara-agent...")
		os.Exit(0)
	}()

	for range ticker.C {
		metrics, err := col.GetMetrics()
		if err != nil {
			logger.Log.Error("Failed to collect metrics", "error", err)
			continue
		}

		// Send payload to server
		payload := map[string]interface{}{
			"agent_id":           "agent-uuid-1", // Mock ID for Sprint 2
			"timestamp":          metrics.Timestamp,
			"cpu_usage_percent":  metrics.CPUUsagePercent,
			"memory_used_bytes":  metrics.MemoryUsedBytes,
			"memory_total_bytes": metrics.MemoryTotalBytes,
			"disk_free_percent":  metrics.DiskFreePercent,
		}

		// Marshal payload
		jsonData, err := json.Marshal(payload)
		if err != nil {
			logger.Log.Error("Failed to marshal metrics", "error", err)
			continue
		}

		// POST to server
		resp, err := http.Post(cfg.ServerURL+"/api/v1/metrics", "application/json", bytes.NewBuffer(jsonData))
		if err != nil {
			logger.Log.Error("Failed to send metrics", "error", err)
			continue
		}
		resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			logger.Log.Error("Server returned non-200 status", "status", resp.StatusCode)
		} else {
			logger.Log.Info("Metrics sent successfully")
		}
	}
}
