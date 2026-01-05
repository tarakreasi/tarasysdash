# 🚀 Sprint 3: Authentication & Security

**Goal:** Secure the ingestion pipeline by implementing Token-Based Authentication. Only authorized agents with valid tokens can submit metrics.

## 📅 Timeline & Scope
- **Focus:** Security & Integrity
- **Deliverable:**
    - `tara-server` enforces `Authorization` header checks.
    - CLI tool to generate and hash tokens.
    - `tara-agent` sends authenticated requests.
- **Anti-goals:** No persistent user login (that's for dashboard users later), no complex OIDC.

## 🛠 Technical Specification

### 1. Security Architecture (Bearer Token)
We will use a **Bearer Token** scheme.
- **Transmisson:** `Authorization: Bearer <token_string>`
- **Storage:** Database stores a **SHA-256 Hash** of the token, ensuring that even if the DB is leaked, the original tokens are safe.
- **Algorithm:** `token_hash = sha256(token_string)`

### 2. Database Schema Changes (SQLite)
We need to modify the `agents` table. Since SQLite has limited `ALTER TABLE` support, we will add a column.

```sql
ALTER TABLE agents ADD COLUMN token_hash TEXT;
```

### 3. Backend Implementation (`cmd/server`)

#### A. Token Generation (CLI)
We will add a CLI mode to `tara-server` to generate tokens securely.
```bash
./bin/tara-server token --agent-id <uuid>
# Output:
# Token: tara_ag_12345... (Keep this safe!)
```

#### B. Middleware (`internal/auth`)
- **Middleware:** `AuthMiddleware(store)`
- Logic:
    1. Extract header `Authorization: Bearer <t>`.
    2. Compute `h = sha256(t)`.
    3. Query DB: `SELECT id FROM agents WHERE token_hash = h`.
    4. If found, inject `AgentID` into context.
    5. If not, return `401 Unauthorized`.

### 4. Agent Update (`cmd/agent`)
- **Config:** Add `AGENT_TOKEN` (env var).
- **HTTP Client:** Add header to validation requests.

## ✅ Definition of Done (DoD)
1.  [ ] `agents` table schema updated with `token_hash`.
2.  [ ] Server accepts `--mode=token` to generate secrets.
3.  [ ] Requests without token return `401`.
4.  [ ] Requests with invalid token return `401`.
5.  [ ] Requests with valid token return `200`.
6.  [ ] Code follows "Secure by Design" principles (no plaintext tokens in DB).
