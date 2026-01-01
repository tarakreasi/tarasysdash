# taraSysDash

![Go Version](https://img.shields.io/badge/go-%3E%3D1.21-00ADD8?style=flat&logo=go)
![Vue Version](https://img.shields.io/badge/vue-3.x-4FC08D?style=flat&logo=vue.js)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

> "Built with the logic of a technician, the stability of an integrator, and the empathy of customer service."

---

## The Story Behind the Code

Hi, I'm **Tri Wantoro**.

This repository-**taraSysDash**-is a small reflection of a long learning process; one that spans different roles, environments, and layers of technology.

### A Journey Through the Stack
My understanding of software didn't start with frameworks or libraries, but grew through different perspectives:

* **Listening to Users (Customer Service)**
  Supporting users taught me how frustrating technology can be when it doesn't behave as expected.
  → *It made me more careful about UX decisions, error handling, and communication through the interface.*

* **Learning Structure from Hardware (Electronics Technician)**
  Working with electronic components reinforced basic principles: clear inputs, predictable processes, and measurable outputs.
  → *In software, I try to apply the same discipline through modular and testable code.*

* **Respecting Production Environments (System Integrator - Ongoing)**
  Working with Linux servers and integrated systems (Milestone VMS) taught me that small mistakes can have real consequences.
  → *Because of this, I tend to be cautious about security, logging, and resource usage.*

* **Connecting Theory with Practice (Formal Education)**
  Completing an Information Systems degree (GPA 3.93) while working full-time reminded me that **textbooks and real-world constraints often need to meet halfway.**

* **Continuing to Build (Software Engineering Focus)**
  In this project, I chose **Go** for its concurrency model and **SQLite** for zero-dependency deployment.
  → *These tools let me focus on the product, not the plumbing-allowing me to write code that is easier to understand, maintain, and operate.*

---

### A Note About This Repository
**Nothing here is meant to be "perfect."**

This code represents what I currently understand, shaped by past experiences and ongoing work in real environments. If you find something that can be improved, it probably can-and I welcome that feedback.

## Project Overview

**taraSysDash** is a lightweight, distributed system monitoring solution designed to bridge the gap between simple server statistics and enterprise-grade APM tools.

I built this project to address a recurring challenge I encounter in system integration: the need for reliable, low-overhead monitoring that doesn't require complex infrastructure. Leveraging my background in hardware diagnostics and production environments, this application focuses on precision data collection and secure transmission.

### Current Features (Sprint 3)
*   **Agent-Based Collection:** Standalone Go binary (`tara-agent`) collects CPU, Memory, and Disk metrics with minimal resource footprint.
*   **Secure Ingestion:** HTTP-based ingestion engine (`tara-server`) with SHA-256 hashed Bearer Token authentication.
*   **Persistent Storage:** SQLite database for metric retention and agent registration.
*   **CLI Token Management:** Built-in token generator for agent provisioning.

---

## Tech Stack & Engineering Decisions

| Component | Tech Selection | Engineering Context (The "Why") |
|-----------|---------------|----------------------------------|
| **Agent** | **Go 1.21+** | Chosen for goroutines and efficient system calls-treating each agent stream like a sensor channel that must never block the others. |
| **Storage** | **SQLite** | Relational integrity with zero external dependencies. Like choosing solid-state over complex RAID setups for the foundation phase. |
| **Security** | **Bearer Tokens (SHA-256)** | Stateless authentication mirrors the "single source of truth" principle I use in hardware diagnostics-no session state to corrupt. |
| **Server** | **Gin (Go)** | Lightweight HTTP framework that handles concurrent connections efficiently, essential for managing multiple agent streams. |

### Technical Highlight: From Hardware to Software
**Challenge:** How to ensure agent→server communication remains secure without adding operational complexity.

**Solution (The RCA Approach):**
Applying my **Root Cause Analysis** mindset:
1.  **Isolate:** Authentication must not depend on shared session state.
2.  **Trace:** Tokens are hashed server-side; plaintext never stored (defense-in-depth).
3.  **Resolve:** CLI tool generates tokens on-demand, keeping the provisioning process deterministic.

---

## Installation & Setup

Since I am accustomed to Linux CLI environments, here is the standard setup to get this running on your local machine:

```bash
# 1. Clone the repository
git clone https://github.com/tarakreasi/taraysdash.git

# 2. Navigate to directory
cd taraSysDash

# 3. Install Go Dependencies
go mod download

# 4. Build Binaries
make build
# Or manually:
# go build -o bin/tara-server cmd/server/main.go
# go build -o bin/tara-agent cmd/agent/main.go

# 5. Generate Agent Token
./bin/tara-server --gen-token --agent-id my-agent-001
# Save the output token securely

# 6. Start Server
./bin/tara-server
# Server will run on http://localhost:8080

# 7. Start Agent (in another terminal)
export AGENT_TOKEN="your_generated_token_here"
export SERVER_URL="http://localhost:8080"
./bin/tara-agent
```

For detailed configuration options, see [docs/AGENT.md](docs/AGENT.md).

---

## Architecture

taraSysDash follows a decoupled architecture to ensure minimal footprint on target servers:

```
[tara-agent] --JSON/HTTP--> [tara-server] --SQLite--> [tara.db]
     |                            |
  Metrics                    Authentication
Collection                    Middleware
```

**Agent:** Collects system metrics every N seconds (configurable).  
**Server:** Validates tokens, persists data, exposes APIs (future).  
**Database:** Stores agent metadata and time-series metrics.

---

## Roadmap

- [x] **Sprint 1:** Core Agent development (CPU, Memory, Disk collection)
- [x] **Sprint 2:** Ingestion Engine & SQLite Storage
- [x] **Sprint 3:** Token-Based Authentication
- [ ] **Sprint 4:** Vue 3 Dashboard (Real-time visualization)
- [ ] **Sprint 5:** Alerting System (Threshold-based notifications)
- [ ] **Sprint 6:** Docker Deployment & CI/CD

---

## Retrospective: What I Learned

> "Software is just hardware that you can change instantly. But the discipline to maintain it should remain the same."

*   **Simplify First:** Choosing SQLite over PostgreSQL for the foundation phase reduced moving parts-much like using a single power supply instead of cascaded regulators.
*   **Production Mindset:** The token generator CLI ensures that security provisioning is repeatable and auditable, mirroring the SOPs I use in system integration.
*   **User-Centricity:** A monitoring tool is only useful if it remains invisible during normal operation-a lesson from my Customer Service days.

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

---

## Connect with Me

I am currently a System Integrator actively pivoting to a professional Fullstack Engineering role. I am ready to bring the reliability of a senior technician and the creativity of a developer to your team.

*   **LinkedIn:** [linkedin.com/in/twantoro](https://www.linkedin.com/in/twantoro)
*   **GitHub:** [github.com/tarakreasi](https://github.com/tarakreasi)
*   **Email:** ajarsinau@gmail.com

*"Ajarsinau" means "Learning to Learn". It represents my commitment to continuous evolution-from hardware to software, from technician to engineer.*

---

## License

This project is licensed under the MIT License.