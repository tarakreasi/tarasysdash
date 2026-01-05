# 🚀 Sprint 4: Frontend Dashboard & Visualization

**Goal:** Build a "Rich Aesthetic" Web Dashboard to visualize system metrics using Vue 3 and ECharts.

## 📅 Timeline & Scope
- **Focus:** User Experience & Visuals.
- **Deliverables:**
    - **Backend:** New READ endpoints for Agents and Metrics.
    - **Frontend:** Vue 3 + Vite + TypeScript application.
    - **UI:** Custom "Zen Glass" dark theme (Vanilla CSS).
    - **Charts:** Real-time CPU, Memory, and Disk visualization using ECharts.

## 🛠 Technical Specification

### 1. Backend Updates (`cmd/server`)
The current server only *ingests* data. We need APIs to *serve* it.

#### A. New Endpoints
- `GET /api/v1/agents`: List all registered agents.
- `GET /api/v1/metrics/:agent_id`: Get recent metrics for specific agent.
    - Query Params: `?limit=60` (last 60 seconds/minutes).

#### B. CORS Support
- Enable CORS to allow the Vue app (port 5173) to talk to the Go server (port 8080).

### 2. Frontend Architecture (`web/`)

#### A. Setup
- **Framework:** Vue 3 (Composition API) + TypeScript.
- **Build Tool:** Vite.
- **Styling:** Vanilla CSS (CSS Variables for theming).
    - **Theme:** "Zen Glass" (Deep dark backgrounds, blur effects, neon accents).

#### B. Key Components
1.  **DashboardLayout:** Sidebar navigation, glassmorphism header.
2.  **AgentList:** Grid view of active agents with status indicators (Online/Offline).
3.  **MetricsPanel:** Detailed view for a selected agent.
    - **Charts:** ECharts instances for CPU/Mem/Disk.
    - **Auto-refresh:** Poll API every 2-5 seconds.

### 3. Directory Structure
```
taraSysDash/
├── cmd/
├── web/              # [NEW] Frontend Root
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── assets/
│   │   ├── App.vue
│   │   └── main.ts
│   └── package.json
```

## ✅ Definition of Done (DoD)
1.  [ ] Backend provides `GET` APIs for agents and metrics.
2.  [ ] Vue 3 project initialized in `web/`.
3.  [ ] "Zen Glass" UI theme implemented (responsive & premium).
4.  [ ] Dashboard displays list of agents.
5.  [ ] Clicking an agent shows real-time graphs (ECharts).
6.  [ ] No build errors; Linting passes.
