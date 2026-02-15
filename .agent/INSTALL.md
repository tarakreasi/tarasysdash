# 💿 Installation Guide

## ⚡ Quick Start (Automated)

The easiest way to install the **Semi-Agentic Toolkit** (v5.0) into your project.

### 1. Run the Deploy Script
Assuming you have the toolkit cloned in `~/tools/agent-toolkit`:

```bash
# Deploy to your target project
~/tools/agent-toolkit/scripts/deploy.sh /path/to/your/project
```

### 2. Configure the Environment
Navigate to your project to set up the Python environment for the automation engine.

```bash
cd /path/to/your/project
cd .agent/workflows/automation

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies (Supervisor, Librarian, etc.)
pip install -e .
```

### 3. Initialize the Brain (Librarian)
Index your current codebase so the agents know what exists.

```bash
# From .agent/workflows/automation directory
uv run python scripts/index_codebase.py
```

### 4. Verify Installation
Ensure the ecosystem is healthy.

```bash
python supervisor_cli.py status
# Expected: "Supervisor Status: IDLE"
```

---

## 🛠️ Manual Installation (Advanced)

If you cannot use the deploy script, follow these steps to replicate the structure.

### 1. Create Folder Taxonomy
The system relies on a standardized folder structure.

```bash
# Root of your project
mkdir -p .agent/workflows/automation
mkdir -p docs/dev/sprints
mkdir -p docs/research
mkdir -p docs/specs
mkdir -p docs/architecture
mkdir -p docs/debugging
mkdir -p docs/planning
mkdir -p docs/product
```

### 2. Copy Core Components
Use `rsync` to copy the agent brains and rules.

```bash
# Copy the .agent folder
rsync -av --exclude '__pycache__' --exclude '.venv' --exclude 'memory/*.db' \
    ~/tools/agent-toolkit/.agent/ ./.agent/
```

### 3. Install Execution Environment
Set up the Python "Body" that runs the automation.

```bash
cd .agent/workflows/automation
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## 📞 Troubleshooting

### Path Errors (`ModuleNotFoundError`)
*   **Cause**: You are running scripts from the wrong directory.
*   **Fix**: Always run automation scripts from `.agent/workflows/automation/`.

### Deployment Fails (`Permission denied`)
*   **Fix**: Make the script executable.
    ```bash
    chmod +x ~/tools/agent-toolkit/scripts/deploy.sh
    ```

### Librarian is Empty
*   **Symptom**: Agent says "I don't know the codebase."
*   **Fix**: Run the indexer again.
    ```bash
    cd .agent/workflows/automation
    uv run python scripts/index_codebase.py
    ```

---

## 🔗 Next Steps

Now that you are installed:

1.  **New Project?** -> Run `/product-planner` to define your mission.
2.  **Old Project?** -> Run `/agent-code` to audit the mess.
3.  **Just working?** -> Run `/agent-scrum-master` to start a sprint.
