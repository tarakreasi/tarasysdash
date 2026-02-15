# Compliance & Security Standards

**Level**: Critical
**Enforcement**: Mandatory for Pull Request / Merge

## 1. Core Principle: Default Deny & Defense in Depth
Security is not a feature; it is a constraint. We operate under the assumption that the Application Layer **WILL** have bugs, therefore the Database Layer must act as the final line of defense.

## 2. Financial Grade Protection Rules

### 2.1 Multi-Tenancy Isolation (The "Nuclear" Option)
- **Requirement**: ALL tables containing Tenant Data MUST be protected by **Postgres Row Level Security (RLS)**.
- **Why**: To prevent data leakage even if the application code attempts to query `User::withoutGlobalScope()->get()`.
- **Implementation**:
    - **Migration**: Every table creation (`create_users_table`) must be accompanied by an RLS Policy `USING (tenant_id = current_setting('app.current_tenant_id'))`.
    - **Middleware**: `SetPostgresTenantContext` must be active on all Tenant Routes.
    - **Exception**: The `User` model MUST NOT use the `BelongsToTenant` trait. Tenant context is derived *from* the User; applying it *to* the User creates an infinite recursion crash during authentication.

### 2.2 Audit Trails
- **Requirement**: Every mutation (Create, Update, Delete) and sensitive Read of Financial Data (Receipts, OCR) MUST be logged.
- **Compliance**:
    - **Who**: Actor ID (User).
    - **Where**: Tenant ID (Strict Isolation).
    - **What**: Old Values vs New Values.
    - **When**: Timestamp.
- **Tool**: `spatie/laravel-activitylog` with `tenant_id` column.

### 2.3 Data Encryption
- **At Rest**: All uploaded files (S3/MinIO) must use **Server-Side Encryption (AES256)**.
- **In Transit**: Production traffic restricted to **HTTPS (TLS 1.2+)** only.

## 3. The "Definition of Secure" Checklist
Before marking any task as "Complete", you MUST answer YES to these:
1.  [ ] **Data Sovreignty**: If I run `SELECT * FROM table` as Tenant A, is Tenant B's data invisible?
2.  [ ] **Auditability**: If I change this record, will the auditor see it?
3.  [ ] **Confidentiality**: If I dump the S3 bucket, are the files unreadable without the key?
