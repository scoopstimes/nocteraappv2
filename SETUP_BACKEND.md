# Musikin Aja - Python FastAPI Backend Setup

Panduan setup untuk menjalankan backend Python FastAPI dengan YouTube Music API.

## Prerequisites

- Python 3.8 atau lebih tinggi
- pip (Python Package Manager)

## Setup Instructions

### 1. Install Dependencies

Buka terminal di folder project dan jalankan:

```bash
pip install -r requirements.txt
```

### 2. Jalankan Server

```bash
python server.py
```

Server akan berjalan di `http://localhost:8000`

Anda akan melihat output seperti:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 3. Tes API

Buka browser dan coba:
- **Search Music**: `http://localhost:8000/api/search?query=lagu+indonesia`
- **Home Data**: `http://localhost:8000/api/home`

### API Endpoints

#### 1. Search Music
- **URL**: `/api/search?query=<search_query>`
- **Method**: GET
- **Example**: `/api/search?query=lagu%20indonesia`

**Response Success (200)**:
```json
{
  "status": "success",
  "data": [
    {
      "videoId": "abc123xyz",
      "title": "Lagu Title",
      "artist": "Artist Name",
      "thumbnail": "https://..."
    }
  ]
}
```

#### 2. Get Home Data
- **URL**: `/api/home`
- **Method**: GET
- **Description**: Mendapatkan data home dengan 8 kategori musik yang di-cache

**Response Success (200)**:
```json
{
  "status": "success",
  "data": {
    "recent": [...],
    "anyar": [...],
    "gembira": [...],
    "charts": [...],
    "galau": [...],
    "baru": [...],
    "tiktok": [...],
    "artists": [...]
  }
}
```

### Troubleshooting

#### 1. ModuleNotFoundError
**Solusi**: Pastikan semua dependencies sudah terinstall dengan benar
```bash
pip install -r requirements.txt
```

#### 2. Connection Refused
**Solusi**: Pastikan server berjalan di port 8000. Cek apakah port sudah digunakan:
- Windows: `netstat -ano | findstr :8000`
- Linux/Mac: `lsof -i :8000`

#### 3. YouTube Music API Error
**Solusi**: Pastikan koneksi internet stabil. API YTMusic mungkin memerlukan:
- Cookie autentikasi (untuk beberapa fitur lanjutan)
- Vpn jika akses diblokir di region tertentu

### Environment Variables (Optional)

Buat file `.env` jika diperlukan konfigurasi khusus:
```
API_PORT=8000
CACHE_TTL=1800
```

### Performance Tips

1. **Cache System**: Server menggunakan cache 30 menit untuk home data
2. **Limit Results**: Search API mengembalikan max 12 hasil untuk performa optimal
3. **Concurrent Requests**: FastAPI support multiple concurrent requests

### Production Deployment

Untuk production, gunakan Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker server:app
```

### Development Mode with Auto-Reload

```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

---

**Note**: Client-side JavaScript sudah dikonfigurasi untuk memanggil API di `http://localhost:8000`. Pastikan server berjalan sebelum menggunakan aplikasi!
