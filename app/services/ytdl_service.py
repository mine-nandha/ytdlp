import yt_dlp
from fastapi.concurrency import run_in_threadpool
from fastapi import HTTPException

def _extract(url, opts):
    with yt_dlp.YoutubeDL(opts) as y:
        return y.extract_info(url, download=False)

async def extract_formats(url: str):
    try:
        info = await run_in_threadpool(
            _extract,
            url,
            {"quiet": False, "noplaylist": True}
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"yt-dlp error (formats): {type(e).__name__}: {str(e)}"
        )

    out = []
    for f in info.get("formats") or [] :
        out.append({
            "format_id": f.get("format_id"),
            "ext": f.get("ext"),
            "resolution": f.get("resolution"),
            "filesize": f.get("filesize"),
            "filesize_approx": f.get("filesize_approx"),
            "has_av": f.get("acodec") != "none" and f.get("vcodec") != "none"
        })

    return {
        "title": info.get("title"),
        "formats": out
    }

async def extract_url(url: str, fmt: str | None):
    opts = {"quiet": True, "noplaylist": True, "format": fmt or "best"}

    try:
        info = await run_in_threadpool(_extract, url, opts)
    except Exception as e:
        raise HTTPException(400, f"yt-dlp error: {type(e).__name__}: {str(e)}")

    direct = info.get("url")
    if not direct:
        raise HTTPException(500, "yt-dlp returned no URL")

    # 🟦 If m3u8 — just return unsupported
    if direct.endswith(".m3u8"):
        return {
            "supported": False,
            "type": "hls",
            "url": direct,
            "message": "m3u8/HLS is not supported by this server. Use the link directly."
        }

    # normal direct link
    return {
        "supported": True,
        "type": "file",
        "url": direct,
        "title": info.get("title"),
        "format": fmt or "best",
    }
