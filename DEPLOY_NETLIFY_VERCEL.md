# Deploy to Netlify + Vercel

Panduan lengkap deploy **frontend ke Netlify** dan **backend Python API ke Vercel**.

## 📊 Architecture

```
┌─────────────────────────────────────────────┐
│         Netlify Frontend                    │
│  (index.html + assets)                      │
│  https://your-site.netlify.app              │
└─────────────────────────────────────────────┘
                    ↓
          Auto-detects Netlify domain
                    ↓
┌─────────────────────────────────────────────┐
│    Vercel Backend API (Python)              │
│  /api/search, /api/home                     │
│  https://nocteraappv2.vercel.app            │
└─────────────────────────────────────────────┘
```

---

## 🚀 Deploy Backend ke Vercel (5 menit)

### 1. Via Web Interface (Recommended)

1. Buka https://vercel.com
2. Click "Add New..." → "Project"
3. Connect GitHub repository: `nocteraappv2`
4. Vercel auto-detect `vercel.json` dan Python runtime
5. Deploy! 
6. **Copy production URL** (e.g., `https://nocteraappv2.vercel.app`)

### 2. Via Vercel CLI (Alternative)

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd /path/to/project
vercel

# Production deploy
vercel --prod
```

### Test Vercel Deployment

```bash
# Test search endpoint
curl "https://nocteraappv2.vercel.app/api/search?query=lagu%20indonesia"

# Test home endpoint  
curl "https://nocteraappv2.vercel.app/api/home"
```

Expected response:
```json
{
  "status": "success",
  "data": [...]
}
```

---

## 🌐 Deploy Frontend ke Netlify (3 menit)

### 1. Via Web Interface (Recommended)

1. Buka https://netlify.com
2. Click "Add new site" → "Import an existing project"
3. Connect GitHub → Select `nocteraappv2` repository
4. Build settings:
   - Build command: `echo 'No build required'`
   - Publish directory: `.`
5. Deploy!
6. **Netlify auto-assigns domain** (e.g., `your-site.netlify.app`)

### 2. Via Netlify CLI (Alternative)

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Login
netlify login

# Deploy
netlify deploy --prod
```

### Test Netlify Deployment

Buka `https://your-site.netlify.app` di browser:
- ✅ Aplikasi muncul
- ✅ Search bekerja
- ✅ Console log menunjukkan Vercel API URL

---

## 🔧 Configuration Reference

### index.html Auto-Detection

Script di `<head>` auto-detect environment:

```javascript
// Localhost Development
hostname = 'localhost'
→ API_BASE_URL = 'http://localhost:8000'

// Netlify Production  
hostname = '*.netlify.app'
→ API_BASE_URL = 'https://nocteraappv2.vercel.app/api'

// Vercel Production
hostname = '*.vercel.app'
→ API_BASE_URL = 'http://localhost:8000' or custom
```

### File Konfigurasi

**vercel.json** - Vercel deployment config
- Runtime: Python 3.11
- Build command: Install requirements
- API routes: /api/*.py → serverless functions

**netlify.toml** - Netlify deployment config
- Publish directory: . (root)
- Redirects: SPA routing to index.html
- Cache: Smart caching settings

---

## ✅ Deployment Checklist

### Backend (Vercel)
- [ ] Repository pushed ke GitHub
- [ ] vercel.json ada di root
- [ ] requirements.txt ada
- [ ] api/index.py ada
- [ ] Vercel deployment successful
- [ ] /api/search endpoint tested
- [ ] /api/home endpoint tested
- [ ] **Copy production URL**

### Frontend (Netlify)
- [ ] Repository pushed ke GitHub
- [ ] netlify.toml ada
- [ ] index.html ada dengan API_CONFIG
- [ ] Netlify deployment successful
- [ ] Akses domain netlify.app
- [ ] Console log show Vercel API URL
- [ ] Search test successful

---

## 🔍 Monitoring & Debugging

### Vercel Logs

```bash
# View logs
vercel logs

# Tail logs
vercel logs --tail
```

Or via Vercel Dashboard:
1. Go to Project
2. Click "Deployments"
3. Select latest deployment
4. Click "View Function Logs"

### Netlify Logs

1. Go to netlify.com
2. Select site
3. Click "Deploys"
4. Click specific deploy
5. View deployment log

### Browser Console (During Runtime)

Press `F12` → Console tab:
```
🔗 Development Mode - Localhost
OR
🔗 Production Mode - Netlify Frontend → Vercel Backend
```

---

## 🐛 Troubleshooting

### API 404 Not Found

```
❌ Failed to fetch https://nocteraappv2.vercel.app/api/search
404 Not Found
```

**Solutions:**
1. Check Vercel deployment succeeded (Dashboard → Deployments)
2. Check Python runtime selected (vercel.json)
3. Check requirements.txt has all dependencies
4. View function logs in Vercel dashboard

### CORS Error in Browser

```
❌ Access to fetch blocked by CORS policy
```

**Solution:**
- Backend already has CORS enabled in api/index.py
- Check network tab for actual error response
- Vercel might be showing HTML error page

### Search Returns Empty Results

```
✓ API responds but no songs in response
```

**Possible causes:**
1. YouTube Music API rate limited
2. ytmusicapi library needs update
3. Network connectivity issue

**Solution:**
- Try different search query
- Check server logs for details
- Wait a minute and retry

---

## 📱 Testing Checklist

### Development (Localhost)

```bash
python server.py
# Open index.html
# Search: Should show results
# Console: "Development Mode - Localhost"
```

### Staging (Vercel)

```bash
curl "https://nocteraappv2.vercel.app/api/search?query=test"
# Should return JSON with songs
```

### Production (Netlify)

```
1. Open https://your-site.netlify.app
2. Search for music
3. Check console: Should show Vercel API URL
4. Results should appear
```

---

## 🚀 Next Steps After Deployment

1. **Monitor Performance**
   - Check Vercel Analytics
   - Monitor Netlify speed insights

2. **Setup Custom Domain** (Optional)
   - Netlify: Domain settings
   - DNS configuration

3. **Enable Auto Deployments**
   - Both Netlify & Vercel auto-deploy on git push
   - No manual deployment needed!

4. **Set Up Alerts** (Optional)
   - Vercel function errors
   - Netlify build failures

---

## 📞 Support

Common issues & solutions:

| Issue | Check | Solution |
|-------|-------|----------|
| API not responding | Vercel logs | Check Python errors |
| Static assets 404 | Netlify build | Check file structure |
| CORS blocked | Browser console | Check API response |
| Search timeout | Both logs | YouTube API slow |

---

## 🔑 Important URLs to Save

```
🟢 GitHub: https://github.com/scoopstimes/nocteraappv2
🔵 Backend (Vercel): https://nocteraappv2.vercel.app
🟡 Frontend (Netlify): https://your-site.netlify.app
```

---

**Status: ✅ Ready to Deploy!**

All files configured and ready. Deploy to Vercel & Netlify now! 🚀
