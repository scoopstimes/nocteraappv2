from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ytmusicapi import YTMusic
import time
import subprocess
import json

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ytmusic = YTMusic()

# Cache untuk home data dan audio streams
home_cache = {}
stream_cache = {}
CACHE_TTL = 1800
STREAM_CACHE_TTL = 3600  # 1 hour untuk stream URLs

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

@app.get("/")
def root():
    return {"status": "ok", "message": "Musikin Aja API is running"}

@app.get("/search")
@app.get("/api/search")
def search_music(query: str):
    try:
        search_results = ytmusic.search(query, filter="songs", limit=12)
        return {"status": "success", "data": format_results(search_results)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/home")
@app.get("/api/home")
def get_home_data():
    current_time = time.time()
    
    if "data" in home_cache and (current_time - home_cache["timestamp"] < CACHE_TTL):
        return {"status": "success", "data": home_cache["data"]}

    try:
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
        
        home_cache["data"] = data
        home_cache["timestamp"] = current_time
        
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/stream")
@app.get("/api/stream")
def get_stream(video_id: str):
    """Get playable stream URL for a YouTube Music video"""
    try:
        # Check cache first
        if video_id in stream_cache:
            cached = stream_cache[video_id]
            if time.time() - cached["timestamp"] < STREAM_CACHE_TTL:
                return {"status": "success", "url": cached["url"]}
        
        # Try to get song info with streaming data
        info = ytmusic.get_song(video_id)
        
        # Extract playable URL from streaming data
        if "streamingData" in info and "adaptiveFormats" in info["streamingData"]:
            formats = info["streamingData"]["adaptiveFormats"]
            
            # Find audio format
            for fmt in formats:
                if "url" in fmt and "audio" in fmt.get("mimeType", ""):
                    url = fmt["url"]
                    # Cache it
                    stream_cache[video_id] = {
                        "url": url,
                        "timestamp": time.time()
                    }
                    return {"status": "success", "url": url}
        
        # Fallback: construct YouTube Music URL
        youtube_url = f"https://music.youtube.com/watch?v={video_id}"
        return {
            "status": "success",
            "url": youtube_url,
            "type": "youtube_music_link"
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
