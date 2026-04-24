import time

from bl0ckchain.bl0ck import Block
from mining_state import MiningState

from .base_backend import MiningBackend


class CpuMiningBackend(MiningBackend):
    name = "cpu"

    def mine(self, block: Block, timeout: int, mining_state: MiningState):
        target_prefix = "0" * block.difficulty
        start_time = time.time()

        block.nonce = 0
        mining_state.start(block.difficulty, backend=self.name)

        try:
            while True:
                block.hash = block.calculate_hash()

                if block.hash.startswith(target_prefix):
                    block.mining_time = time.time() - start_time
                    return block.hash, block.mining_time

                block.nonce += 1
                mining_state.update(block.nonce)

                if time.time() - start_time > timeout:
                    block.mining_time = time.time() - start_time
                    return None, block.mining_time
        finally:
            mining_state.stop()
