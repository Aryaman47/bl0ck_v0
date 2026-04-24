# backend/routes/mining_routes.py
from fastapi import APIRouter, HTTPException
from bl0ckchain.mining import set_mining_timeout
from contracts import ErrorResponse, MiningTimeoutResponse, success_response

router = APIRouter()

@router.post("/set-timeout/{timeout}", response_model=MiningTimeoutResponse, responses={400: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
async def update_mining_timeout(timeout: int):
    if timeout < 10 or timeout > 300:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_TIMEOUT",
                "message": "Invalid timeout. Please set a value between 10 and 300 seconds.",
                "details": {
                    "min": 10,
                    "max": 300,
                    "provided": timeout,
                },
            },
        )
    set_mining_timeout(timeout)
    return success_response(
        f"Mining timeout set to {timeout} seconds.",
        {"timeout": timeout},
    )