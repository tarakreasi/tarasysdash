# Panduan Pengguna: Local AI Automation (Untuk Pemula)

Selamat datang! Panduan ini akan membantu Anda menggunakan kecerdasan buatan (AI) lokal di komputer Anda tanpa perlu internet (setelah setup awal) dan gratis selamanya.

## Setup Awal (Hanya Sekali)
Sebelum memulai, pastikan "mesin" AI Anda menyala.
1.  Buka terminal.
2.  Ketik perintah: `ollama list`
    *   Jika muncul daftar model (seperti `qwen2.5-coder`), Anda siap!
    *   Jika error, jalankan `python src/main.py` nanti setelah download selesai.

---

## Cara Menggunakan di VS Code / Antigravity IDE

### 1. Tab Autocomplete (Melengkapi Kode Otomatis)
Ini fitur "Magic Tab". AI akan menebak apa yang ingin Anda ketik.
*   **Cara Pakai**:
    1.  Mulai mengetik kode (misal: `def hitung_luas(`).
    2.  Tunggu sejenak, teks abu-abu akan muncul.
    3.  Tekan tombol `Tab` di keyboard untuk menerima saran tersebut.
*   **Tips**: Sangat berguna untuk menulis kode yang berulang atau boilerplate.

### 2. Chat Assistant (Tanya Jawab)
Ini seperti ChatGPT, tapi berjalan di komputer Anda sendiri.
*   **Cara Pakai**:
    1.  Tekan `Ctrl+L` (atau `Cmd+L` di Mac) untuk membuka panel chat di sebelah kanan.
    2.  Ketik pertanyaan Anda, misal: "Buatkan fungsi python untuk menghitung fibonacci".
    3.  AI akan menjawab dan menuliskan kodenya.
*   **Fitur Keren**:
    *   Anda bisa memblok kode di editor, lalu tekan `Ctrl+L`. AI akan otomatis tahu Anda bertanya tentang kode yang diblok tersebut.
    *   Ketik `/check` untuk meminta AI memeriksa error pada kode Anda.

### 3. Mengedit Kode (Edit Mode)
*   **Cara Pakai**:
    1.  Blok kode yang ingin diubah.
    2.  Tekan `Ctrl+I`.
    3.  Ketik perintah: "Tambahkan komentar pada kode ini" atau "Ubah variabel x menjadi y".
    4.  Tekan Enter. AI akan langsung mengubah kode di file Anda.

---

## Troubleshooting (Jika Ada Masalah)
1.  **AI Tidak Muncul / Lemot**:
    *   Cek apakah ada program berat lain yang berjalan. AI butuh RAM!
    *   Pastikan Ollama berjalan.
2.  **Saran Kode Aneh**:
    *   Terkadang AI bisa salah. Selalu cek ulang kode yang diberikan.

Selamat mencoba! 🚀
