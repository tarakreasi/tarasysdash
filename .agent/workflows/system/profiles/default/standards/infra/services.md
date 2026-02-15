# Service Integration Standards

## 1. Storage (MinIO)
- **Driver**: `s3` (via `league/flysystem-aws-s3-v3`).
- **Addressing**:
    - **Internal** (App -> MinIO): `http://minio:9000`
    - **External** (Browser -> MinIO): `http://localhost:9000`
- **Bucket**: `rembes-bucket` (Created programmatically/manually).
- **Region**: `us-east-1` (Default Dummy).

## 2. Cache & Queue (Redis)
- **Role**: Primary driver for `CACHE_STORE`, `SESSION_DRIVER`, and `QUEUE_CONNECTION`.
- **Hostname**: `redis` (Internal).
- **Prefix**: `rembes_database_` (To allow shared redis usage if needed).

## 3. Mail (Mailpit)
- **Role**: SMTP Capture for local development.
- **SMTP**: `mailpit:1025`
- **Dashboard**: `http://localhost:8025`
- **Production**: Never use Mailpit in production.

## 4. Environment Variables (.env)
- **DB_HOST**: `db`
- **REDIS_HOST**: `redis`
- **MAIL_HOST**: `mailpit`
- **AWS_ENDPOINT**: `http://minio:9000` (Use path style `AWS_USE_PATH_STYLE_ENDPOINT=true`)
