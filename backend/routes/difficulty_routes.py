from fastapi import APIRouter, HTTPException
from singleton import blockchain
from contracts import DifficultyStateResponse, ErrorResponse, success_response

router = APIRouter()



# Get Current Difficulty + Mode

@router.get("/current", response_model=DifficultyStateResponse, responses={400: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
async def get_current_difficulty():
    return success_response(
        "Difficulty state fetched",
        {
            "mode": "manual" if blockchain.manual_mode else "automatic",
            "current_difficulty": blockchain.get_effective_difficulty(),
        },
    )



# Enable Manual Mode

@router.put("/manual/{difficulty}", response_model=DifficultyStateResponse, responses={400: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
async def set_manual_difficulty(difficulty: int):
    if difficulty < 1 or difficulty > 10:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_DIFFICULTY",
                "message": "Invalid difficulty. Please enter a number between 1 and 10.",
                "details": {
                    "min": 1,
                    "max": 10,
                    "provided": difficulty,
                },
            },
        )

    blockchain.set_manual_difficulty(difficulty)

    return success_response(
        f"Manual mode enabled. Difficulty set to {difficulty}.",
        {
            "mode": "manual",
            "current_difficulty": blockchain.get_effective_difficulty(),
        },
    )



# Switch Back to Automatic Mode

@router.put("/auto", response_model=DifficultyStateResponse, responses={400: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
async def switch_to_auto_mode():
    if not blockchain.manual_mode:
        return success_response(
            "Already in Automatic Mode.",
            {
                "mode": "automatic",
                "current_difficulty": blockchain.get_effective_difficulty(),
            },
        )

    blockchain.switch_to_auto_mode()

    return success_response(
        "Switched to Automatic Mode.",
        {
            "mode": "automatic",
            "current_difficulty": blockchain.get_effective_difficulty(),
        },
    )
