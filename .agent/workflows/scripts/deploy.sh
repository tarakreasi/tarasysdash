#!/bin/bash
set -e

# Semi-Agentic Toolkit Deployment Script
# Usage: ./deploy.sh [TARGET_DIR]

TARGET_DIR=${1:-.}
TOOLKIT_ROOT=$(cd "$(dirname "$0")/.." && pwd)

echo "🚀 Deploying Semi-Agentic Toolkit to: $TARGET_DIR"

# 1. Check Dependencies
echo "🔍 Checking dependencies..."
command -v rsync >/dev/null 2>&1 || { echo >&2 "rsync is required but not installed. Aborting."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo >&2 "python3 is required but not installed. Aborting."; exit 1; }

# 2. Prepare Target Structure
echo "📂 Creating directory structure..."
mkdir -p "$TARGET_DIR/.agent"
mkdir -p "$TARGET_DIR/docs/dev/sprints"

# 3. Copy Core Engine (using rsync with exclude)
echo "📦 Installing Automation Engine..."
rsync -av --update --delete \
    --exclude '__pycache__' \
    --exclude '.venv' \
    --exclude '*.pyc' \
    "$TOOLKIT_ROOT/automation/" "$TARGET_DIR/.agent/automation/"

# 4. Copy Workflows
echo "📜 Installing Protocols..."
mkdir -p "$TARGET_DIR/.agent/workflows"
rsync -av --update "$TOOLKIT_ROOT/.agent/workflows/" "$TARGET_DIR/.agent/workflows/"

# 5. Copy Documentation Template
echo "📚 Installing Documentation..."
cp "$TOOLKIT_ROOT/SPRINT_GUIDE.md" "$TARGET_DIR/SPRINT_GUIDE.md"
cp "$TOOLKIT_ROOT/PM.md" "$TARGET_DIR/.agent/PM.md"
cp "$TOOLKIT_ROOT/OPTIONAL_TOOLS.md" "$TARGET_DIR/.agent/OPTIONAL_TOOLS.md"

if [ ! -f "$TARGET_DIR/.agent/current_sprint.md" ]; then
    echo "# Current Sprint: IDLE" > "$TARGET_DIR/.agent/current_sprint.md"
    echo "**Status**: WAIT_FOR_PLAN" >> "$TARGET_DIR/.agent/current_sprint.md"
fi

# 6. Setup Python Environment
echo "🐍 Setting up Python environment..."
cd "$TARGET_DIR/.agent/automation"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "   Virtualenv created."
else
    echo "   Virtualenv already exists."
fi

# Install Dependencies
echo "   Installing dependencies..."
./.venv/bin/pip install -e . > /dev/null

# 7. Validation
echo "✅ Validating installation..."
if [ -f "$TOOLKIT_ROOT/scripts/validate.sh" ]; then
    bash "$TOOLKIT_ROOT/scripts/validate.sh" "$TARGET_DIR"
fi

echo "🎉 Deployment Complete!"
echo "   To start the supervisor:"
echo "   cd $TARGET_DIR/.agent/automation"
echo "   source .venv/bin/activate"
echo "   python supervisor_cli.py start --json"
