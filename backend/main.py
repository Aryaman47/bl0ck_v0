# main.py
from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore

# import routers (existing)
from routes import bl0ckchain_routes, difficulty_routes, mining_routes

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

# serve frontend static files (index.html at root)
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
