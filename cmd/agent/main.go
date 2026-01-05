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

	"github.com/google/uuid"
	"github.com/tarakreasi/taraSysDash/internal/collector"
	"github.com/tarakreasi/taraSysDash/internal/config"
	"github.com/tarakreasi/taraSysDash/internal/logger"
	"github.com/tarakreasi/taraSysDash/internal/storage"
)

func main() {
	// 1. Identify Agent defaults
	defaultHostname, _ := os.Hostname()

	// 2. CLI Flags
	serverURL := flag.String("server", "http://localhost:8080", "Server URL (e.g. http://10.200.150.85:8080)")
	s := flag.String("s", "", "Server URL (short)")
	rack := flag.String("rack", "", "Rack Location (e.g., 'Rack A')")
	r := flag.String("r", "", "Rack Location (short)")
	name := flag.String("name", defaultHostname, "Agent Name")
	n := flag.String("n", "", "Agent Name (short)")
	agentID := flag.String("id", "", "Agent ID (e.g. uuid)")

	flag.Parse()

	// Load config
	cfg := config.Load()

	// Override config with flags (Short flags take precedence over long flags)
	if *s != "" {
		cfg.ServerURL = *s
	} else if *serverURL != "http://localhost:8080" || cfg.ServerURL == "" {
		cfg.ServerURL = *serverURL
	}

	finalRack := *rack
	if *r != "" {
		finalRack = *r
	}

	finalName := *name
	if *n != "" {
		finalName = *n
	}

	// 3. Identification
	finalID := *agentID
	if finalID == "" {
		// Generate one if not provided.
		// NOTE: In production, this should be persisted to disk so it survives restarts.
		// For now, if you want persistence, pass -id explicitly.
		finalID = uuid.New().String()
	}

	agent := storage.Agent{
		ID:           finalID,
		Hostname:     finalName,
		OS:           "linux",
		RackLocation: finalRack,
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
			"agent_id":           finalID,
			"timestamp":          metrics.Timestamp,
			"cpu_usage_percent":  metrics.CPUUsagePercent,
			"memory_used_bytes":  metrics.MemoryUsedBytes,
			"memory_total_bytes": metrics.MemoryTotalBytes,
			"disk_usage":         metrics.DiskUsage,
			"bytes_in":           metrics.BytesIn,
			"bytes_out":          metrics.BytesOut,
			"services":           metrics.Services,
			"uptime_seconds":     metrics.UptimeSeconds,
			"process_count":      metrics.ProcessCount,
			"temperature":        metrics.Temperature,
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
