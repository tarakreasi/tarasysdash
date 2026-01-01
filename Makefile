BINARY_NAME=tara-agent
MAIN_PATH=cmd/agent/main.go

.PHONY: all build run clean lint

all: build

build:
	@echo "Building $(BINARY_NAME)..."
	@mkdir -p bin
	@go build -o bin/$(BINARY_NAME) $(MAIN_PATH)

run: build
	@echo "Running $(BINARY_NAME)..."
	@./bin/$(BINARY_NAME)

clean:
	@echo "Cleaning..."
	@rm -rf bin/

lint:
	@echo "Running linters..."
	@golangci-lint run
