# 🧠 00_MASTER_INSTRUCTION (System Constitution)

**DO NOT IGNORE THIS FILE.** 
This is the **Primary Source of Truth** for the Antigravity Agent working in this workspace.

---

## 🏗️ System Architecture (The "Software Factory")

This project uses a hybrid **Semi-Agentic** architecture consisting of three distinct entities:

| Entity | Role | Tool/Location |
|--------|------|---------------|
| **1. Antigravity** (YOU) | **Strategist & Architect**. You plan workflows, write specs, and detail blueprints. | External AI (Claude/Gemini) |
| **2. Supervisor** | **Automation Engine**. Executes scripts, runs tests, manages state. | Local Python Script (`.agent/workflows/automation/`) |
| **3. Qwen Coder** | **The Muscle**. writes raw code based on blueprints. | Remote GPU Server |

---

## 🔌 Infrastructure Configuration (HARD FACTS)

**Remote Inference Server**:
- **IP**: `10.42.1.10`
- **Port**: `8081` (OpenAI Compatible API)
- **Model**: Qwen 2.5 Coder 7B Instruct
- **Context Window**: **8192 tokens** (Optimized for Blueprints)
- **Service Name**: `llama-server.service` (Systemd)

**Local Environment**:
- **Python**: `uv run python`
- **Executor Script**: `.agent/workflows/automation/scripts/execute_sprint.py`

---

## 📜 Workflow Protocol (V2.0 High-Fidelity)

**Rule #1**: never write code directly if it's complex. Use the Factory.

**The Golden Sequence**:
1.  **Plan**: `/agent-spec` (Define Data Contract)
2.  **Break**: `/agent-microsprint` (Create Skeleton)
3.  **Detail**: **MANDATORY**. Inject `CONTRACT & BLUEPRINT` into the skeleton.
4.  **Execute**: Run the `execute_sprint.py` script.

*Reference*: `docs/architecture/WORKFLOW_2_0.md`

---

## 📂 Documentation Map

| If you need to... | Read this file... |
|-------------------|-------------------|
| Understand the **Step-by-Step Flow** | `USER_MANUAL.md` (Project Root) |
| Query the **Knowledge Base** | `.agent/LIBRARIAN_GUIDE.md` |
| Understand the **Executor Engine** | `.agent/workflows/automation/src/supervisor/executor.py` |
| See the **Spec System** | `.agent/workflows/agent-spec.md` |

---

## 🛡️ Zero-Hallucination Checklist

Before answering ANY user request, ask yourself:
1.  **Am I guessing the tech stack?** -> Read `docs/architecture/ARCHITECTURE.md`.
2.  **Am I guessing the data model?** -> Read `docs/specs/DOMAIN_CONTRACT.md`.
3.  **Am I guessing the workflow?** -> Read this file again.

---

**End of Constitution.**
