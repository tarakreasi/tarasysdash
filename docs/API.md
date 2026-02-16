# API Documentation

taraSysDash REST API Reference

## Base URL

```
http://localhost:8080/api/v1
```

## Authentication

Protected endpoints require an `Authorization` header with agent token:

```
Authorization: Bearer <AGENT_TOKEN>
```

---

## Agents

### List All Agents

```http
GET /api/v1/agents
```

**Response:**
```json
[
  {
    "id": "agent-uuid-1",
    "hostname": "srv-us-e-01",
    "ip_address": "192.168.1.10",
    "os": "linux",
    "rack_location": "Rack A1",
    "temperature": 45.0,
    "status": "online",
    "created_at": "2026-01-01T09:00:00Z",
    "updated_at": "2026-01-01T10:25:00Z"
  }
]
```

**Status Computation:**
- `online` - Last update within 30 seconds
- `offline` - Last update older than 30 seconds

---

### Filter Agents by Rack

```http
GET /api/v1/agents/rack/:rack_id
```

**Parameters:**
- `rack_id` (path) - Rack location identifier (e.g., "Rack A1")

**Example:**
```bash
curl http://localhost:8080/api/v1/agents/rack/Rack%20A1
```

**Response:**
```json
[
  {
    "id": "agent-uuid-1",
    "hostname": "srv-us-e-01",
    "rack_location": "Rack A1",
    "temperature": 45.0,
    "status": "online"
  },
  {
    "id": "agent-uuid-2",
    "hostname": "srv-us-e-02",
    "rack_location": "Rack A1",
    "temperature": 42.0,
    "status": "online"
  }
]
```

---

### Update Agent Metadata

```http
PUT /api/v1/agents/:id/metadata
```

**Parameters:**
- `id` (path) - Agent ID

**Request Body:**
```json
{
  "rack_location": "Rack A1",
  "temperature": 45.5
}
```

**Response:**
```json
{
  "status": "updated"
}
```

**Example:**
```bash
curl -X PUT http://localhost:8080/api/v1/agents/agent-uuid-1/metadata \
  -H "Content-Type: application/json" \
  -d '{"rack_location":"Rack A1","temperature":45.5}'
```

---

## Metrics

### Submit Metrics (Protected)

```http
POST /api/v1/metrics
```

**Request Body:**
```json
{
  "timestamp": 1735714800,
  "cpu_usage_percent": 45.2,
  "memory_used_bytes": 13298769920,
  "memory_total_bytes": 16777216000,
  "disk_usage": [
    { "mount_point": "/", "used_bytes": 70000000000, "total_bytes": 100000000000 },
    { "mount_point": "/data", "used_bytes": 250000000000, "total_bytes": 500000000000 }
  ],
  "bytes_in": 450000000,
  "bytes_out": 120000000,
  "uptime_seconds": 3600,
  "process_count": 245,
  "temperature": 48.0,
  "services": [
    { "name": "recording-svc", "running": true }
  ]
}
```

---

### Get Metrics History

```http
GET /api/v1/metrics/:agent_id
```

**Parameters:**
- `agent_id` (path) - Agent identifier (e.g., `agent-482ae3b630b3`)
- `limit` (query, optional) - Records to return (default: 60)

---

### Get Global History (Aggregated)

```http
GET /api/v1/metrics/global/history
```

**Purpose:** Get averaged cluster-wide CPU and Memory trends.

**Response Body:**
```json
[
  {
    "timestamp": 1735714800,
    "avg_cpu": 24.5,
    "avg_memory": 45032014848
  }
]
```

---

### Get Network Metrics with Mbps

```http
GET /api/v1/metrics/:agent_id/network
```

**Parameters:**
- `agent_id` (path) - Agent ID
- `limit` (query, optional) - Number of records (default: 60)

**Response:**
```json
[
  {
    "timestamp": 1735714800,
    "bytes_in": 450000000,
    "bytes_out": 120000000,
    "mbps_in": 3.6,
    "mbps_out": 0.96,
    "latency_ms": 0.05
  }
]
```

**Mbps Calculation:**
```
mbps = (bytes_diff * 8) / (time_diff_seconds * 1000000)
```

---

## Statistics

### Network Statistics

```http
GET /api/v1/stats/:agent_id/network
```

**Parameters:**
- `agent_id` (path) - Agent ID
- `limit` (query, optional) - Sample size (default: 60)

**Response:**
```json
{
  "total_bytes_in": 450000000,
  "total_bytes_out": 120000000,
  "avg_mbps_in": 3.6,
  "avg_mbps_out": 0.96,
  "peak_mbps_in": 12.5,
  "peak_mbps_out": 4.2
}
```

**Example:**
```bash
curl http://localhost:8080/api/v1/stats/agent-uuid-1/network
```

---

### Latency Statistics

```http
GET /api/v1/stats/:agent_id/latency
```

**Parameters:**
- `agent_id` (path) - Agent ID
- `limit` (query, optional) - Sample size (default: 60)

**Response:**
```json
{
  "avg_latency_ms": 0.05,
  "min_latency_ms": 0.02,
  "max_latency_ms": 0.12,
  "p95_latency_ms": 0.08,
  "history": [0.05, 0.04, 0.06, ...]
}
```

**P95 Calculation:**
- Sort latency values ascending
- Take value at 95th percentile index

**Example:**
```bash
curl http://localhost:8080/api/v1/stats/agent-uuid-1/latency | jq
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request body"
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized"
}
```

### 404 Not Found
```json
{
  "error": "Agent not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Failed to get metrics"
}
```

---

## Rate Limiting

Currently no rate limiting implemented. Recommended for production:
- 100 requests per minute per agent
- 1000 requests per minute per IP

---

## Versioning

API version is included in the base URL: `/api/v1`

Future versions will be released as `/api/v2`, etc.

---

## CORS

CORS is disabled by default. For production with separate frontend:

```go
r.Use(cors.New(cors.Config{
  AllowOrigins: []string{"https://dashboard.example.com"},
  AllowMethods: []string{"GET", "POST", "PUT"},
  AllowHeaders: []string{"Authorization", "Content-Type"},
}))
```

---

## Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1735714800
}
```

*(Note: Health check endpoint to be implemented)*

---

## Metrics Retention

Default: No automatic cleanup

Recommended production setup:
```sql
-- Delete metrics older than 30 days
DELETE FROM system_metrics WHERE time < datetime('now', '-30 days');
```

Add to cron for daily execution.
