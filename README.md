# taraSysDash

![Go Version](https://img.shields.io/badge/go-%3E%3D1.21-00ADD8?style=flat&logo=go)
![Vue Version](https://img.shields.io/badge/vue-3.x-4FC08D?style=flat&logo=vue.js)
![Docker](https://img.shields.io/badge/docker-ready-2496ED?style=flat&logo=docker)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**taraSysDash** is a lightweight, distributed system monitoring solution designed for high performance and real-time observability. Built to bridge the gap between simple server stats and enterprise-grade APM tools.

> **Status:** Active Development (Sprint 1 - Foundation Phase)

---

## 🏛 Architecture Overview

taraSysDash follows a **decoupled architecture** to ensure minimal footprint on target servers while maintaining high-throughput data processing on the backend.

```mermaid
graph LR
    A[tara-agent] -->|JSON Stream| B(Ingestor Service)
    A2[tara-agent] -->|JSON Stream| B
    B -->|Hot Data| C[(Redis)]
    B -->|Persist| D[(PostgreSQL)]
    C -->|Pub/Sub| E[WebSocket Hub]
    E -->|Real-time| F[Vue 3 Dashboard]
The Ecosystem
tara-agent (The Spy): A standalone, cross-compiled Go binary (Linux/Windows) that sits on the target server. It collects CPU, Memory, Disk, and Network stats using OS-level system calls with minimal resource usage.
tara-core (The Brain): A microservice backend that ingests data streams, handles alerting logic via background workers, and exposes REST APIs.
tara-web (The View): A modern Vue 3 + TypeScript dashboard utilizing WebSockets for live, non-blocking data visualization.
🛠 Tech Stack
Designed for concurrency and scalability.

Component	Technology	Reasoning
Backend	Go (Golang)	Chosen for its goroutines (concurrency) and efficient compilation. Ideal for handling thousands of agent streams.
Frontend	Vue 3 + TypeScript	Composition API for modular logic; TypeScript for type safety across the board.
Real-time	Redis + WebSockets	Redis Pub/Sub ensures low-latency data delivery to the frontend.
Storage	PostgreSQL	Relational integrity for user management, historical metric data, and audit logs.
Infra	Docker & GitHub Actions	Fully containerized environment with automated CI/CD pipelines.
✨ Key Features (Planned)
Live Monitoring: Sub-second latency updates for CPU, RAM, and Disk I/O.
Service Health Check: Integrated HTTP/TCP probers to monitor uptime of internal services (e.g., Nginx, DBs).
Smart Alerting: Configurable threshold alerts sent via Telegram/Email (e.g., CPU > 90% for 5 mins).
Log Aggregation: (Beta) Live tail preview of critical server logs.
Secure: Agent-Server authentication via secret tokens.
🚀 Getting Started (Dev)
Prerequisites
Go 1.21+
Node.js 18+
Docker & Docker Compose
Installation
Clone the repository

git clone https://github.com/yourusername/taraSysDash.git
cd taraSysDash
Start Infrastructure (DB & Redis)

docker-compose up -d postgres redis
Run the Backend

cd backend
go mod download
go run cmd/server/main.go
Run the Frontend

cd frontend
npm install
npm run dev
🗺 Roadmap
[ ] Sprint 1: Core Agent development & System Stats Collection (Go).
[ ] Sprint 2: Backend Ingestion Engine & Database Schema Design.
[ ] Sprint 3: Real-time WebSocket Layer & Redis Integration.
[ ] Sprint 4: Frontend Dashboard (Vue 3 + ECharts).
[ ] Sprint 5: Alerting System & Telegram Integration.
[ ] Sprint 6: Dockerization & CI/CD Pipeline.
🤝 Contribution
Contributions are welcome! Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

📝 License
This project is licensed under the MIT License.


---

### Tips Tambahan:
Jika Anda ingin repo ini terlihat sangat profesional:
1.  Buat file `CONTRIBUTING.md` nanti (kosongkan dulu tidak apa-apa).
2.  Pastikan diagram Mermaid di atas ter-render (GitHub support Mermaid native).
3.  Saat Anda push code di Sprint 1, update bagian checkbox di **Roadmap** menjadi `[x]`. Ini menunjukkan progres nyata kepada siapa pun yang mengunjungi profil Anda.