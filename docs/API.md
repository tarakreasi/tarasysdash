# taraSysDash API Documentation

This document describes the HTTP API exposed by the `tara-server` ingestion engine.

## Authentication

All API endpoints (except `/health`) require authentication using a **Bearer Token**.

- **Header:** `Authorization: Bearer <your_token_string>`
- **Generation:** Tokens are generated via CLI: `./bin/tara-server --gen-token --agent-id <id>`

## Endpoints

### 1. Health Check
Checks if the server is running.

- **URL:** `/health`
- **Method:** `GET`
- **Auth Required:** No
- **Response:**
  ```json
  {
    "status": "ok"
  }
  ```

### 2. Ingest Metrics
Receives system metrics from an agent.

- **URL:** `/api/v1/metrics`
- **Method:** `POST`
- **Auth Required:** Yes
- **Payload:**
  ```json
  {
    "agent_id": "agent-uuid-1",
    "timestamp": 1704073200,
    "cpu_usage_percent": 12.5,
    "memory_used_bytes": 4096000,
    "memory_total_bytes": 16777216,
    "disk_free_percent": 45.2
  }
  ```
- **Response (Success):**
  - **Code:** `200 OK`
  - **Body:** `{"status": "recorded"}`
- **Response (Error):**
  - **Code:** `401 Unauthorized` (Invalid token)
  - **Code:** `403 Forbidden` (Token valid but Agent ID mismatch)
  - **Code:** `400 Bad Request` (Invalid JSON)
