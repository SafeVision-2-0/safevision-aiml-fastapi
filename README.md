## 🚀 Cara Menjalankan Aplikasi (Local Development)

Ikuti langkah-langkah berikut untuk menjalankan FastAPI di environment lokal.

---

### 1️⃣ Clone Repository

```bash
git clone https://github.com/USERNAME/NAMA-REPO.git
cd NAMA-REPO
```

---

### 2️⃣ Buat Virtual Environment

#### Windows

```bash
python -m venv venv
```

#### Linux / macOS

```bash
python3 -m venv venv
```

---

### 3️⃣ Aktifkan Virtual Environment

#### Windows (PowerShell)

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

Jika berhasil, terminal akan menampilkan:

```text
(venv)
```

---

### 4️⃣ Install Dependencies

Pastikan berada di root project, lalu jalankan:

```bash
pip install -r requirements.txt
```

---

### 5️⃣ Jalankan FastAPI Server

Gunakan **uvicorn** untuk menjalankan aplikasi FastAPI yang berada di `app/main.py`:

```bash
uvicorn app.main:app --reload
```

Keterangan:

* `app.main` → lokasi file `main.py`
* `app` → instance FastAPI
* `--reload` → auto-reload saat development

---

### 6️⃣ Akses Aplikasi

* API root:

  ```
  http://127.0.0.1:8000
  ```

* Swagger UI (API Documentation): (Progress)

  ```
  http://127.0.0.1:8000/docs
  ```

* ReDoc: (Progress)

  ```
  http://127.0.0.1:8000/redoc
  ```

---

### 7️⃣ Menghentikan Server

Tekan:

```text
CTRL + C
```

---

## 📁 Struktur Entry Point

```text
app/
└── main.py   ← Entry point FastAPI
```

---

## ℹ️ Catatan

* Pastikan **Python 3.9+** sudah terinstall
* Virtual environment **wajib aktif** saat development
* Gunakan `.env` untuk konfigurasi sensitif (jangan di-push ke GitHub)

---
