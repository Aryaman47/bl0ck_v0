import time
from .bl0ck import Block

def mine_block(block, timeout_limit=60):
    target_prefix = '0' * block.difficulty
    start_time = time.time()

    while not block.hash.startswith(target_prefix):
        block.nonce += 1
        block.hash = block.calculate_hash()

        if time.time() - start_time > timeout_limit:
            return None, time.time() - start_time  # Mining failed

    return block.hash, time.time() - start_time