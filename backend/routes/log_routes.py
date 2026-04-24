from fastapi import APIRouter
from logger import get_logs
from contracts import ErrorResponse, LogsResponse, success_response

router = APIRouter()

@router.get("/logs", response_model=LogsResponse, responses={422: {"model": ErrorResponse}})
async def fetch_logs():
    return success_response("Logs fetched", {"logs": get_logs()})
