# 🔄 Automation & Looping System Changelog

Tujuan: Mencatat evolusi script supervisor dan orchestrator dalam mencapai Full Autonomous Sprint Execution.

---

## [1.1.0] - 2026-01-17
### Added
- **`marathon.py` (The Orchestrator)**: Script baru untuk menjalankan Batch Execution pada sprint-sprint yang tertunda.
  - **Auto-Scan**: Mencari file `.md` di `docs/dev/sprints/`.
  - **Smart Filtering**: Hanya mengambil sprint dengan status `**Status**: PLANNING`.
  - **Numeric Sorting**: Mengurutkan eksekusi berdasarkan nomor sprint (misal: 6.2.1 → 6.2.2).
  - **State Persistence**: Otomatis mengubah status file markdown dari `PLANNING` ke `DONE` setelah eksekusi sukses.
  - **Safety Halt**: Berhenti otomatis jika terjadi error pada salah satu sprint untuk mencegah cascade errors.

### Changed
- **Execution Workflow**: Migrasi dari manual single-file execution (`execute_sprint_manual.py`) ke loop-based execution (`marathon.py`).
- **User Manual Integration**: Menambahkan diagram dan instruksi khusus untuk menjalankan marathon loop.

### Technical Specs
- **Logic Level**: Sequential Synchronous (FIFO).
- **LLM Engine**: Qwen 2.5 7B via Local API (10.42.1.10:8081).
- **Status Markers**: Strict string matching untuk `**Status**: PLANNING` agar kompatibel dengan template High-Fidelity.

---

## [1.0.0] - 2026-01-16
### Added
- **`execute_sprint.py`**: Pekerja inti (Worker) yang melakukan parsing Markdown dan interaksi API Qwen.
- **CodeExtractor V1**: Regex-based extraction untuk mengambil code block dari respons AI.
- **`execute_sprint_manual.py`**: Wrapper sederhana untuk menjalankan satu file sprint.

### Fixed
- **Markdown Fence Hallucination**: Menambahkan filter regex untuk membersihkan ` ```php ` atau ` ```typescript ` dari isi file yang disimpan ke disk.

---

### 🚀 Roadmap Selanjutnya
- [ ] **Self-Healing Loop**: Integrasi dengan `supervisor_ultimate.py` untuk otomatis memperbaiki file jika `verify_sprint.py` gagal.
- [ ] **Parallel Generation**: Kemampuan menjalankan multiple Qwen instances (jika GPU memadai).
- [ ] **Git Integration**: Auto-commit setiap kali satu sprint di marathon selesai (saat ini masih manual).

---
*Created by: Antigravity Senior Automation Engineer*
