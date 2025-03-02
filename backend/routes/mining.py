from fastapi import APIRouter
from ..bl0ckchain.mining import set_mining_timeout

router = APIRouter()

@router.post("/set-timeout/{timeout}")
async def update_mining_timeout(timeout: int):
    """Set a custom mining timeout."""
    set_mining_timeout(timeout)
    return {"message": f"Mining timeout set to {timeout} seconds."}
