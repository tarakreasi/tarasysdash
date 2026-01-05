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
## Sprint 5: Backend Extended Metadata (Completed)

**Status:** COMPLETED
**Duration:** 2026-01-01

### Objectives
Extend backend infrastructure to support production dashboard requirements.

### Deliverables
1. **Database Schema Extensions**
   - Added `rack_location TEXT` column to agents table
   - Added `temperature REAL` column to agents table
   - Migration script handles duplicate column errors gracefully

2. **New API Endpoints**
   - `PUT /api/v1/agents/:id/metadata` - Update agent rack location and temperature
   - Enhanced `GET /api/v1/agents` to return rack_location, temperature, and computed status

3. **Status Computation Logic**
   - Agents marked "offline" if not updated in last 30 seconds
   - Agents marked "online" otherwise
   - Status computed dynamically in ListAgents method

4. **Storage Layer Updates**
   - `UpdateAgentMetadata(ctx, agentID, rack, temp)` method
   - Updated `ListAgents` to include new fields and status

### Technical Notes
- Status logic: `time.Since(agent.UpdatedAt) > 30*time.Second`
- Temperature collection in agent deferred to future sprint
- All migrations backward compatible

---

## Sprint 6: Production Dashboard UI (Completed)

**Status:** COMPLETED
**Duration:** 2026-01-01

### Objectives
Implement production-ready frontend with color-coded status, rack information, and temperature display.

### Deliverables
1. **Color-Coded Status Badges**
   - Green (#4caf50) for online agents
   - Red (#ff6b6b) for offline agents
   - Smooth color transitions with CSS

2. **Extended Metadata Display**
   - Rack location below hostname
   - Temperature with degree symbol (°C)
   - Status indicator with animation

3. **TypeScript Safety**
   - Added optional chaining for null safety
   - Fixed type compatibility issues
   - Added CSS vendor prefixes for compatibility

4. **Real-time Updates**
   - Agent data refreshes every 5 seconds
   - Metrics refresh every 3 seconds
   - Status updates automatically

### UI Components Updated
- `web/src/App.vue` - Main dashboard component
- Agent interface extended with rack_location, temperature, status
- Helper functions: `getStatusColor()`, `getStatusClass()`

### Verification
- Dashboard displays rack location: "Rack A1"
- Temperature shown: "24.5°C"
- Offline agents show red badge
- Online agents show green badge
- All real-time updates working

---

## Sprint 7: Dashboard Visual Polish (Planned)

**Status:** PENDING
**Priority:** Medium

### Objectives
Add visual enhancements from mockup design to match professional appearance.

### Planned Features
1. **Animated SVG Logo**
   - Pulsing animation for brand identity
   - Cyan color (#43e9ff) with glow effect

2. **Enhanced Navigation Bar**
   - Full-width top navigation
   - Navigation links (Overview, Metrics, Alerts, Settings)
   - Responsive design for mobile

3. **Server List Enhancements**
   - Multiple server display capability
   - Total capacity progress bar
   - Scrollable list with custom scrollbar

4. **Material Symbols Integration**
   - Replace emoji icons with Google Material Symbols
   - Consistent iconography across dashboard
   - Better visual hierarchy

5. **Cyberpunk Effects**
   - Scanline overlay effect
   - Glow effects on interactive elements
   - Enhanced glassmorphism

### Technical Requirements
- Install Material Symbols font
- Create reusable icon components
- Add CSS animations for scanline
- Implement capacity calculation logic

---

## Sprint 8: Alert System (Pending)

**Status:** NOT STARTED
**Priority:** High (Production Critical)

### Objectives
Implement threshold-based alerting system for proactive monitoring.

### Planned Features
1. **Alert Configuration UI**
   - Create alert rules (CPU > 80%, Memory > 90%, etc.)
   - Enable/disable alerts per agent
   - Alert duration settings

2. **Backend Alert Engine**
   - Database table: `alerts` and `alert_history`
   - Alert evaluation on metric ingestion
   - Alert state management (triggered/resolved)

3. **Notification Channels**
   - Email notifications
   - Webhook support for Slack/Discord
   - In-app notification center

4. **Alert Dashboard**
   - Active alerts view
   - Alert history
   - Alert analytics

### Technical Architecture
- Alert rules stored in SQLite
- Evaluation happens in SaveMetric handler
- Notification service runs as goroutine
- Alert states prevent spam

---

## Technology Stack Summary

### Backend
- **Language:** Go 1.21+
- **Framework:** Gin (HTTP server)
- **Database:** SQLite (modernc.org/sqlite - pure Go)
- **Auth:** Bearer Token (SHA-256 hashed)

### Frontend
- **Framework:** Vue 3 + TypeScript
- **Build Tool:** Vite
- **Charts:** Apache ECharts
- **HTTP Client:** Axios
- **Styling:** Custom CSS (Zen Glass theme)

### Infrastructure
- **Monitoring:** tara-agent (Go binary)
- **Collection Interval:** 1 second (configurable)
- **Metrics:** CPU, Memory, Disk, Temperature (planned)

---

## Current Status (2026-01-01)

### Completed Sprints
- ✅ Sprint 1: Foundation & Core Agent
- ✅ Sprint 2: Ingestion Engine & Storage
- ✅ Sprint 3: Authentication & Security
- ✅ Sprint 4: Frontend Dashboard (Vue 3)
- ✅ Sprint 5: Backend Extended Metadata
- ✅ Sprint 6: Production Dashboard UI

### In Progress
- 🔄 Sprint 7: Dashboard Visual Polish

### Planned
- ⏳ Sprint 8: Alert System
- ⏳ Sprint 9: Historical Data & Analytics
- ⏳ Sprint 10: Multi-tenant Support

### Production Readiness
**Current State:** 80% Production-Ready

**Ready:**
- ✅ Secure ingestion (Bearer tokens)
- ✅ Real-time monitoring
- ✅ Persistent storage
- ✅ Professional UI

**Pending:**
- ⏳ Alert system
- ⏳ User authentication
- ⏳ Backup/restore
- ⏳ High availability

