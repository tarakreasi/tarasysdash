# User Manual: The Local AI Stack (For Geeks/Power Users)

This manual details the architecture and advanced usage of the `qwen2.5-coder` integration within the Antigravity ecosystem.

## Architecture Overview
The system follows a "Stitiched" architecture optimized for Intel i5/16GB environments:
*   **Inferencing Engine**: `Ollama` (running as a systemd service).
*   **Quantization**: `qwen2.5-coder:1.5b-q4_k_m` (Low Latency) & `qwen2.5-coder:7b-q4_k_m` (Logic).
*   **Orchestration**: `LangChain` + `LangGraph`.
*   **Interface**: `Continue` Extension (VS Code Protocol).

---

## 1. Advanced Configuration (Tuning)
You can modify `src/core/config.py` to adjust system behavior:
```python
# Adjust temperature for creativity vs precision
# 0.0 = Deterministic (Code), 0.7 = Creative (Writing)
TEMPERATURE = 0.1 
```

### Context Providers (RAG)
The system uses `nomic-embed-text` for local embeddings. To utilize RAG effectively:
1.  In Chat Panel (`Ctrl+L`), type `@Codebase`.
2.  Ask: "How does the `check_path_safety` function work?".
3.  The system will vector-search your project files and answer based on *actual* code.

### Custom Commands
You can add custom slash commands in `~/.continue/config.json`.
Example "Refactor" command:
```json
{
  "name": "refactor",
  "prompt": "Refactor this code to follow SOLID principles. Maintain current functionality.",
  "description": "Refactor Code"
}
```

---

## 2. The Autonomous CLI Agent (`src/main.py`)
Beyond the IDE, you have a CLI agent capable of file operations.

### Modes
1.  **Interact**: Just run `python src/main.py`. Loops until exit.
2.  **One-Shot**: `python src/main.py --prompt "Create a hello world flask app in ./web"`

### Tool Usage
The agent has access to `src/tools/`.
*   **Safety**: It is sandboxed to `PROJECT_ROOT`. Attempting to access `/` or `..` will raise a PermissionError.
*   **Logic**: It uses a ReAct (Reason+Act) loop via LangGraph. 
    *   If prompt is "List files", it executes `list_dir`.
    *   It feeds the output back to itself to generate the final answer.

## 3. Performance Metrics (Benchmarks)
On an Intel i5 Gen 10:
*   **1.5b Model**: ~20-30 tokens/sec. Instant for autocomplete.
*   **7b Model**: ~5-8 tokens/sec. Good for chat/logic.
*   **RAM Usage**: ~5.5GB Total (1.5b + 7b active).

## 4. Debugging
If the agent hallucinates or fails:
1.  Check **Ollama Logs**: `journalctl -u ollama -f`
2.  Run **Verification**: `uv run scripts/verify_stitch.py`

Happy Hacking. 🛠️
