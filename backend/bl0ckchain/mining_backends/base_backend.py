from abc import ABC, abstractmethod

from mining_state import MiningState
from bl0ckchain.bl0ck import Block


class MiningBackend(ABC):
    name = "base"

    @abstractmethod
    def mine(self, block: Block, timeout: int, mining_state: MiningState):
        """Mine a block and return (hash_or_none, mining_time_seconds)."""
        raise NotImplementedError()
