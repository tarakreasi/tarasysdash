GO_BIN := go
APP_NAME := tara
SERVER_BIN := bin/tara-server
AGENT_BIN_LINUX := bin/tara-agent
AGENT_BIN_WINDOWS := bin/tara-agent-windows-amd64.exe

.PHONY: all build-all clean

all: build-all

build-all: build-server build-agent-linux build-agent-windows

build-server:
	@echo "Building Server (Linux)..."
	@mkdir -p bin
	$(GO_BIN) build -o $(SERVER_BIN) ./cmd/server

build-server-windows:
	@echo "Building Server (Windows amd64)..."
	@mkdir -p bin
	GOOS=windows GOARCH=amd64 $(GO_BIN) build -o bin/tara-agent-windows-amd64.exe ./cmd/server

build-agent-linux:
	@echo "Building Agent (Linux amd64)..."
	@mkdir -p bin
	GOOS=linux GOARCH=amd64 $(GO_BIN) build -o $(AGENT_BIN_LINUX) ./cmd/agent

build-agent-windows:
	@echo "Building Agent (Windows amd64)..."
	@mkdir -p bin
	GOOS=windows GOARCH=amd64 $(GO_BIN) build -o $(AGENT_BIN_WINDOWS) ./cmd/agent

clean:
	@echo "Cleaning bin/..."
	@rm -rf bin

dev:
	@echo "Starting Full Stack Dev Environment..."
	@# Run Server in background, then Frontend
	@# formatting: ensure we kill child processes on exit
	@trap 'kill 0' EXIT; \
	$(GO_BIN) run cmd/server/main.go & \
	cd web && CI=true npm run dev
