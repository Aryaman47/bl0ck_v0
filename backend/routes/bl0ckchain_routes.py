# bl0ckchain_routes.py
from fastapi import APIRouter, HTTPException
from singleton import blockchain  # <-- Use the shared instance
from bl0ckchain.display import display_chain, last_block

router = APIRouter()

@router.get("/")
async def get_blockchain():
    chain_data = display_chain(blockchain.chain)
    if not chain_data:
        raise HTTPException(status_code=404, detail="Blockchain is empty")
    return {"blockchain": chain_data}

@router.post("/add")
async def add_block():
    new_block = blockchain.add_block()
    if new_block is None:
        return {
            "error": "❌ Block mining failed due to timeout!",
            "failed_difficulty": blockchain.difficulty_adjuster.failed_difficulty,
        }
    return {
        "message": "✅ Block added successfully!",
        "mining_time": new_block.mining_time,
        "difficulty": new_block.difficulty,
    }

@router.get("/last-block")
async def get_last_block():
    block = last_block(blockchain.chain)
    if block is None:
        raise HTTPException(status_code=404, detail="Blockchain is empty")
    return block
