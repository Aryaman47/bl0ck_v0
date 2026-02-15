# backend/routes/mining_routes.py
from fastapi import APIRouter, HTTPException
from bl0ckchain.mining import set_mining_timeout

router = APIRouter()

@router.post("/set-timeout/{timeout}")
async def update_mining_timeout(timeout: int):
    if timeout < 10 or timeout > 300:
        raise HTTPException(status_code=400, detail="❌ Invalid timeout! Please set a value between 10 and 300 seconds.")
    set_mining_timeout(timeout)
    return {"message": f"Mining timeout set to {timeout} seconds."}
