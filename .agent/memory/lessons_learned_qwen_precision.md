# 🧠 Lessons Learned: Combatting LLM Bias in Code Generation

**Tanggal**: 2026-01-17
**Konteks**: Pengembangan MoneyTracker dengan Qwen 2.5 7B.

## 🔴 Masalah: "The Description Hallucination"
Meskipun `DOMAIN_CONTRACT.md` sudah mendefinisikan field `title`, Qwen secara konsisten (bias training data) menggunakan `description`. Peringatan global di awal file sering kali "tenggelam" oleh konteks yang panjang.

## 🟢 Solusi: "Brutal Local Patching"
Ditemukan bahwa instruksi yang diletakkan **tepat di dalam deskripsi Task** (lokal) jauh lebih efektif daripada instruksi di level file (global).

### Prinsip Utama:
1. **Local Context is King**: Masukkan daftar field "FORBIDDEN" tepat sebelum blok pembuatan kode.
2. **Technical Guardrails**: Sebutkan secara eksplisit detail yang sering meleset (misal: `computed` vs `ref`, wrapping `data`, naming convention).
3. **Log Truncation**: Untuk sistem Self-Healing, log error harus dipangkas (trailing 3000 chars) agar tidak melebihi kapasitas konteks model.

---
