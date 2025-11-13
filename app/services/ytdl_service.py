import yt_dlp
from fastapi.concurrency import run_in_threadpool
from fastapi import HTTPException

def _extract(url, opts):
    with yt_dlp.YoutubeDL(opts) as y:
        return y.extract_info(url, download=False)

async def extract_formats(url: str):
    try:
        info = await run_in_threadpool(
            _extract, url, {"quiet": True, "noplaylist": True}
        )
    except:
        raise HTTPException(400, "invalid url")

    out = []
    for f in info["formats"]:
        out.append({
            "format_id": f["format_id"],
            "ext": f["ext"],
            "resolution": f.get("resolution"),
            "filesize_approx": f.get("filesize_approx"),
            "has_av": f.get("acodec") != "none" and f.get("vcodec") != "none"
        })
    return {"title": info["title"], "formats": out}

async def extract_url(url: str, fmt: str | None):
    opts = {"quiet": True, "noplaylist": True, "format": fmt or "best"}

    try:
        info = await run_in_threadpool(_extract, url, opts)
    except:
        raise HTTPException(400, "invalid url or unavailable format")

    return {"url": info["url"], "title": info["title"], "format": fmt or "best"}