"""
Configuration module for Agent Automation
Handles all settings with priority: .env > environment variables > defaults
"""
from typing import Literal
import os
from pathlib import Path

# Try to load python-dotenv, but don't crash if it's missing (fallback to os.environ)
try:
    from dotenv import load_dotenv
    
    # Look for .env in multiple locations with priority
    # Priority: 1. Project Root (cwd) > 2. Parent of .agent > 3. .agent/automation
    
    # Try current working directory first
    cwd_env = Path.cwd() / ".env"
    if cwd_env.exists():
        load_dotenv(cwd_env)
        print(f"✓ Loaded .env from: {cwd_env}")
    else:
        # Try to find .agent directory and go up to project root
        current = Path(__file__).resolve()
        while current.parent != current:
            if (current / ".agent").exists():
                project_env = current / ".env"
                if project_env.exists():
                    load_dotenv(project_env)
                    print(f"✓ Loaded .env from: {project_env}")
                break
            current = current.parent
        
except ImportError:
    print("⚠ python-dotenv not available, using os.environ only")

# Helper to get env with default
def get_env(key: str, default: any) -> any:
    return os.getenv(key, default)

def get_bool_env(key: str, default: bool) -> bool:
    val = os.getenv(key, str(default)).lower()
    return val in ('true', '1', 'yes', 'on')

# --- CONFIGURATION VARIABLES ---

# 1. Model Configuration
MODEL_FAST = get_env("OLLAMA_MODEL_FAST", "qwen2.5-coder:1.5b")
MODEL_SMART = get_env("OLLAMA_MODEL_SMART", "qwen2.5-coder:1.5b")
MODEL_EMBEDDING = get_env("OLLAMA_MODEL_EMBEDDING", "nomic-embed-text")

OLLAMA_BASE_URL = get_env("OLLAMA_BASE_URL", "http://localhost:11434")

# 2. System Configuration
# Hardcoded for Deterministic Agentic Toolset Mode (Sprint 4.0)
AI_ENABLED = False 
DETERMINISTIC_MODE = True

# 3. Performance / Limits
TARGET_TTFT = float(get_env("TARGET_TTFT", "0.5"))
MAX_REASONING_LOOPS = int(get_env("MAX_REASONING_LOOPS", "10"))
MAX_RETRIES = int(get_env("MAX_RETRIES", "3"))

# 4. Project Paths (Auto-detection with Override)
def detect_project_root() -> Path:
    """
    Intelligently detect the project root directory.
    Priority:
    1. PROJECT_ROOT env variable (explicit override)
    2. Look for .agent directory walking up from current file
    3. Current working directory as fallback
    
    Logic: Walk up until we find a directory that CONTAINS .agent
           (not IS .agent or inside .agent)
    """
    # Priority 1: Explicit override
    if override := get_env("PROJECT_ROOT", None):
        return Path(override).resolve()
    
    # Priority 2: Auto-detect by finding directory that CONTAINS .agent
    current = Path(__file__).resolve()
    
    # Walk up from current file location
    while current.parent != current:
        # Check if current directory contains .agent folder
        agent_path = current / ".agent"
        if agent_path.exists() and agent_path.is_dir():
            # Make sure we're not inside .agent itself
            if ".agent" not in current.parts[-2:]:
                print(f"✓ Auto-detected project root: {current}")
                return current
        current = current.parent
    
    # Priority 3: Fallback to CWD
    fallback = Path.cwd()
    print(f"⚠ Using CWD as project root: {fallback}")
    return fallback

PROJECT_ROOT = detect_project_root()
AGENT_DIR_NAME = get_env("AGENT_DIR_NAME", ".agent")
DOCS_DIR_NAME = get_env("DOCS_DIR_NAME", "docs")
SPRINTS_DIR_NAME = get_env("SPRINTS_DIR_NAME", "sprints")

# Computed paths
AGENT_DIR = PROJECT_ROOT / AGENT_DIR_NAME
DOCS_DIR = PROJECT_ROOT / DOCS_DIR_NAME
SPRINTS_DIR = DOCS_DIR / "dev" / SPRINTS_DIR_NAME

# Debug output
if __name__ == "__main__":
    print("\n=== Configuration Summary ===")
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"AGENT_DIR: {AGENT_DIR}")
    print(f"DOCS_DIR: {DOCS_DIR}")
    print(f"SPRINTS_DIR: {SPRINTS_DIR}")
    print(f"OLLAMA_BASE_URL: {OLLAMA_BASE_URL}")
    print(f"MODEL_SMART: {MODEL_SMART}")
    print(f"AI_ENABLED: {AI_ENABLED}")
    print(f"DETERMINISTIC_MODE: {DETERMINISTIC_MODE}")
