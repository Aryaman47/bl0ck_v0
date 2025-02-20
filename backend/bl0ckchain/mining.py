import time
from .bl0ck import Block

# Default timeout value
timeout_limit = 60  

def mine_block(block):
    global timeout_limit
    target_prefix = '0' * block.difficulty
    start_time = time.time()

    while not block.hash.startswith(target_prefix):
        block.nonce += 1
        block.hash = block.calculate_hash()

        if time.time() - start_time > timeout_limit:
            block.mining_time = time.time() - start_time  # Store mining failure duration
            return None, block.mining_time  # Mining failed due to timeout

    block.mining_time = time.time() - start_time  # Store successful mining duration
    return block.hash, block.mining_time

def set_mining_timeout(timeout):
    """Allows users to set a manual timeout limit."""
    global timeout_limit
    if timeout > 0:
        timeout_limit = timeout
        print(f"⏳ Mining timeout set to {timeout} seconds.")
    else:
        print("⚠️ Invalid timeout! Please enter a positive number.")
