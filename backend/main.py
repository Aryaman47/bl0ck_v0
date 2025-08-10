# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import bl0ckchain_routes, difficulty_routes, mining_routes

app = FastAPI(title="The bl0ck 🔗 API")

# Enable CORS for the frontend. For production, lock this down to exact origins.
origins = [
    "http://127.0.0.1:8000",      # when served by the same host
    "http://localhost:8000",
    "http://127.0.0.1:5500",      # optional if you serve via local dev server
    "http://localhost:5500",
    "*"                           # development convenience; remove in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register modular routers with prefixes
app.include_router(bl0ckchain_routes.router, prefix="/blockchain")
app.include_router(difficulty_routes.router, prefix="/difficulty")
app.include_router(mining_routes.router, prefix="/mining")

# Serve the frontend (static files) from the 'frontend' directory.
# This mounts the frontend at the root path.
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
