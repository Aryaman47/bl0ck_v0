from fastapi import APIRouter
from backend.difficulty import DifficultyAdjuster

router = APIRouter()
difficulty_adjuster = DifficultyAdjuster()

@router.post("/set-manual/{difficulty}")
async def set_manual_difficulty(difficulty: int):
    """Set difficulty manually."""
    difficulty_adjuster.difficulty = difficulty
    return {"message": f"Manual difficulty set to {difficulty}."}

@router.post("/enable-dynamic")
async def enable_dynamic_difficulty():
    """Enable dynamic difficulty mode."""
    difficulty_adjuster.failed_difficulty = None  # Reset failed difficulty tracking
    return {"message": "Dynamic Difficulty Mode enabled."}

@router.post("/disable-dynamic")
async def disable_dynamic_difficulty():
    """Disable dynamic difficulty mode."""
    return {"message": "Reverted to standard mode."}

@router.post("/switch-to-auto")
async def switch_to_auto_mode():
    """Switch back to automatic difficulty adjustment."""
    difficulty_adjuster.failed_difficulty = None
    return {"message": "Switched to Automatic Mode."}
