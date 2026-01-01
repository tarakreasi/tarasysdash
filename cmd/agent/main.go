package main

import (
	"encoding/json"
	"fmt"
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

		// For Sprint 1, we just print JSON to stdout
		jsonData, err := json.Marshal(metrics)
		if err != nil {
			logger.Log.Error("Failed to marshal metrics", "error", err)
			continue
		}

		fmt.Println(string(jsonData))
	}
}
