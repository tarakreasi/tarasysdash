package main

import (
	"flag"
	"fmt"
	"os"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
	internalAgent "github.com/tarakreasi/taraSysDash/internal/agent"
	"github.com/tarakreasi/taraSysDash/internal/config"
	"github.com/tarakreasi/taraSysDash/internal/storage"
)

func main() {
	// 1. Identify Agent defaults
	defaultHostname, _ := os.Hostname()

	// 2. CLI Flags
	guiMode := flag.Bool("gui", false, "Enable GUI mode")
	serverURL := flag.String("server", "http://localhost:8080", "Server URL (e.g. http://10.200.150.85:8080)")
	s := flag.String("s", "", "Server URL (short)")
	rack := flag.String("rack", "", "Rack Location (e.g., 'Rack A')")
	r := flag.String("r", "", "Rack Location (short)")
	name := flag.String("name", defaultHostname, "Agent Name")
	n := flag.String("n", "", "Agent Name (short)")
	agentID := flag.String("id", "", "Agent ID (e.g. uuid)")

	flag.Parse()

	if *guiMode {
		runGUI(defaultHostname)
		return
	}

	// CLI Mode
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
	finalID, err := internalAgent.GetOrGenerateAgentID(*agentID)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to generate agent ID: %v\n", err)
		os.Exit(1)
	}

	agent := storage.Agent{
		ID:           finalID,
		Hostname:     finalName,
		OS:           "linux",
		RackLocation: finalRack,
	}

	internalAgent.Run(cfg, agent)
}

func runGUI(defaultHostname string) {
	myApp := app.New()
	myWindow := myApp.NewWindow("Tara Agent Setup")

	serverEntry := widget.NewEntry()
	serverEntry.SetPlaceHolder("http://localhost:8080")
	serverEntry.Text = "http://localhost:8080"

	rackEntry := widget.NewEntry()
	rackEntry.SetPlaceHolder("Rack Location")

	nameEntry := widget.NewEntry()
	nameEntry.SetText(defaultHostname)

	idEntry := widget.NewEntry()
	idEntry.SetPlaceHolder("Leave empty to generate new UUID")

	statusLabel := widget.NewLabel("Ready to start...")

	form := &widget.Form{
		Items: []*widget.FormItem{
			{Text: "Server URL", Widget: serverEntry},
			{Text: "Rack Location", Widget: rackEntry},
			{Text: "Agent Name", Widget: nameEntry},
			{Text: "Agent ID", Widget: idEntry},
		},
	}

	startButton := widget.NewButton("Start Agent", func() {
		// Disable inputs
		serverEntry.Disable()
		rackEntry.Disable()
		nameEntry.Disable()
		idEntry.Disable()
		// statusLabel.SetText("Starting agent...")
		// Note: Button disable logic inside callback might be delayed until next frame?
		// But here we want to kick off the agent in background.

		// Prepare Config
		cfg := config.Load()
		cfg.ServerURL = serverEntry.Text

		// Prepare Agent
		finalID, err := internalAgent.GetOrGenerateAgentID(idEntry.Text)
		if err != nil {
			statusLabel.SetText(fmt.Sprintf("Error: %v", err))
			return
		}

		agent := storage.Agent{
			ID:           finalID,
			Hostname:     nameEntry.Text,
			OS:           "linux",
			RackLocation: rackEntry.Text,
		}

		statusLabel.SetText("Agent Running...")

		// Run in background
		go internalAgent.Run(cfg, agent)
	})

	content := container.NewVBox(
		widget.NewLabel("Tara System Dashboard Agent"),
		form,
		startButton,
		statusLabel,
	)

	myWindow.SetContent(content)
	myWindow.Resize(fyne.NewSize(400, 300))
	myWindow.ShowAndRun()
}
