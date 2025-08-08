#difficulty_routes.py
from fastapi import APIRouter, HTTPException
from singleton import blockchain  # <-- Use the shared instance

router = APIRouter()

@router.post("/enable")
async def enable_dynamic_difficulty():
    if blockchain.dynamic_difficulty_enabled:
        return {"message": "⚠️ DDM is already enabled!"}
    blockchain.enable_dynamic_difficulty()
    return {"message": "✅ Dynamic Difficulty Mode enabled."}

@router.post("/disable")
async def disable_dynamic_difficulty():
    if not blockchain.dynamic_difficulty_enabled:
        return {"message": "⚠️ DDM is already in Standard Mode!"}
    blockchain.disable_dynamic_difficulty()
    return {"message": "🔄 Exiting to Standard Mode, DDM is disabled."}

@router.post("/set-manual/{difficulty}")
async def set_manual_difficulty(difficulty: int):
    if not blockchain.dynamic_difficulty_enabled:
        raise HTTPException(status_code=400, detail="⚠️ Dynamic Difficulty Mode is not enabled! Enable DDM first.")
    if difficulty < 1 or difficulty > 10:
        raise HTTPException(status_code=400, detail="❌ Invalid difficulty! Please enter a number between 1 and 10.")
    blockchain.set_manual_difficulty(difficulty)
    return {"message": f"Manual difficulty set to {difficulty}."}

@router.post("/switch-to-auto")
async def switch_to_auto_mode():
    if not blockchain.dynamic_difficulty_enabled:
        raise HTTPException(status_code=400, detail="⚠️ Dynamic Difficulty Mode is not enabled!")
    blockchain.switch_to_auto_mode()
    return {"message": "🔄 Switched back to Auto Mode."}
