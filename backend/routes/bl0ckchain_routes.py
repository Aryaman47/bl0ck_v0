# backend/routes/bl0ckchain_routes.py
from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from singleton import blockchain  # <-- Use the shared instance
from bl0ckchain.display import display_chain, last_block
from contracts import (
    AddBlockResponse,
    BlockchainDisplayResponse,
    BlockchainStatusResponse,
    ErrorResponse,
    LastBlockResponse,
    success_response,
)

router = APIRouter()

@router.get("/status", response_model=BlockchainStatusResponse, responses={404: {"model": ErrorResponse}, 408: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
async def root():
    return success_response(
        "Blockchain route status",
        {"message": "Welcome to the bl0ckchain API! Use /display to see the blockchain and /add to mine a new block."},
    )

@router.get("/display", response_model=BlockchainDisplayResponse, responses={404: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
async def get_blockchain():
    chain_data = display_chain(blockchain.chain)
    if not chain_data:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "BLOCKCHAIN_EMPTY",
                "message": "Blockchain is empty",
            },
        )
    return success_response("Blockchain fetched", {"blockchain": chain_data})

@router.post("/add", response_model=AddBlockResponse, responses={404: {"model": ErrorResponse}, 408: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
async def add_block():
    new_block = await run_in_threadpool(blockchain.add_block)  # Run the blocking mining operation in a thread
    if new_block is None:
        raise HTTPException(
            status_code=408,
            detail={
                "code": "MINING_TIMEOUT",
                "message": "Block mining failed due to timeout",
                "details": {
                    "failed_difficulty": blockchain.difficulty_adjuster.failed_difficulty,
                },
            },
        )
    return success_response(
        "Block added successfully",
        {
            "mining_time": new_block.mining_time,
            "difficulty": new_block.difficulty,
        },
    )

@router.get("/last-block", response_model=LastBlockResponse, responses={404: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
async def get_last_block():
    block = last_block(blockchain.chain)
    if block is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "BLOCKCHAIN_EMPTY",
                "message": "Blockchain is empty",
            },
        )
    return success_response("Last block fetched", block)
