from fastapi import APIRouter, HTTPException
from singleton import blockchain
from contracts import DifficultyStateResponse, ErrorResponse, success_response

router = APIRouter()



# Get Current Difficulty + Mode

@router.get("/current", response_model=DifficultyStateResponse, responses={400: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
async def get_current_difficulty():
    configured = blockchain.difficulty_adjuster.difficulty
    effective = blockchain.get_effective_difficulty()
    return success_response(
        "Difficulty state fetched",
        {
            "mode": "manual" if blockchain.manual_mode else "automatic",
            "configured_difficulty": configured,
            "effective_difficulty": effective,
            "current_difficulty": effective,
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
    configured = blockchain.difficulty_adjuster.difficulty
    effective = blockchain.get_effective_difficulty()

    return success_response(
        f"Manual mode enabled. Difficulty set to {difficulty}.",
        {
            "mode": "manual",
            "configured_difficulty": configured,
            "effective_difficulty": effective,
            "current_difficulty": effective,
        },
    )



# Switch Back to Automatic Mode

@router.put("/auto", response_model=DifficultyStateResponse, responses={400: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
async def switch_to_auto_mode():
    if not blockchain.manual_mode:
        configured = blockchain.difficulty_adjuster.difficulty
        effective = blockchain.get_effective_difficulty()
        return success_response(
            "Already in Automatic Mode.",
            {
                "mode": "automatic",
                "configured_difficulty": configured,
                "effective_difficulty": effective,
                "current_difficulty": effective,
            },
        )

    blockchain.switch_to_auto_mode()
    configured = blockchain.difficulty_adjuster.difficulty
    effective = blockchain.get_effective_difficulty()

    return success_response(
        "Switched to Automatic Mode.",
        {
            "mode": "automatic",
            "configured_difficulty": configured,
            "effective_difficulty": effective,
            "current_difficulty": effective,
        },
    )
