# Sprint 1.3: Intelligence Verification ("The Stitch")

**Objective**:
Verify the "Stitch" between Python (LangChain) and the LLM (Ollama). Measure latency and throughput to ensure the system is usable for development.

**Role**: QA / Integration Specialist
**Pre-requisites**: Sprint 1.1, Sprint 1.2
**Status**: COMPLETE

## 1. Scope of Work
### A. Connection Logic
- [ ] **Create `src/core/llm.py`**: A factory function to get the standard ChatOllama instance.
    -   Defaults to `qwen2.5-coder:7b` for logic.
    -   Configures correct temperature (0 for code).

### B. Validation Script
- [ ] **Create `scripts/verify_stitch.py`**:
    -   Import `src.core.llm`.
    -   Send a standardized prompt: *"Write a Python function to calculate Fibonacci numbers."*
    -   **Measure**: Time to First Token (TTFT) and Tokens Per Second (TPS).

### C. ChromaDB Test
- [ ] **Create `scripts/verify_rag.py`**:
    -   Embed a simple string "The sky is blue".
    -   Query "What color is the sky?".
    -   Prove that `nomic-embed-text` is working via LangChain.

## 2. Compliance Gates
- **Latency Threshold**: TTFT < 500ms (for local feel).
- **Throughput Threshold**: > 20 tokens/sec (on i5 CPU).
- **Error Handling**: Script must fail gracefully if Ollama is down.

## 3. Deliverables
- `src/core/llm.py`
- `scripts/verify_stitch.py`
- `scripts/verify_rag.py`
