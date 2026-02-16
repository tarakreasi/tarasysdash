#!/bin/bash

# Function to kill background processes on exit
cleanup() {
    echo "Stopping all services..."
    kill $(jobs -p) 2>/dev/null
}
trap cleanup EXIT

echo "🚀 Starting TaraSysDash Local Development Environment..."

# 1. Build & Run Server
echo "📦 Building Server..."
go build -o bin/server ./cmd/server
if [ $? -ne 0 ]; then
    echo "❌ Server build failed"
    exit 1
fi

echo "🟢 Starting Server (Port 8080)..."
./bin/server > server.log 2>&1 &
SERVER_PID=$!
echo "   Server PID: $SERVER_PID"

# Wait for server to be ready
sleep 2

# 2. Build & Run CLI Agent
echo "📦 Building CLI Agent..."
go build -o bin/agent-cli ./cmd/agent-cli
if [ $? -ne 0 ]; then
    echo "❌ Agent build failed"
    exit 1
fi

echo "🟢 Starting Agent..."
./bin/agent-cli -server http://localhost:8080 -name "local-dev-agent" -id "p1" > agent.log 2>&1 &
AGENT_PID=$!
echo "   Agent PID: $AGENT_PID"

# 3. Start Frontend
echo "💻 Starting Frontend (Port 5173)..."
echo "   Opening in standard output..."
cd web
npm run dev
