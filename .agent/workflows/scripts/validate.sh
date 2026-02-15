#!/bin/bash
set -e

# Semi-Agentic Toolkit Validation Script
# Usage: ./validate.sh [TARGET_DIR]

TARGET_DIR=${1:-.}

echo "🧪 Validating deployment in: $TARGET_DIR"

# Check Directories
if [ ! -d "$TARGET_DIR/.agent/automation" ]; then
    echo "❌ Error: Automation directory missing!"
    exit 1
fi

if [ ! -d "$TARGET_DIR/docs/dev/sprints" ]; then
    echo "❌ Error: Sprints directory missing!"
    exit 1
fi

# Check Python Venv
if [ ! -f "$TARGET_DIR/.agent/automation/.venv/bin/python" ]; then
    echo "❌ Error: Python virtualenv missing or broken!"
    exit 1
fi

# Check Supervisor Runnable
echo "   Testing Supervisor executable..."
if "$TARGET_DIR/.agent/automation/.venv/bin/python" "$TARGET_DIR/.agent/automation/supervisor_cli.py" status > /dev/null 2>&1; then
    echo "✅ Supervisor is runnable."
else
    echo "❌ Error: Supervisor failed to start!"
    exit 1
fi

echo "✅ Validation Passed!"
