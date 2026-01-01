# Changelog

All notable changes to `taraSysDash` will be documented in this file.

## [Unreleased] - Sprint 4 (Frontend)
- **Planned:** Vue 3 dashboard (Zen Glass theme).
- **Planned:** Server READ APIs.
- **Planned:** ECharts visualization.

## [0.3.0] - Sprint 3: Authentication - 2026-01-01
### Added
- **Security:** Token-based authentication using Bearer tokens.
- **Database:** Added `token_hash` column to `agents` table (SQLite).
- **Server:** New `--gen-token` CLI flag to generate secure agent tokens.
- **Server:** `AuthMiddleware` to enforce security on ingestion endpoints.
- **Agent:** Support for `AGENT_TOKEN` environment variable.

## [0.2.0] - Sprint 2: Ingestion & Storage - 2026-01-01
### Added
- **Backend:** `tara-server` Ingestion Engine using Gin (HTTP).
- **Storage:** SQLite integration using `modernc.org/sqlite` (Pure Go).
- **Database:** Auto-migration for `agents` and `system_metrics` tables.
- **Agent:** Updated `tara-agent` to send JSON data via HTTP POST instead of stdout.

## [0.1.0] - Sprint 1: Foundation - 2026-01-01
### Added
- **Agent:** Core `tara-agent` implemented in Go.
- **Metrics:** CPU, Memory, and Disk usage collection (`gopsutil`).
- **Config:** Environment-based configuration (`AGENT_INTERVAL`, `LOG_LEVEL`).
- **Build:** `Makefile` for Go build automation.
- **Docs:** Initial Request for Comments (RFC) and Sprint Plans.
