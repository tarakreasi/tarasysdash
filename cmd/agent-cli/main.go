package main

import (
	"flag"
	"fmt"
	"os"
	"runtime"
	"time"

	"github.com/tarakreasi/taraSysDash/internal/agent"
	"github.com/tarakreasi/taraSysDash/internal/config"
	"github.com/tarakreasi/taraSysDash/internal/storage"
)

func main() {
	defaultHostname, _ := os.Hostname()

	serverURL := flag.String("server", "http://localhost:8080", "Server URL")
	rack := flag.String("rack", "Lab-CLI", "Rack Location")
	name := flag.String("name", defaultHostname, "Agent Name")
	agentID := flag.String("id", "", "Agent ID (defaults to hostname if empty)")
	interval := flag.Int("interval", 1, "Reporting Interval (seconds)")

	flag.Parse()

	cfg := config.Load()
	cfg.ServerURL = *serverURL
	if *interval > 0 {
		cfg.AgentInterval = time.Duration(*interval) * time.Second
	}

	finalID, err := agent.GetOrGenerateAgentID(*agentID)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to generate agent ID: %v\n", err)
		os.Exit(1)
	}

	agentMeta := storage.Agent{
		ID:           finalID,
		Hostname:     *name,
		OS:           runtime.GOOS,
		RackLocation: *rack,
	}

	fmt.Printf("Starting CLI Agent: %s (%s) at %s\n", *name, finalID, *serverURL)
	agent.Run(cfg, agentMeta)
}
