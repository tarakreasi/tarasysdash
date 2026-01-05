package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/tarakreasi/taraSysDash/internal/collector"
	"github.com/tarakreasi/taraSysDash/internal/config"
	"github.com/tarakreasi/taraSysDash/internal/logger"
	"github.com/tarakreasi/taraSysDash/internal/storage"
)

func main() {
	// CLI Flags
	serverURL := flag.String("server", "http://localhost:8080", "Server URL")
	rack := flag.String("rack", "", "Rack Location (e.g., 'Rack A')")
	flag.Parse()

	// Load config
	cfg := config.Load()
	// Override if flag is set, though cfg loads from env. Flags usually take precedence or specific flow.
	// In this code, cfg seems to already load SERVER_URL from env.
	// But let's respect the CLI flag if it's different/default?
	// The original code used `*serverURL` in registerAgent, but `cfg.ServerURL` in metrics loop.
	// Let's ensure consistent usage. Ideally update cfg.ServerURL with flag if flag is not default.
	cfg.ServerURL = *serverURL

	// 1. Identify Agent
	hostname, _ := os.Hostname()
	agent := storage.Agent{
		ID:           "agent-uuid-1", // TODO: Persist UUID properly
		Hostname:     hostname,
		OS:           "linux", // TODO: Detect OS
		RackLocation: *rack,
	}

	logger.Init(cfg.LogLevel)
	logger.Log.Info("Starting tara-agent...", "interval", cfg.AgentInterval)

	col := collector.New()

	// Handshake: Register and get Token
	if cfg.AgentToken == "" {
		logger.Log.Info("No token found. Attempting to register via Handshake...")
		token, err := registerAgent(cfg.ServerURL, agent)
		if err != nil {
			logger.Log.Error("Failed to register agent", "error", err)
			os.Exit(1)
		}
		cfg.AgentToken = token
		logger.Log.Info("Agent registered successfully", "token_snippet", token[:8]+"...")
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

	// Services to monitor (Critical VMS services)
	// In production, this should be configurable.
	criticalServices := []string{
		"RecordingServer",
		"MilestoneService",
		"VideoOS Event Server",
	}

	for range ticker.C {
		metrics, err := col.GetMetrics(criticalServices)
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
			"disk_usage":         metrics.DiskUsage,
			"bytes_in":           metrics.BytesIn,
			"bytes_out":          metrics.BytesOut,
			"services":           metrics.Services,
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

func registerAgent(serverURL string, agent storage.Agent) (string, error) {
	// 1. Gather Basic Info
	agent.Status = "online"
	if agent.RackLocation == "" {
		agent.RackLocation = "Unknown"
	}

	payload := agent // Use struct directly

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
