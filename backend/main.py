from fastapi import FastAPI, HTTPException
from bl0ckchain.bl0ckchain import Blockchain
from bl0ckchain.display import display_chain, last_block
from bl0ckchain.mining import set_mining_timeout
from difficulty import DifficultyAdjuster

app = FastAPI(title="The bl0ck 🔗 API")

# Initialize Blockchain and Difficulty Adjuster
blockchain = Blockchain()
difficulty_adjuster = DifficultyAdjuster()

@app.get("/")
async def root():
    """Welcome message"""
    return {"message": "Welcome to The bl0ck 🔗 API"}

@app.get("/blockchain")
async def get_blockchain():
    """Fetch the entire blockchain."""
    chain_data = display_chain(blockchain.chain)  # Updated function call
    if not chain_data:
        raise HTTPException(status_code=404, detail="Blockchain is empty")
    return {"blockchain": chain_data}
@app.post("/blockchain/add")
async def add_block():
    """Add a new block to the blockchain."""
    new_block = blockchain.add_block()  # Store the block

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


@app.get("/blockchain/last-block")
async def get_last_block():
    """Get the last block in the blockchain."""
    block = last_block(blockchain.chain)  # Updated function call
    if block is None:
        raise HTTPException(status_code=404, detail="Blockchain is empty")
    return block

@app.post("/difficulty/enable")
async def enable_dynamic_difficulty():
    """Enable Dynamic Difficulty Mode (Auto Mode by default)."""
    if blockchain.dynamic_difficulty_enabled:
        return {"message": "⚠️ DDM is already enabled!"}
    blockchain.enable_dynamic_difficulty()
    return {"message": "✅ Dynamic Difficulty Mode enabled."}

@app.post("/difficulty/disable")
async def disable_dynamic_difficulty():
    """Revert to Standard Mode (bl0ck v0)."""
    if not blockchain.dynamic_difficulty_enabled:
        return {"message": "⚠️ DDM is already in Standard Mode!"}
    blockchain.disable_dynamic_difficulty()
    return {"message": "🔄 Exiting to Standard Mode, DDM is disabled."}

@app.post("/difficulty/set-manual/{difficulty}")
async def set_manual_difficulty(difficulty: int):
    """Set manual difficulty (Only in DDM)."""
    if not blockchain.dynamic_difficulty_enabled:
        raise HTTPException(status_code=400, detail="⚠️ Dynamic Difficulty Mode is not enabled! Enable DDM first.")
    if difficulty < 1 or difficulty > 10:
        raise HTTPException(status_code=400, detail="❌ Invalid difficulty! Please enter a number between 1 and 10.")
    blockchain.set_manual_difficulty(difficulty)
    return {"message": f"Manual difficulty set to {difficulty}."}

@app.post("/difficulty/switch-to-auto")
async def switch_to_auto_mode():
    """Switch back to Auto Mode (Only in DDM)."""
    if not blockchain.dynamic_difficulty_enabled:
        raise HTTPException(status_code=400, detail="⚠️ Dynamic Difficulty Mode is not enabled!")
    blockchain.switch_to_auto_mode()
    return {"message": "🔄 Switched back to Auto Mode."}

@app.post("/mining/set-timeout/{timeout}")
async def update_mining_timeout(timeout: int):
    """Set a custom mining timeout."""
    if timeout < 10 or timeout > 300:
        raise HTTPException(status_code=400, detail="❌ Invalid timeout! Please set a value between 10 and 300 seconds.")
    set_mining_timeout(timeout)
    return {"message": f"Mining timeout set to {timeout} seconds."}
