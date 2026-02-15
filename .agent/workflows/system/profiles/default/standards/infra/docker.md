# Docker Infrastructure Standards

## Core Principles
- **Local-First**: The environment must run entirely offline/local via `docker-compose`.
- **Isolation**: Each logical service must run in its own container.
- **Networking**: All services communicate via the `rembes-network` bridge.

## Services & Naming
| Service Role | Container Name | Image Name | Port (Host:Internal) |
| :--- | :--- | :--- | :--- |
| **App** | `rembes-app` | `rembes-app` (Local Build) | N/A (Internal 9000) |
| **Web** | `rembes-web` | `nginx:alpine` | `8000:80` |
| **Database** | `rembes-db` | `postgres:15-alpine` | `5433:5432` |
| **Cache/Queue** | `rembes-redis` | `redis:alpine` | `6380:6379` |
| **Storage** | `rembes-minio` | `minio/minio` | `9000-9001:9000-9001` |
| **Mail** | `rembes-mailpit` | `axllent/mailpit` | `8025:8025`, `1025:1025` |

## Volume Management
- **Persistence**: Database and MinIO data must be persisted via named volumes (`pgdata`, `miniodata`).
- **Development**: Source code is mounted via bind mount (`./:/var/www/html`) for live editing.

## Health Checks
- Services must expose health status where possible.
- **Mailpit**: Uses internal healthcheck.
- **App**: PHP-FPM status page (optional).
