# Sprint 1.2: Model Provisioning

**Objective**:
Automate the acquisition and configuration of the "Intelligence Engine" (Ollama Models). Ensure the correct quantized models (GGUF) are present for the hardware constraints (16GB RAM).

**Role**: AI Systems Engineer
**Pre-requisites**: basic terminal access
**Status**: IN PROGRESS (Downloading)

## 1. Scope of Work
### A. Model Selection (The "Hardware Algebra")
- [ ] **Coding Model (Fast)**: `qwen2.5-coder:1.5b` (For tab-autocomplete).
- [ ] **Coding Model (Smart)**: `qwen2.5-coder:7b` (For chat/logic).
- [ ] **Embedding Model**: `nomic-embed-text` (For RAG/ChromaDB).

### B. Automation Scripting
- [ ] **Create `scripts/setup_models.sh`**:
    -   Check if `ollama` is installed/running.
    -   `pull` the models if missing.
    -   Verify the SHA/size to ensure it's the correct quantization level (avoid crashing RAM).

## 2. Compliance Gates
- **RAM Budget**: Total model footprint loaded in memory should not exceed 8GB (leaving 8GB for OS/App).
- **Idempotency**: Running the script twice should not re-download models.

## 3. Deliverables
- `scripts/setup_models.sh` (Executable bash script).
- A running, verified Ollama instance with listed models.
