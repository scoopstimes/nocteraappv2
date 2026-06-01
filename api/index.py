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
    return {"status": "ok", "message": "Musikin Aja API v2 - Real audio streaming"}

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
    """
    Try to get audio stream, but recommend search-based playback.
    When given a video_id, search for song info and return searchable results.
    """
    try:
        # Check cache first
        if video_id in stream_cache:
            cached = stream_cache[video_id]
            if time.time() - cached["timestamp"] < STREAM_CACHE_TTL:
                return {"status": "success", "url": cached["url"], "video_id": video_id, "type": "audio/mp3"}
        
        # For direct video extraction, suggest using search instead
        # This endpoint primarily tells the frontend "use search results for better audio"
        return {
            "status": "redirect",
            "message": "Direct video playback limited. Use search to find and play songs.",
            "video_id": video_id,
            "recommendation": "search"  # Signal to frontend to use search-based playback
        }
        
    except Exception as e:
        print(f"Stream endpoint error: {str(e)}")
        return {
            "status": "error",
            "message": str(e),
            "video_id": video_id
        }
