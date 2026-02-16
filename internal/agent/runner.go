package agent

import (
	"bytes"
	"encoding/json"
	"fmt"
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

var (
	lastBytesIn  uint64
	lastBytesOut uint64
	lastTime     time.Time
)

// Run starts the agent with the given configuration and agent metadata.
func Run(cfg *config.Config, agent storage.Agent) {
	logger.Init(cfg.LogLevel)
	logger.Log.Info("Starting tara-agent...", "interval", cfg.AgentInterval)

	col := collector.New()

	// Handshake: Register and get Token
	if cfg.AgentToken == "" {
		logger.Log.Info("No token found. Attempting to register via Handshake...")
		token, err := registerAgent(cfg.ServerURL, agent)
		if err != nil {
			logger.Log.Error("Failed to register agent", "error", err)
			// In a GUI context, we might want to return this error instead of exiting.
			// But for now, keeping behavior consistent with CLI.
			// We'll modify this later if needed.
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
		"Milestone XProtect Recording Server",
		"Milestone XProtect Management Server",
		"Milestone XProtect Event Server",
	}

	for range ticker.C {
		metrics, err := col.GetMetrics(criticalServices)
		if err != nil {
			logger.Log.Error("Failed to collect metrics", "error", err)
			continue
		}

		// Send with retry
		err = sendMetricsWithRetry(cfg, agent, metrics)
		if err != nil {
			logger.Log.Error("Failed to send metrics after retries", "error", err)
		}

		// Print live stats to console
		printLiveStats(metrics)
	}
}

func printLiveStats(m *collector.SystemMetrics) {
	now := time.Now()
	if !lastTime.IsZero() {
		duration := now.Sub(lastTime).Seconds()
		if duration > 0 {
			diffIn := float64(m.BytesIn-lastBytesIn) / duration / 1024 / 1024 * 8    // Mbps
			diffOut := float64(m.BytesOut-lastBytesOut) / duration / 1024 / 1024 * 8 // Mbps
			fmt.Printf("\r[%s] CPU: %.1f%% | RAM: %.1fGB | NET: ↓%.2f Mbps ↑%.2f Mbps          ",
				now.Format("15:04:05"),
				m.CPUUsagePercent,
				float64(m.MemoryUsedBytes)/1073741824,
				diffIn,
				diffOut,
			)
		}
	} else {
		fmt.Printf("[%s] Agent Running... Waiting for first delta metrics.\n", now.Format("15:04:05"))
	}
	lastBytesIn = m.BytesIn
	lastBytesOut = m.BytesOut
	lastTime = now
}

// HTTPError represents an HTTP error response
type HTTPError struct {
	StatusCode int
	Status     string
}

func (e *HTTPError) Error() string {
	return fmt.Sprintf("HTTP %d: %s", e.StatusCode, e.Status)
}

// isRetryable checks if an error is retryable (5xx server error)
func isRetryable(err error) bool {
	if httpErr, ok := err.(*HTTPError); ok {
		return httpErr.StatusCode >= 500 && httpErr.StatusCode < 600
	}
	return false
}

// sendMetricsWithRetry sends metrics with exponential backoff retry
func sendMetricsWithRetry(cfg *config.Config, agent storage.Agent, metrics *collector.SystemMetrics) error {
	const maxRetries = 3
	baseDelay := 100 * time.Millisecond

	for attempt := 0; attempt < maxRetries; attempt++ {
		err := sendMetrics(cfg, agent, metrics)

		// Success
		if err == nil {
			if attempt > 0 {
				logger.Log.Info("Metrics sent successfully after retry", "attempts", attempt+1)
			} else {
				logger.Log.Info("Metrics sent successfully")
			}
			return nil
		}

		// Check if retryable
		if !isRetryable(err) {
			return err // Don't retry non-5xx errors
		}

		// Last attempt failed
		if attempt == maxRetries-1 {
			return err
		}

		// Exponential backoff
		delay := baseDelay * (1 << attempt) // 100ms, 200ms, 400ms
		logger.Log.Warn("Retrying after server error", "attempt", attempt+1, "max", maxRetries, "delay", delay, "error", err)
		time.Sleep(delay)
	}
	return nil
}

// sendMetrics sends a single metric payload to the server
func sendMetrics(cfg *config.Config, agent storage.Agent, metrics *collector.SystemMetrics) error {
	// Send payload to server
	payload := map[string]interface{}{
		"agent_id":           agent.ID,
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
		return fmt.Errorf("failed to marshal metrics: %w", err)
	}

	// Prepare request
	req, err := http.NewRequest("POST", cfg.ServerURL+"/api/v1/metrics", bytes.NewBuffer(jsonData))
	if err != nil {
		return fmt.Errorf("failed to create request: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")
	if cfg.AgentToken != "" {
		req.Header.Set("Authorization", "Bearer "+cfg.AgentToken)
	}

	// Send request
	client := &http.Client{Timeout: 5 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return fmt.Errorf("failed to send request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return &HTTPError{StatusCode: resp.StatusCode, Status: resp.Status}
	}

	return nil
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
