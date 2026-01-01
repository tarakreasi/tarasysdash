APP_NAME := tara
SERVER_BIN := bin/server
AGENT_BIN_LINUX := bin/agent-linux-amd64
AGENT_BIN_WINDOWS := bin/agent-windows-amd64.exe

.PHONY: all build-all clean

all: build-all

build-all: build-server build-agent-linux build-agent-windows

build-server:
	@echo "Building Server (Linux)..."
	@mkdir -p bin
	go build -o $(SERVER_BIN) ./cmd/server

build-server-windows:
	@echo "Building Server (Windows amd64)..."
	@mkdir -p bin
	GOOS=windows GOARCH=amd64 go build -o bin/server-windows-amd64.exe ./cmd/server

build-agent-linux:
	@echo "Building Agent (Linux amd64)..."
	@mkdir -p bin
	GOOS=linux GOARCH=amd64 go build -o $(AGENT_BIN_LINUX) ./cmd/agent

build-agent-windows:
	@echo "Building Agent (Windows amd64)..."
	@mkdir -p bin
	GOOS=windows GOARCH=amd64 go build -o $(AGENT_BIN_WINDOWS) ./cmd/agent

clean:
	@echo "Cleaning bin/..."
	@rm -rf bin

dev:
	@echo "Starting Full Stack Dev Environment..."
	@# Run Server in background, then Frontend
	@# formatting: ensure we kill child processes on exit
	@trap 'kill 0' EXIT; \
	go run cmd/server/main.go & \
	cd web && CI=true npm run dev
