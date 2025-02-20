from fastapi import APIRouter
from backend.bl0ckchain.bl0ckchain import Blockchain

router = APIRouter()
blockchain = Blockchain()

@router.get("/")
async def get_blockchain():
    """Fetch the entire blockchain."""
    return {"blockchain": [block.dict() for block in blockchain.chain]}

@router.post("/add")
async def add_block():
    """Add a new block to the blockchain."""
    blockchain.add_block()
    return {"message": "Block added successfully!"}
