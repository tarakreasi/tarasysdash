#!/bin/bash

# Agent and Server Configuration
SERVER_URL="http://10.200.150.85:8080"
AGENT_NAME="Rec"
RACK_LOCATION="Production Rack A"

# Run the agent using new short flags
./bin/tara-agent -s "$SERVER_URL" -n "$AGENT_NAME" -r "$RACK_LOCATION"
