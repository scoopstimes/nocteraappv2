from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from ytmusicapi import YTMusic
from fastapi.middleware.cors import CORSMiddleware
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ytmusic = YTMusic()

# Cache sementara (10-30 menit) untuk mengurangi beban request berulang ke YouTube
home_cache = {}
CACHE_TTL = 1800 # 30 menit dalam detik

@app.get("/")
def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Musikin Aja API is running"}

def format_results(search_results):
    cleaned_results = []
    for item in search_results:
        if 'videoId' in item:
            cleaned_results.append({
                "videoId": item['videoId'],
                "title": item.get('title', 'Unknown Title'),
                "artist": item.get('artists', [{'name': 'Unknown Artist'}])[0]['name'] if 'artists' in item else 'Unknown Artist',
                "thumbnail": item['thumbnails'][-1]['url'] if 'thumbnails' in item else ''
            })
    return cleaned_results

@app.get("/api/search")
def search_music(query: str):
    try:
        search_results = ytmusic.search(query, filter="songs", limit=12)
        return {"status": "success", "data": format_results(search_results)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/home")
def get_home_data():
    current_time = time.time()
    
    # Cek apakah data cache ada dan belum kadaluarsa
    if "data" in home_cache and (current_time - home_cache["timestamp"] < CACHE_TTL):
        return {"status": "success", "data": home_cache["data"]}

    try:
        # Menggabungkan 8 request menjadi 1 respon JSON untuk mencegah Vercel Timeout / Rate Limit
        data = {
            "recent": format_results(ytmusic.search('lagu indonesia hits terbaru', filter="songs", limit=4)),
            "anyar": format_results(ytmusic.search('lagu pop indonesia rilis terbaru anyar', filter="songs", limit=8)),
            "gembira": format_results(ytmusic.search('lagu ceria gembira semangat', filter="songs", limit=8)),
            "charts": format_results(ytmusic.search('top 50 indonesia playlist update', filter="songs", limit=8)),
            "galau": format_results(ytmusic.search('lagu galau sedih indonesia terpopuler', filter="songs", limit=8)),
            "baru": format_results(ytmusic.search('lagu viral terbaru 2026', filter="songs", limit=8)),
            "tiktok": format_results(ytmusic.search('lagu fyp tiktok viral jedag jedug', filter="songs", limit=8)),
            "artists": format_results(ytmusic.search('penyanyi pop indonesia paling hits', filter="songs", limit=8))
        }
        
        # Simpan hasil ke cache memori server
        home_cache["data"] = data
        home_cache["timestamp"] = current_time
        
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/get-song-url")
def get_song_url(video_id: str):
    """Get playable URL for a YouTube Music video"""
    try:
        # Get the song info to get the URL
        info = ytmusic.get_song(video_id)
        if 'streamingData' in info:
            # Extract the playable URL
            streams = info['streamingData'].get('adaptiveFormats', [])
            if streams:
                # Get the first audio stream that works
                for stream in streams:
                    if 'url' in stream:
                        return {"status": "success", "url": stream['url']}
        
        return {"status": "error", "message": "Could not extract playable URL"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
