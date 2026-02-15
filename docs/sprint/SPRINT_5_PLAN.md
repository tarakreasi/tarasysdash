# 🚀 Sprint 5: Windows Upgrade - Production Ready

**Objective**: Upgrade TaraSysDash agent untuk production deployment di 50 Windows Server, dengan menambahkan Windows Service mode, Temperature monitoring via WMI, dan Alert System.

**Status**: PLANNING

**Spec Reference**: `docs/specs/2026-01-16-tarasysdassh-windows-upgrade/spec.md`

---

## 📋 Micro-Sprints Breakdown

Sprint ini dipecah menjadi 5 micro-sprints untuk eksekusi bertahap:

### [ ] Sprint 5.1: Windows Service Mode
**Focus**: Implement `kardianos/service` untuk menjalankan agent sebagai Windows Service.
- Add dependency `kardianos/service`
- Refactor `cmd/agent/main.go` untuk implement `service.Interface`
- Support commands: `install`, `uninstall`, `start`, `stop`, `run`
- **Verification**: Agent muncul di `services.msc`, auto-start setelah reboot

### [ ] Sprint 5.2: WMI Temperature Collection
**Focus**: Tambahkan pengumpulan CPU temperature di Windows via WMI.
- Query `MSAcpi_ThermalZoneTemperature` menggunakan `yusufpapurcu/wmi`
- Konversi ke Celsius: `(CurrentTemperature / 10) - 273.15`
- Handle unsupported hardware dengan return `-1` (N/A)
- **Verification**: Nilai temperature muncul di dashboard untuk Windows agent

### [ ] Sprint 5.3: Windows Collector Parity
**Focus**: Pastikan semua metrics Linux tersedia di Windows.
- Add `UptimeSeconds` collection di `collector_windows.go`
- Add `ProcessCount` collection di `collector_windows.go`
- **Verification**: Semua gauge charts di dashboard bekerja untuk Windows

### [ ] Sprint 5.4: Alert System Backend
**Focus**: Implementasi alert system di backend.
- Add `alerts` table di SQLite schema
- Implement threshold evaluation on metric submission
- Add API endpoints: `GET /api/v1/alerts`, `GET /api/v1/alerts/:agent_id`
- Alert states: `firing` → `resolved`
- **Verification**: Alert muncul di database saat threshold terlampaui

### [ ] Sprint 5.5: Email Notification & Dashboard
**Focus**: Email notification dan tampilan alert di dashboard.
- SMTP configuration di config file
- Send email on alert firing (jika enabled)
- Add alert section di dashboard Vue
- **Verification**: Email terkirim saat threshold terlampaui (jika enabled)

---

## 📊 Effort Estimation

| Sprint | Focus | Effort |
|--------|-------|--------|
| 5.1 | Windows Service Mode | 1 day |
| 5.2 | WMI Temperature | 0.5 day |
| 5.3 | Collector Parity | 0.5 day |
| 5.4 | Alert Backend | 1 day |
| 5.5 | Email & Dashboard | 1 day |
| | **Total** | **4 days** |

---

## 🎯 Definition of Done (Parent Sprint)

- [ ] Agent dapat di-install sebagai Windows Service
- [ ] Temperature muncul di dashboard untuk Windows agent
- [ ] Uptime dan ProcessCount tersedia di Windows
- [ ] Alert triggered when threshold exceeded
- [ ] Email notification berfungsi (jika enabled)
- [ ] Semua acceptance criteria di spec terpenuhi

---

## 📁 Root Folder

**Project Root**: `taraSysDash/`

---

## 🔗 Related Documents

- Research: `docs/research/research_tarasysdassh_windows_monitoring_20260116.md`
- Gap Analysis: `docs/research/gap_tarasysdassh_windows_20260116.md`
- Specification: `docs/specs/2026-01-16-tarasysdassh-windows-upgrade/spec.md`
