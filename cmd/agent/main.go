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

	// Handshake: Register and get Token
	if cfg.AgentToken == "" {
		logger.Log.Info("No token found. Attempting to register via Handshake...")
		token, err := registerAgent(cfg.ServerURL)
		if err != nil {
			logger.Log.Error("Failed to register agent. Exiting.", "error", err)
			os.Exit(1)
		}
		cfg.AgentToken = token
		logger.Log.Info("Handshake successful! Token obtained.")
	}

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

		// Prepare request
		req, err := http.NewRequest("POST", cfg.ServerURL+"/api/v1/metrics", bytes.NewBuffer(jsonData))
		if err != nil {
			logger.Log.Error("Failed to create request", "error", err)
			continue
		}
		req.Header.Set("Content-Type", "application/json")
		if cfg.AgentToken != "" {
			req.Header.Set("Authorization", "Bearer "+cfg.AgentToken)
		} else {
			logger.Log.Warn("Agent token is missing! Request will likely fail.")
		}

		// Send request
		client := &http.Client{Timeout: 5 * time.Second}
		resp, err := client.Do(req)
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

func registerAgent(serverURL string) (string, error) {
	// 1. Gather Basic Info
	hostname, _ := os.Hostname()
	// Simple OS detection (mock for now, or use runtime.GOOS)
	agentOS := "linux" // default

	payload := map[string]string{
		"id":            "agent-uuid-1", // Fixed for MVP. In prod use machine-id or uuid
		"hostname":      hostname,
		"os":            agentOS,
		"status":        "online",
		"rack_location": "Rack 1", // Default
	}

	jsonData, _ := json.Marshal(payload)
	resp, err := http.Post(serverURL+"/api/v1/register", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", http.ErrNoCookie // Just a generic error
	}

	var result struct {
		Status string `json:"status"`
		Token  string `json:"token"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return "", err
	}
	return result.Token, nil
}
