# backend/main.py
from fastapi import APIRouter, FastAPI, HTTPException, Request # type: ignore
from fastapi.exceptions import RequestValidationError # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.responses import JSONResponse # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
from fastapi import WebSocket
from mining_state import mining_state
import asyncio


# import routers (existing)
from routes import bl0ckchain_routes, difficulty_routes, mining_routes, log_routes
from contracts import ErrorResponse, StatusResponse, success_response

# use singleton blockchain instance you've already created
from singleton import blockchain
from bl0ckchain.mining import get_mining_backend_capabilities, get_mining_timeout

app = FastAPI(title="The bl0ck 🔗 API")
api_v1_router = APIRouter(prefix="/api/v1")

# CORS - development-friendly (tighten origin list in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _normalize_http_error(status_code: int, detail: object) -> dict[str, object]:
    if isinstance(detail, dict):
        code = str(detail.get("code") or f"HTTP_{status_code}")
        message = str(detail.get("message") or "Request failed")
        details = detail.get("details")
    elif isinstance(detail, str):
        code = f"HTTP_{status_code}"
        message = detail
        details = None
    else:
        code = f"HTTP_{status_code}"
        message = "Request failed"
        details = detail

    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details,
        },
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    _ = request
    content = _normalize_http_error(exc.status_code, exc.detail)
    return JSONResponse(status_code=exc.status_code, content=content)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    _ = request
    content = {
        "success": False,
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Request validation failed",
            "details": exc.errors(),
        },
    }
    return JSONResponse(status_code=422, content=content)


# register routers (versioned API)
api_v1_router.include_router(bl0ckchain_routes.router, prefix="/blockchain")
api_v1_router.include_router(difficulty_routes.router, prefix="/difficulty")
api_v1_router.include_router(mining_routes.router, prefix="/mining")
api_v1_router.include_router(log_routes.router)

# status endpoint for frontend initialization
@api_v1_router.get("/status", response_model=StatusResponse, responses={400: {"model": ErrorResponse}, 422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
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
    difficulty = getattr(blockchain, "get_effective_difficulty", lambda: 1)()
    failed = getattr(blockchain.difficulty_adjuster, "failed_difficulty", None)

    return success_response(
        "Status fetched",
        {
            "ddm_enabled": ddm_enabled,
            "ddm_mode": ddm_mode,
            "timeout": timeout,
            "difficulty": difficulty,
            "failed_difficulty": failed,
            "mining_backend": get_mining_backend_capabilities(),
        },
    )


app.include_router(api_v1_router)

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