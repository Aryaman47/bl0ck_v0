# backend/routes/mining_routes.py
from fastapi import APIRouter, HTTPException
from bl0ckchain.mining import (
    get_mining_backend_capabilities,
    set_mining_backend,
    set_mining_timeout,
)
from contracts import ErrorResponse, MiningBackendResponse, MiningTimeoutResponse, success_response

router = APIRouter()


@router.get("/backend", response_model=MiningBackendResponse, responses={422: {"model": ErrorResponse}})
async def get_backend_mode():
    return success_response(
        "Mining backend status fetched.",
        get_mining_backend_capabilities(),
    )


@router.post("/backend/{backend_name}", response_model=MiningBackendResponse, responses={400: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
async def set_backend_mode(backend_name: str):
    try:
        set_mining_backend(backend_name)
    except ValueError:
        capabilities = get_mining_backend_capabilities()
        raise HTTPException(
            status_code=400,
            detail={
                "code": "UNSUPPORTED_BACKEND",
                "message": f"Unsupported backend '{backend_name}'.",
                "details": {
                    "supported_modes": capabilities["supported_modes"],
                    "available_backends": capabilities["available_backends"],
                },
            },
        )

    return success_response(
        f"Mining backend switched to {backend_name}.",
        get_mining_backend_capabilities(),
    )

@router.put("/timeout/{timeout}", response_model=MiningTimeoutResponse, responses={400: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
async def update_mining_timeout(timeout: int):
    if timeout < 10 or timeout > 300:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_TIMEOUT",
                "message": "Invalid timeout. Please set a value between 10 and 300 seconds.",
                "details": {
                    "min": 10,
                    "max": 300,
                    "provided": timeout,
                },
            },
        )
    set_mining_timeout(timeout)
    return success_response(
        f"Mining timeout set to {timeout} seconds.",
        {"timeout": timeout},
    )