from fastapi import APIRouter, HTTPException
from singleton import blockchain

router = APIRouter()



# Get Current Difficulty + Mode

@router.get("/current")
async def get_current_difficulty():
    return {
        "mode": "manual" if blockchain.manual_mode else "automatic",
        "current_difficulty": blockchain.difficulty_adjuster.difficulty
    }



# Enable Manual Mode

@router.post("/set-manual/{difficulty}")
async def set_manual_difficulty(difficulty: int):
    if difficulty < 1 or difficulty > 10:
        raise HTTPException(
            status_code=400,
            detail="Invalid difficulty. Please enter a number between 1 and 10."
        )

    blockchain.set_manual_difficulty(difficulty)

    return {
        "message": f"Manual mode enabled. Difficulty set to {difficulty}.",
        "mode": "manual",
        "current_difficulty": blockchain.difficulty_adjuster.difficulty
    }



# Switch Back to Automatic Mode

@router.post("/switch-to-auto")
async def switch_to_auto_mode():
    if not blockchain.manual_mode:
        return {
            "message": "Already in Automatic Mode.",
            "mode": "automatic",
            "current_difficulty": blockchain.difficulty_adjuster.difficulty
        }

    blockchain.switch_to_auto_mode()

    return {
        "message": "Switched to Automatic Mode.",
        "mode": "automatic",
        "current_difficulty": blockchain.difficulty_adjuster.difficulty
    }
