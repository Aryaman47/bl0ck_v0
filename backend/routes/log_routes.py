from fastapi import APIRouter
from logger import get_logs

router = APIRouter()

@router.get("/logs")
async def fetch_logs():
    return {"logs": get_logs()}
