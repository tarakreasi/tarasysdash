# Catatan Terakhir & Analisa "Bottleneck" Project (Bootlenect)

Dokumen ini merangkum status terakhir proyek `taraSysDash` berdasarkan inspeksi kode terkini pada **2026-01-07**.

## � Status Terkini (Real-Time Code Check)

### 1. Backend (`cmd/server`) - **READY** ✅
Berlawanan dengan asumsi awal, Backend ternyata **sudah siap** melayani trafik Dashboard.
*   **API Read:** Endpoint sudah tersedia dan lengkap:
    *   `GET /api/v1/agents`: Listing agent aktif.
    *   `GET /api/v1/metrics/:agent_id`: Mengambil 60 data points terakhir.
    *   `GET /api/v1/metrics/:agent_id/network`: Kalkulasi throughput (Mbps) di sisi server.
*   **CORS:** Sudah diaktifkan untuk semua origin (`*`), memungkinan akses dari localhost:5173.
*   **Storage:** Menggunakan SQLite dengan rotasi data otomatis (Watchdog loop).

### 2. Frontend (`web/`) - **PARTIAL** ⚠️
Dashboard Vue 3 sudah berjalan dan memiliki desain dasar "Zen Glass", namun integrasi datanya belum sempurna.
*   **Integrasi API:** Frontend sudah memanggil API (`/agents` dan `/metrics`), namun...
*   **Charts (Bottleneck Utama):**
    *   **Gauges:** Sudah terupdate dengan data real (CPU/RAM/Temp) dari API.
    *   **Line/Bar Charts:** Masih menggunakan **MOCK DATA** (random) untuk history. Fungsi `renderCpuChart` membuat data palsu (`Math.random()`) daripada memplot array data yang dikembalikan endpoint `/metrics/:agent_id`.
*   **Visual:** Efek "Glow" sudah ada (via CSS `drop-shadow` dan ECharts gradient), namun perlu dipoles agar sesuai mockup (scanline, dll).

## 🛑 Hambatan Utama (The Real Bottleneck)

Hambatan sesungguhnya bukan di Backend, melainkan di logic **Visualisasi Frontend**:

1.  **Mapping Data Chart:** Kita perlu mengubah `renderCpuChart()` dan `renderMemoryChart()` agar menerima array data historis dari backend (`response.data`) alih-alih men-generate data acak.
2.  **Reaktivitas:** Memastikan chart di-update secara efisien saat polling data baru masuk (polling interval sudah ada, tapi logic update chart history belum).

## � Rekomendasi Langkah Selanjutnya (Action Plan)

Abaikan pengerjaan Backend (sudah cukup bagus). Fokus 100% pada Frontend:

1.  **Fix Chart Data Pipeline:**
    *   Ubah API Call di `DashboardView.vue` agar data history dari `/metrics/:agent_id` diparsing ke dalam array ECharts.
    *   Hapus `Math.random()` pada `renderCpuChart` dan `renderMemoryChart`.

2.  **Refine Visual:**
    *   Pastikan efek Scanline overlay terlihat jelas.
    *   Tweak warna gradients pada ECharts agar lebih "Neon/Cyberpunk" sesuai desain.

---
*Status Last Updated: 2026-01-07 (Verified by Code Inspection)*
