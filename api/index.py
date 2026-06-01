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
    """Get playable audio stream URL for a YouTube video"""
    try:
        import requests as req
        
        # Check cache first
        if video_id in stream_cache:
            cached = stream_cache[video_id]
            if time.time() - cached["timestamp"] < STREAM_CACHE_TTL:
                return {"status": "success", "url": cached["url"], "video_id": video_id, "type": "audio/mp3"}
        
        # Try using yt-dlp to extract audio URL
        try:
            from yt_dlp import YoutubeDL
            
            print(f"Extracting audio URL for video: {video_id}")
            
            # Configure yt-dlp to extract audio URL only (no download)
            ydl_opts = {
                'quiet': False,
                'no_warnings': False,
                'extract_flat': False,
                'skip_download': True,  # Important: don't download, just get URL
                'format': 'bestaudio',  # Get best audio format
                'socket_timeout': 15,
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
                
                if info and 'url' in info:
                    audio_url = info['url']
                    
                    # Cache it
                    stream_cache[video_id] = {
                        "url": audio_url,
                        "type": "audio",
                        "timestamp": time.time()
                    }
                    
                    print(f"Successfully extracted audio URL: {audio_url[:60]}...")
                    return {
                        "status": "success",
                        "url": audio_url,
                        "type": "audio/mp3",
                        "video_id": video_id
                    }
                else:
                    print("No audio URL in extracted info")
                    
        except ImportError:
            print("yt-dlp not available, trying alternative methods")
        except Exception as e:
            print(f"yt-dlp extraction failed: {str(e)}")
        
        # Fallback: Try using a direct MP3 conversion service
        try:
            print(f"Trying MP3 conversion service for {video_id}")
            
            # Use a service that converts YouTube to MP3
            conversion_url = f"https://api.paxsenixofficiel.fr/convert?url=https://www.youtube.com/watch?v={video_id}&format=mp3"
            
            resp = req.get(
                conversion_url,
                timeout=12,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            if resp.status_code == 200:
                data = resp.json()
                
                if data.get('status') == 'success' and 'url' in data:
                    audio_url = data['url']
                    
                    stream_cache[video_id] = {
                        "url": audio_url,
                        "type": "audio",
                        "timestamp": time.time()
                    }
                    
                    print(f"Got audio from conversion service")
                    return {
                        "status": "success",
                        "url": audio_url,
                        "type": "audio/mp3",
                        "video_id": video_id
                    }
        except Exception as e:
            print(f"Conversion service failed: {str(e)}")
        
        # If all methods fail, return error
        print(f"All audio extraction methods failed for {video_id}")
        return {
            "status": "error",
            "message": "Cannot extract audio. Try searching for the song instead - it may have more reliable sources.",
            "video_id": video_id,
            "suggestion": "Use the search feature to find alternate versions of the song"
        }
        
    except Exception as e:
        print(f"Stream endpoint error: {str(e)}")
        return {
            "status": "error",
            "message": str(e),
            "video_id": video_id
        }
