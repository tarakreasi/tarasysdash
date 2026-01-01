# Backend API Documentation for Dashboard UI Design

This document provides complete backend information to help you design and implement the taraSysDash frontend dashboard.

## Current Backend Capabilities

### Base URL
```
http://localhost:8080
```

---

## Available Endpoints

### 1. Health Check
**Endpoint:** `GET /health`  
**Authentication:** None  
**Purpose:** Check if server is running

**Response:**
```json
{
  "status": "ok"
}
```

---

### 2. List All Agents
**Endpoint:** `GET /api/v1/agents`  
**Authentication:** None (Public read)  
**Purpose:** Get all registered monitoring agents

**Response Structure:**
```json
[
  {
    "id": "agent-uuid-1",
    "hostname": "provisioned",
    "ip_address": "127.0.0.1",
    "os": "linux",
    "created_at": "2026-01-01T08:39:25Z",
    "updated_at": "2026-01-01T09:10:32Z"
  }
]
```

**UI Design Opportunities:**
- Agent list/grid view
- Online/offline status (based on `updated_at`)
- Filter by OS type
- Sort by hostname, last update
- Agent detail cards

---

### 3. Get  Metrics for Specific Agent
**Endpoint:** `GET /api/v1/metrics/:agent_id`  
**Authentication:** None (Public read)  
**Purpose:** Retrieve recent metrics for a specific agent

**URL Parameters:**
- `agent_id`: The agent identifier (e.g., "agent-uuid-1")

**Query Parameters (Future):**
- `limit`: Number of data points (default: 60)
- `from`: Start timestamp (not yet implemented)
- `to`: End timestamp (not yet implemented)

**Response Structure:**
```json
[
  {
    "timestamp": 1735707572,
    "cpu_usage_percent": 12.5,
    "memory_used_bytes": 4096000000,
    "memory_total_bytes": 16777216000,
    "disk_free_percent": 45.2
  },
  {
    "timestamp": 1735707573,
    "cpu_usage_percent": 13.1,
    "memory_used_bytes": 4100000000,
    "memory_total_bytes": 16777216000,
    "disk_free_percent": 45.1
  }
]
```

**Data Points Explained:**
- `timestamp`: Unix timestamp (seconds since epoch)
- `cpu_usage_percent`: 0-100 (percentage)
- `memory_used_bytes`: Bytes currently used
- `memory_total_bytes`: Total system memory
- `disk_free_percent`: 0-100 (percentage of free space)

**UI Design Opportunities:**
- **Time Series Charts:** Line/area charts for CPU, Memory, Disk trends
- **Gauge Widgets:** Circular/linear gauges for current usage
- **Alert Indicators:** Highlight when metrics exceed thresholds (e.g., CPU > 80%)
- **Sparklines:** Miniature charts in agent cards
- **Heatmaps:** Show patterns over time
- **Comparison View:** Side-by-side agent metrics

---

### 4. Ingest Metrics (POST)
**Endpoint:** `POST /api/v1/metrics`  
**Authentication:** Required (Bearer Token)  
**Purpose:** Agent sends metrics to server

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "agent_id": "agent-uuid-1",
  "timestamp": 1735707572,
  "cpu_usage_percent": 12.5,
  "memory_used_bytes": 4096000000,
  "memory_total_bytes": 16777216000,
  "disk_free_percent": 45.2
}
```

**UI Design Note:** This endpoint is for agents only. Dashboard should not call this.

---

## Data Refresh Strategy

### Current Implementation
- **Agent Data:** Refresh every 5 seconds
- **Metrics Data:** Refresh every 3 seconds
- **Default History:** Last 60 data points

### Recommendations
- Use WebSocket for real-time updates (future enhancement)
- Implement auto-pause when dashboard not visible (`document.hidden`)
- Show "Last Updated" timestamp
- Add manual refresh button

---

## Calculated Metrics for UI

The backend provides raw data. Frontend should calculate:

### Memory Usage Percentage
```javascript
const memoryPercent = (memory_used_bytes / memory_total_bytes) * 100
```

### Disk Used Percentage
```javascript
const diskUsedPercent = 100 - disk_free_percent
```

### Bytes Formatting
```javascript
function formatBytes(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB'
  if (bytes < 1073741824) return (bytes / 1048576).toFixed(1) + ' MB'
  return (bytes / 1073741824).toFixed(2) + ' GB'
}
```

### Agent Status
```javascript
function getAgentStatus(updated_at) {
  const now = new Date()
  const lastUpdate = new Date(updated_at)
  const diffSeconds = (now - lastUpdate) / 1000
  
  if (diffSeconds < 10) return 'online'
  if (diffSeconds < 60) return 'warning'
  return 'offline'
}
```

---

## Suggested Dashboard Layout

### 1. Header Bar
- Logo and title
- Global stats (total agents, online agents)
- User menu (future)
- Refresh controls

### 2. Sidebar
- Agent list with status indicators
- Quick stats per agent
- Filter/search agents

### 3. Main Panel

#### **Option A: Overview Dashboard**
- Grid of metric cards (CPU, Memory, Disk)
- Charts showing trends
- System health score

#### **Option B: Detailed Agent View**
- Large charts (time series)
- Detailed metrics table
- Historical data analysis
- Export/download options

#### **Option C: Multi-Agent Comparison**
- Side-by-side charts
- Performance ranking
- Anomaly detection

---

## Chart Recommendations

### CPU Usage Chart
- **Type:** Line/Area chart
- **Color:** Cyan (#43e9ff)
- **Threshold:** Warning at 70%, Critical at 90%
- **Y-Axis:** 0-100%

### Memory Usage Chart
- **Type:** Line/Area chart
- **Color:** Red (#ff6b6b)
- **Show:** Both percentage and absolute values
- **Y-Axis:** 0-100%

### Disk Free Chart
- **Type:** Line/Area chart
- **Color:** Green (#4caf50)
- **Invert:** Consider showing "Disk Used" for clarity
- **Y-Axis:** 0-100%

---

## Design System References

### Current Theme: "Zen Glass"
- **Background:** Dark gradient (`#0a0e27` → `#1a1f3a`)
- **Glass Effect:** `backdrop-filter: blur(15px)`
- **Borders:** Subtle cyan glow (`rgba(67, 233, 255, 0.2)`)
- **Typography:** Inter font family
- **Contrast:** Light text on dark backgrounds

### Color Palette
- **Primary:** `#43e9ff` (Cyan)
- **Success:** `#4caf50` (Green)
- **Warning:** `#ffa726` (Orange)
- **Danger:** `#ff6b6b` (Red)
- **Neutral:** `#888` (Gray)

---

## Future Enhancements (Not Yet Implemented)

These features are planned but not available yet:

- **Alerts/Notifications:** Threshold-based alerts
- **WebSocket Streaming:** Real-time push updates
- **Historical Data:** Query by date range
- **Aggregations:** Min/max/avg calculations
- **User Authentication:** Dashboard login
- **Agent Grouping:** Organize by environment/role
- **Custom Metrics:** Beyond CPU/Memory/Disk

---

## Testing the Backend

### Quick Test Commands

```bash
# List all agents
curl http://localhost:8080/api/v1/agents

# Get metrics for specific agent
curl http://localhost:8080/api/v1/metrics/agent-uuid-1

# Health check
curl http://localhost:8080/health
```

---

## Example UI Component Pseudo-code

### Agent Status Badge
```javascript
<AgentBadge>
  <StatusIndicator color={getStatusColor(agent.updated_at)} />
  <AgentName>{agent.hostname}</AgentName>
  <LastSeen>{formatTimeAgo(agent.updated_at)}</LastSeen>
</AgentBadge>
```

### Metric Widget
```javascript
<MetricWidget>
  <Icon>⚡</Icon>
  <Label>CPU Usage</Label>
  <Value>{latestMetric.cpu_usage_percent}%</Value>
  <Chart type="sparkline" data={cpuHistory} />
</MetricWidget>
```

---

## Performance Considerations

- **Data Volume:** 60 data points × 3 metrics = ~180 numbers per agent
- **Update Frequency:** Every 3 seconds = 20 updates/minute
- **Multiple Agents:** Scale linearly (10 agents = 1800 numbers in memory)
- **Recommendation:** Limit history to last 5-10 minutes for performance

---

## CORS Configuration

The backend is configured to allow all origins (`*`) for development:
- **Allowed Origins:** `*`
- **Allowed Methods:** `GET, POST, OPTIONS`
- **Allowed Headers:** `Content-Type, Authorization`

**Production Note:** Restrict CORS to specific frontend domain.
