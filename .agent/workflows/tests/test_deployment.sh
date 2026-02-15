#!/bin/bash
set -e

# Semi-Agentic Toolkit Deployment Test Suite
# Usage: ./test_deployment.sh

TOOLKIT_ROOT=$(cd "$(dirname "$0")/.." && pwd)
TEST_DIR="/tmp/toolkit-test-$(date +%s)"

echo "🧪 Starting Deployment Test Suite..."
echo "📂 Test Directory: $TEST_DIR"

cleanup() {
    echo "🧹 Cleaning up..."
    # rm -rf "$TEST_DIR" # Commented out for debugging
    echo "   (Test directory preserved for inspection: $TEST_DIR)"
}
trap cleanup EXIT

# Test 1: Fresh Install
echo "---------------------------------------------------"
echo "TEST 1: Fresh Installation (Greenfield)"
mkdir -p "$TEST_DIR/greenfield"
cd "$TEST_DIR/greenfield"

"$TOOLKIT_ROOT/scripts/deploy.sh" . > deploy.log 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Deploy Script Exit Code: 0"
else
    echo "❌ Deploy Script Failed! See deploy.log"
    cat deploy.log
    exit 1
fi

if [ -f "scripts/validate.sh" ]; then
    bash scripts/validate.sh .
    echo "✅ Validation: Passed"
else
    echo "❌ Validation: Failed (Script missing)"
    exit 1
fi

# Manual check for structure
[ -d ".agent/automation" ] && echo "✅ Structure: .agent/automation exists" || exit 1
[ -f "SPRINT_GUIDE.md" ] && echo "✅ Structure: SPRINT_GUIDE.md exists" || exit 1

# Test 2: Supervisor Execution
echo "---------------------------------------------------"
echo "TEST 2: Supervisor Dry Run"
source .agent/automation/.venv/bin/activate
STATUS_OUTPUT=$(python .agent/automation/supervisor_cli.py status)
if [[ "$STATUS_OUTPUT" == *"Supervisor Status"* ]]; then
     echo "✅ Supervisor Status Check: Passed"
else
     echo "❌ Supervisor Status Check: Failed"
     echo "Output: $STATUS_OUTPUT"
     exit 1
fi
deactivate

echo "---------------------------------------------------"
echo "🎉 ALL TESTS PASSED!"
echo "---------------------------------------------------"
