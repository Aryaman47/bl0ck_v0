# backend/bl0ckchain/mining.py
import time
from .bl0ck import Block
from logger import logger
# Default timeout value (in seconds)
timeout_limit = 60


def mine_block(block: Block, timeout=None):
    """
    Mine the given block.

    If `timeout` is provided, use it for this mining attempt;
    otherwise use the global timeout_limit.

    Returns:
        (hash or None, mining_time_seconds)
    """

    global timeout_limit

    if timeout is None:
        timeout = timeout_limit

    target_prefix = '0' * block.difficulty
    start_time = time.time()

    # 🔹 Reset nonce before mining attempt
    block.nonce = 0

    while True:
        block.hash = block.calculate_hash()

        if block.hash.startswith(target_prefix):
            block.mining_time = time.time() - start_time
            return block.hash, block.mining_time

        block.nonce += 1

        # Timeout check (optimized)
        if time.time() - start_time > timeout:
            block.mining_time = time.time() - start_time
            return None, block.mining_time

    block.mining_time = time.time() - start_time  # Store successful mining duration
    return block.hash, block.mining_time

def set_mining_timeout(timeout):
    """Allows users to set a manual timeout limit."""
    global timeout_limit
    if timeout > 0:
        timeout_limit = timeout
        print(f"⏳ Mining timeout set to {timeout} seconds.")
        logger.info(f"Mining timeout updated to {timeout} seconds.")
    else:
        print("⚠️ Invalid timeout! Please enter a positive number.")

def get_mining_timeout():
    """Return the current mining timeout (global session value)."""
    return timeout_limit
