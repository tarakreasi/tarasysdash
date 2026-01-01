Sprint 1: The Foundation & The Agent
Objective: Membangun struktur project monorepo/polyrepo yang solid dan membuat tara-agent yang mampu mengoleksi data sistem secara efisien.

Tech Specs:

Language: Go
Library: gopsutil (untuk sys stats), viper (config).
Architecture: Hexagonal/Clean Architecture (walaupun ini cuma agent, biasakan memisah logic pengumpulan data dengan logic pengiriman data).
Tasks:

Setup Project Structure: Implementasi Standard Go Project Layout.
/cmd, /internal, /pkg.
Core Collector Logic:
Buat interface Collector untuk abstract data gathering.
Implementasi fungsi untuk ambil CPU usage, Memory stats, dan Disk I/O.
Concurrency Implementation:
Gunakan Goroutines dan time.Ticker untuk mengumpulkan data setiap X detik tanpa memblokir main thread.
Quality Gate (Must Have):
Unit Test coverage minimal 70% untuk package collector.
Linter: golangci-lint (strict mode).
Sprint 2: The Ingestion Engine (Backend Core)
Objective: Membuat backend yang mampu menerima "serbuan" data dari agent dan menyimpannya dengan efisien.

Tech Specs:

Language: Go (Echo/Fiber)
DB: PostgreSQL + GORM/Sqlc (pilih Sqlc untuk type-safe SQL).
Pattern: Repository Pattern.
Tasks:

Database Design:
Desain skema hosts, metrics, dan logs di PostgreSQL.
Setup Database Migration (menggunakan golang-migrate).
API Ingestion Endpoint:
Buat endpoint POST /api/v1/metrics yang menerima JSON payload dari Agent.
Implementasi DTO Validation (pastikan data yang masuk valid).
Service Layer:
Business logic untuk memproses data mentah sebelum masuk DB.
Quality Gate:
Implementasi Dependency Injection (biar mudah di-mock saat testing).
Integration Test: Pastikan data yang dikirim ke API benar-benar masuk ke DB.
Sprint 3: Real-time Layer & Caching
Objective: Mengubah sistem dari "request-response" menjadi "live monitoring" menggunakan Redis dan WebSockets.

Tech Specs:

Infra: Redis.
Protocol: WebSocket (Gorilla/Melody).
Tasks:

Redis Integration:
Saat data masuk ke API Ingestor, simpan snapshot terakhir ke Redis (Key: host:{id}:latest).
Set TTL (Time to Live) agar Redis tidak penuh sampah.
WebSocket Hub:
Buat WebSocket handler di Backend.
Implementasi pattern Pub/Sub: Saat data baru masuk Redis -> Publish ke Channel -> WebSocket mengirim ke Client yang subscribe.
Concurrency Safety:
Pastikan penggunaan Mutex atau Channels yang tepat untuk mencegah Race Condition saat banyak koneksi WebSocket terbuka.
Quality Gate:
Load Testing sederhana (gunakan k6) untuk memastikan WebSocket tidak crash saat ada 100+ koneksi simulasi.
Sprint 4: Frontend Architecture (Vue 3 + TS)
Objective: Visualisasi data dengan kode Frontend yang Type-Safe dan modular.

Tech Specs:

Framework: Vue 3 (Composition API), TypeScript, Vite.
State: Pinia.
Styling: Tailwind CSS.
Tasks:

Component Design:
Buat komponen Atomic: BaseCard, StatusBadge, MetricGuage.
State Management (Pinia):
Store useHostStore untuk menyimpan list server.
Store useSocketStore untuk mengelola koneksi WebSocket global.
Chart Implementation:
Integrasi Apache ECharts / Chart.js.
Pastikan chart di-update reaktif tanpa me-render ulang seluruh komponen (Performance optimization).
Quality Gate:
Strict Typing: Tidak ada any di TypeScript.
Eslint + Prettier config.
Sprint 5: Alerting System & Background Workers
Objective: Menambahkan "otak" pada sistem untuk mendeteksi anomali.

Tech Specs:

Concurrency: Go Worker Pools / Task Queue (Asynq/Machinery).
External: Telegram Bot API / SMTP.
Tasks:

Alert Logic:
User bisa set rule: IF CPU > 90% FOR 5 Minutes.
Background Worker:
Buat proses terpisah (Goroutine/Worker) yang membaca metric dari Redis/DB dan mencocokkan dengan Rule Alert.
Notification Dispatcher:
Service untuk mengirim pesan ke Telegram/Email.
Implementasi Rate Limiting (jangan spam notifikasi setiap detik, beri jeda/cooldown).
Quality Gate:
Unit test untuk logic alert (Mock skenario CPU tinggi).
Sprint 6: DevOps, Hardening & Showcase
Objective: Membuat project ini siap dipamerkan dan mudah di-deploy orang lain.

Tech Specs:

Infra: Docker, Docker Compose, GitHub Actions.
Tasks:

Containerization:
Buat Dockerfile untuk Backend (Multi-stage build agar image kecil < 20MB).
Buat Dockerfile untuk Frontend (Build static files -> Serve with Nginx/Caddy).
Orchestration:
docker-compose.yml yang menjalankan: App, DB, Redis, dan Migration script otomatis.
Documentation (PENTING):
README.md: Cara install, Architecture Diagram, Tech Stack explanation.
Swagger/OpenAPI documentation untuk backend.
CI/CD Pipeline:
GitHub Actions: Run Test & Lint setiap kali push code.
