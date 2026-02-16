//go:build gui_agent

package main

import (
	"fmt"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
	internalAgent "github.com/tarakreasi/taraSysDash/internal/agent"
	"github.com/tarakreasi/taraSysDash/internal/config"
	"github.com/tarakreasi/taraSysDash/internal/storage"
)

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
		serverEntry.Disable()
		rackEntry.Disable()
		nameEntry.Disable()
		idEntry.Disable()

		cfg := config.Load()
		cfg.ServerURL = serverEntry.Text

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
