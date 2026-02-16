package main

import (
	"flag"
	"fmt"
	"os"

	internalAgent "github.com/tarakreasi/taraSysDash/internal/agent"
	"github.com/tarakreasi/taraSysDash/internal/config"
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

	// Override config with flags
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
	finalID, err := internalAgent.GetOrGenerateAgentID(*agentID)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to generate agent ID: %v\n", err)
		os.Exit(1)
	}

	agent := storage.Agent{
		ID:           finalID,
		Hostname:     finalName,
		OS:           "linux", // Will be corrected by runner based on dynamic info
		RackLocation: finalRack,
	}

	internalAgent.Run(cfg, agent)
}
