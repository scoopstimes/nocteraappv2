# Deploy Musikin Aja ke Production

Panduan lengkap untuk deploy Python FastAPI backend ke Railway, Heroku, atau Render.

## Pilihan Platform Deployment

### 1. Railway (⭐ Recommended - Free tier terbaik)

**Kelebihan:**
- Free tier generous
- Deploy langsung dari GitHub
- Auto-deploy pada git push
- Environment variables mudah

**Langkah:**

1. Buka https://railway.app dan login dengan GitHub
2. Click "New Project" → "Deploy from GitHub"
3. Pilih repository `Musikin-Aja-New`
4. Railway akan otomatis detect Procfile dan deploy
5. Tunggu build selesai (2-5 menit)
6. Copy domain yang diberikan (contoh: `https://musikin-api-production.up.railway.app`)

**Update index.html:**
- Buka `index.html` di editor
- Script di `<head>` akan otomatis detect production domain
- Tidak perlu manual update!

---

### 2. Heroku

**Kelebihan:**
- Populer dan reliable
- Easy integration dengan GitHub

**Langkah:**

1. Buat akun di https://www.heroku.com
2. Install Heroku CLI dari https://devcenter.heroku.com/articles/heroku-cli
3. Terminal:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

4. Ambil URL dari output:
```
https://your-app-name.herokuapp.com
```

---

### 3. Render

**Kelebihan:**
- Modern platform
- Free tier dengan sleep time
- Integration dengan GitHub

**Langkah:**

1. Buka https://render.com dan login
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Environment: Python 3.11
5. Build command: `pip install -r requirements.txt`
6. Start command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
7. Deploy

---

## Konfigurasi Production

### Environment Variables yang Diperlukan:

```env
PORT=8000              # Auto-set by platform
PYTHON_VERSION=3.11    # Optional
```

### Automatic Configuration

Script di index.html sudah handle production URLs:

```javascript
// Development (localhost)
const API_BASE_URL = 'http://localhost:8000'

// Production (auto-detect)
const API_BASE_URL = window.location.origin
```

**Contoh:**
- Localhost: API calls ke `http://localhost:8000/api/search`
- Production: API calls ke `https://your-domain.com/api/search`

---

## Setup Final di Frontend (Vercel)

Setelah backend di-deploy:

1. Push `index.html` ke GitHub
2. Buka https://vercel.com → "New Project"
3. Import repository `Musikin-Aja-New`
4. Vercel auto-build static files
5. Deploy ke domain Vercel

**File yang akan di-serve:**
- `index.html` (main app)
- Assets statis (CSS, JS)

**Backend API yang akan dipanggil:**
- `https://your-backend-domain.com/api/search`
- `https://your-backend-domain.com/api/home`

---

## Testing Production

Setelah deploy, test endpoints:

```bash
# Test search
curl "https://your-api-domain.com/api/search?query=lagu%20indonesia"

# Test home data
curl "https://your-api-domain.com/api/home"

# Test health check
curl "https://your-api-domain.com/"
```

---

## Troubleshooting

### 404 Not Found
```
❌ curl https://your-domain.com/api/search
404 Not Found
```
**Solusi:** Pastikan backend sudah di-deploy dan URL benar

### CORS Error di Browser Console
```
❌ Access to XMLHttpRequest blocked by CORS policy
```
**Solusi:** Backend sudah punya CORS config, tapi cek:
- Domain index.html tidak diblokir
- Server tidak down

### API Response Timeout
```
❌ Failed to fetch (timeout)
```
**Solusi:**
- First request cepat (health check)
- Subsequent requests ke YouTube Music bisa lambat
- Tunggu 10-30 detik untuk search pertama

---

## Monitoring & Logs

### Railway
```bash
# Lihat logs real-time
railway logs
```

### Heroku
```bash
# Lihat logs
heroku logs --tail --app your-app-name
```

### Render
- Dashboard → Web Service → Logs

---

## Perintah Helpful

```bash
# Test server lokal sebelum deploy
python server.py

# Cek requirements ada semua
pip install -r requirements.txt

# Cek syntax server.py
python -m py_compile server.py

# Test API search
curl "http://localhost:8000/api/search?query=test"
```

---

## Production Checklist

- [ ] Backend di-deploy ke Railway/Heroku/Render
- [ ] Backend URL ditest dan berfungsi
- [ ] index.html sudah pull latest changes (dengan API_CONFIG)
- [ ] Frontend di-deploy ke Vercel
- [ ] Test search di production
- [ ] Check browser console untuk errors
- [ ] Monitor backend logs

---

**Status Deployment Anda:**
- Backend: [Railway/Heroku/Render] - `https://your-backend-url.com`
- Frontend: [Vercel] - `https://your-frontend-url.vercel.app`

Browser akan otomatis gunakan production URLs saat akses lewat Vercel domain!
