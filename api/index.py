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
        
        # Try multiple Piped instances
        piped_instances = [
            "https://piped.kavin.rocks",
            "https://piped.silkky.cloud",
            "https://piped.moomoo.me",
            "https://piped.artemislena.eu"
        ]
        
        for piped_instance in piped_instances:
            try:
                print(f"Trying Piped instance: {piped_instance}")
                
                # Get video info from Piped
                resp = req.get(
                    f'{piped_instance}/api/v1/streams/{video_id}',
                    timeout=10,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                
                if resp.status_code == 200:
                    data = resp.json()
                    audio_streams = data.get('audioStreams', [])
                    
                    # Get best quality audio
                    if audio_streams:
                        # Sort by bitrate (highest first)
                        audio_streams.sort(key=lambda x: x.get('bitrate', 0), reverse=True)
                        stream_url = audio_streams[0].get('url')
                        
                        if stream_url:
                            # Cache it
                            stream_cache[video_id] = {
                                "url": stream_url,
                                "type": "audio",
                                "timestamp": time.time()
                            }
                            
                            print(f"Success from {piped_instance}")
                            return {
                                "status": "success",
                                "url": stream_url,
                                "type": "audio/mp3",
                                "video_id": video_id
                            }
            except Exception as e:
                print(f"Piped instance {piped_instance} failed: {str(e)}")
                continue
        
        # Try HLS stream extraction using another method
        try:
            print(f"Trying alternative audio extraction for {video_id}")
            # Try using a direct YouTube extraction service
            alt_services = [
                f"https://yt-audio.herokuapp.com/api/v1/download?video_id={video_id}",
                f"https://api.codetabs.com/v1/proxy?quest=https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}"
            ]
            
            for service_url in alt_services:
                try:
                    resp = req.get(service_url, timeout=8, headers={'User-Agent': 'Mozilla/5.0'})
                    if resp.status_code == 200:
                        # If we get any response, try to extract URL
                        try:
                            json_data = resp.json()
                            if isinstance(json_data, dict) and 'download_url' in json_data:
                                stream_url = json_data['download_url']
                                stream_cache[video_id] = {
                                    "url": stream_url,
                                    "type": "audio",
                                    "timestamp": time.time()
                                }
                                return {
                                    "status": "success",
                                    "url": stream_url,
                                    "type": "audio/mp3",
                                    "video_id": video_id
                                }
                        except:
                            pass
                except:
                    pass
        except Exception as e:
            print(f"Alternative service failed: {str(e)}")
        
        # If all extraction methods fail, return error
        return {
            "status": "error",
            "message": "Unable to extract audio stream. Try searching for the song instead.",
            "video_id": video_id
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "video_id": video_id
        }
