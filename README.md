# Musikin Aja - Production Ready

Project musik streaming dengan FastAPI backend dan frontend statis.

## 📁 Struktur Project

```
musikin-aja/
├── index.html           # Frontend main app (22000+ lines)
├── server.py            # FastAPI backend (production-ready)
├── requirements.txt     # Python dependencies
├── Procfile             # Heroku/Railway deployment
├── runtime.txt          # Python version specification
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
├── SETUP_BACKEND.md     # Backend setup guide
├── DEPLOY_GUIDE.md      # Production deployment guide
├── start-server.bat     # Windows server starter
├── start-server.sh      # Linux/Mac server starter
└── profile-functions.js # Utility functions
```

## 🚀 Quick Start

### Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start backend
python server.py
# atau
./start-server.bat        # Windows
./start-server.sh         # Linux/Mac

# 3. Open browser
# index.html akan auto-connect ke http://localhost:8000
```

### Production

```bash
# 1. Deploy backend ke Railway/Heroku/Render
# Lihat DEPLOY_GUIDE.md

# 2. Deploy frontend ke Vercel
# Pilih repository di https://vercel.com

# index.html auto-detect production URL
# Tidak perlu manual config!
```

## 🔧 Tech Stack

- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **Backend**: FastAPI + Uvicorn
- **Music API**: YouTube Music API (ytmusicapi)
- **Database**: Firebase (optional, for user data)
- **Hosting**:
  - Backend: Railway/Heroku/Render
  - Frontend: Vercel

## 📊 API Endpoints

### Search Music
```
GET /api/search?query=<search_query>

Response:
{
  "status": "success",
  "data": [
    {
      "videoId": "...",
      "title": "...",
      "artist": "...",
      "thumbnail": "..."
    }
  ]
}
```

### Home Data
```
GET /api/home

Response:
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

### Health Check
```
GET /

Response:
{
  "status": "ok",
  "message": "Musikin Aja API is running"
}
```

## ⚙️ Configuration

### Development (.env)
```env
PORT=8000
CACHE_TTL=1800
```

### Production
- Automatic environment detection di index.html
- Development: `http://localhost:8000`
- Production: `https://your-domain.com`

## 📝 Features

✅ Search music dari YouTube Music API
✅ Home feed dengan 8 kategori musik
✅ Caching 30 menit untuk performance
✅ CORS enabled untuk cross-origin requests
✅ Production-ready dengan error handling
✅ Auto environment detection (dev/prod)

## 🛠️ Development Commands

```bash
# Run server dengan auto-reload (dev)
uvicorn server:app --reload

# Run server (production)
python server.py

# Test API endpoints
curl http://localhost:8000/api/search?query=lagu%20indonesia
curl http://localhost:8000/api/home

# Install new dependencies
pip install package_name
pip freeze > requirements.txt
```

## 📚 Documentation

- [Backend Setup](SETUP_BACKEND.md) - Detailed backend setup guide
- [Deployment Guide](DEPLOY_GUIDE.md) - Production deployment steps
- [API Reference](SETUP_BACKEND.md#api-endpoints) - Full API documentation

## 🐛 Troubleshooting

### Server tidak bisa start
```
❌ ModuleNotFoundError: No module named 'fastapi'
```
**Solusi**: `pip install -r requirements.txt`

### API 404 Not Found
```
❌ Failed to connect to http://localhost:8000
```
**Solusi**: Pastikan server berjalan `python server.py`

### CORS Error di Browser
**Solusi**: Server sudah punya CORS config, cek console untuk detail

## 📱 Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Android)

## 📄 License

Private project - Musikin Aja by Januar Adhi N

## 📞 Support

Untuk issues atau pertanyaan:
1. Check troubleshooting di atas
2. Check logs: `python server.py` (development)
3. Check browser console untuk frontend errors

---

**Next Steps:**
1. ✅ Backend setup selesai
2. ✅ Frontend terintegrasi dengan API
3. ⏳ Deploy ke production (Railway/Heroku untuk backend, Vercel untuk frontend)
4. ⏳ Monitor & maintain

Happy coding! 🎵
