# VS Code / Antigravity Optimization Guide

Agar IDE Anda berjalan maksimal di hardware menengah (i5/16GB), ikuti langkah-langkah "Diet Digital" ini:

## Langkah 1: Bersihkan Sampah (Cache)
Jalankan script otomatis yang telah saya buat untuk menghapus file sementara yang menumpuk.
```bash
chmod +x scripts/optimize_ide.sh
./scripts/optimize_ide.sh
```

## Langkah 2: Terapkan Setting Performa
Salin isi file `docs/vscode_performance_settings.json` ke dalam `settings.json` Anda.
**Efek**:
- Mematikan Minimap (Hemat RAM/GPU).
- Mematikan Smooth Scrolling (Hemat CPU).
- Mengabaikan folder `.venv` dan `node_modules` saat searching (Pencarian jadi instan).

## Langkah 3: Audit Ekstensi
Ekstensi adalah penyebab utama VS Code lambat.
1.  Buka tab Extensions (`Ctrl+Shift+X`).
2.  Ketik `@installed`.
3.  **Matikan/Hapus** ekstensi yang jarang dipakai (misal: Theme berat, Bracket colorizer lama yang sudah built-in, atau Snippets bahasa yang tidak dipakai).
4.  **Wajib Install**:
    -   **Continue**: Untuk AI lokal kita.
    -   **Python**: Untuk development.
    -   **Pylance**: Untuk intellisense cepat.

## Langkah 4: Runtime Arguments (Advanced)
Jika masih terasa berat, Anda bisa memaksa VS Code berjalan dalam mode hemat daya dengan mengubah shortcut peluncurnya:
`code --disable-gpu` (Jika grafis terasa patah-patah).
