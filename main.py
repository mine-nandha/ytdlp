from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
 
app = FastAPI()
 
# Allow all origins (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all domains
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
 
# Endpoint to get available formats
@app.get("/get-formats")
async def get_formats(video_url: str):
    ydl_opts = {"quiet": True, "noplaylist": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
 
    formats = [
        {"format_id": f["format_id"], "ext": f["ext"], "resolution": f.get("resolution", "audio"), "filesize": f.get("filesize")}
        for f in info["formats"]
    ]
 
    return {"title": info["title"], "formats": formats}
 
# Endpoint to get direct video URL for a specific format
@app.get("/get-url")
async def get_video_url(video_url: str, format_id: str = none):
    ydl_opts = {"quiet": True, "format": format_id, "noplaylist": True}
    if format_id:
        ydl_opts["format_id"] = format_id
    else:
        ydl_opts["format"] = "best"
        
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
    
    return {"url": info["url"], "title": info["title"], "format_id": format_id}