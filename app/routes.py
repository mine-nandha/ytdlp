from fastapi import APIRouter
from app.services.ytdl_service import extract_formats, extract_url
from fastapi import APIRouter

router = APIRouter()

@router.get("/get-formats")
async def formats(url: str):
    return await extract_formats(url)

@router.get("/get-url")
async def direct(url: str, format_id: str | None = None):
    return await extract_url(url, format_id)