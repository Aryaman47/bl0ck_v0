# main.py
from fastapi import FastAPI
from routes import bl0ckchain_routes, difficulty_routes, mining_routes

app = FastAPI(title="The bl0ck 🔗 API")

# Register modular routers with prefixes
app.include_router(bl0ckchain_routes.router, prefix="/blockchain")
app.include_router(difficulty_routes.router, prefix="/difficulty")
app.include_router(mining_routes.router, prefix="/mining")

@app.get("/")
async def root():
    """Welcome message"""
    return {"message": "Welcome to The bl0ck 🔗 API"}
