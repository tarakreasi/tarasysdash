# Domain Contract: taraSysDash (Frontend Focus)

> **Status**: DRAFT (Created during Recovery)
> **Purpose**: Single Source of Truth for API Contracts, Data Models, and UI Components.

---

## 1. terminology
- **Agent**: A monitored server (physical or virtual).
- **Metric**: A specific data point (CPU, RAM, Temp) collected from an Agent.
- **Rack**: A physical grouping of Agents in the datacenter.

---

## 2. API Contract
**Base URL**: `VITE_API_BASE_URL` (Default: `http://localhost:8080/api/v1`)

### Endpoints

#### `GET /agents`
- **Description**: List all registered agents.
- **Response**: `Agent[]`

#### `GET /metrics/{agent_id}`
- **Query Params**: `limit` (number, default 10)
- **Response**: `Metric[]`

#### `PUT /agents/{agent_id}/hostname`
- **Payload**: `{ hostname: string }`
- **Response**: `Agent`

#### `PUT /agents/{agent_id}/metadata`
- **Payload**: 
  ```json
  {
    "rack_location": string,
    "temperature": number,
    "log_retention_days": number
  }
  ```
- **Response**: `Agent`

---

## 3. Data Models (TypeScript Interfaces)

```typescript
export interface Agent {
  id: string;
  hostname: string;
  ip_address: string;
  os: string;
  status: 'online' | 'offline' | 'warning';
  rack_location: string;
  temperature?: number;
  log_retention_days?: number;
  last_seen?: string;
}

export interface Metric {
  timestamp: number;
  cpu_usage_percent: number;
  memory_used_bytes: number;
  memory_total_bytes: number;
  disk_usage: DiskUsage[];
  bytes_in: number;
  bytes_out: number;
  uptime_seconds: number;
  process_count: number;
  services: ServiceStatus[];
  temperature?: number;
}

export interface DiskUsage {
  mount_point: string;
  used_bytes: number;
  total_bytes: number;
}

export interface ServiceStatus {
  name: string;
  running: boolean;
}
```

---

## 4. UI Components (Atomic)

### Core
- `ServerCard.vue`: Displays summary of an Agent.
- `EditServerModal.vue`: Form to edit Agent details.
- `ServerGauge.vue` (Planned): Extract from DashboardView.

### Views
- `DashboardView.vue`: Main cockpit.
- `AnalyticsView.vue` (Future): Historical data.
