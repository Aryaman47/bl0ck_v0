# backend/main.py
from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
from fastapi import WebSocket
from mining_state import mining_state
import asyncio


# import routers (existing)
from routes import bl0ckchain_routes, difficulty_routes, mining_routes, log_routes

# use singleton blockchain instance you've already created
from singleton import blockchain
from bl0ckchain.mining import get_mining_timeout

app = FastAPI(title="The bl0ck 🔗 API")

# CORS - development-friendly (tighten origin list in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register routers
app.include_router(bl0ckchain_routes.router, prefix="/blockchain")
app.include_router(difficulty_routes.router, prefix="/difficulty")
app.include_router(mining_routes.router, prefix="/mining")
app.include_router(log_routes.router)

# status endpoint for frontend initialization
@app.get("/status")
async def status():
    """
    Returns authoritative server state for the frontend to initialize:
    - ddm_enabled: bool
    - ddm_mode: "auto" or "manual"
    - timeout: int (seconds)
    - difficulty: int (current difficulty set in difficulty_adjuster)
    - failed_difficulty: (optional) last failed difficulty or None
    """
    ddm_enabled = bool(getattr(blockchain, "dynamic_difficulty_enabled", False))
    ddm_mode = "manual" if getattr(blockchain, "manual_mode", False) else "auto"
    timeout = get_mining_timeout()
    difficulty = getattr(blockchain.difficulty_adjuster, "difficulty", 1)
    failed = getattr(blockchain.difficulty_adjuster, "failed_difficulty", None)

    return {
        "ddm_enabled": ddm_enabled,
        "ddm_mode": ddm_mode,
        "timeout": timeout,
        "difficulty": difficulty,
        "failed_difficulty": failed,
    }

@app.websocket("/ws/mining")
async def mining_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await asyncio.sleep(1)
            await websocket.send_json(mining_state.snapshot())
    except Exception as e:
        print(f"WebSocket error: {e}")

# serve frontend static files (index.html at root)
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")