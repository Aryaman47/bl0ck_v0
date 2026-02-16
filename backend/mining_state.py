import time
from threading import Lock

class MiningState:
    def __init__(self):
        self.lock = Lock()
        self.reset()

    def reset(self):
        with self.lock:
            self.active = False
            self.start_time = None
            self.current_nonce = 0
            self.difficulty = 0
            self.hash_rate = 0

    def start(self, difficulty):
        with self.lock:
            self.active = True
            self.start_time = time.time()
            self.current_nonce = 0
            self.difficulty = difficulty
            self.hash_rate = 0

    def update(self, nonce):
        with self.lock:
            self.current_nonce = nonce
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                self.hash_rate = nonce / elapsed

    def stop(self):
        with self.lock:
            self.active = False

    def snapshot(self):
        with self.lock:
            elapsed = 0
            if self.start_time:
                elapsed = time.time() - self.start_time

            return {
                "active": self.active,
                "elapsed": round(elapsed, 2),
                "nonce": self.current_nonce,
                "difficulty": self.difficulty,
                "hash_rate": round(self.hash_rate, 2)
            }

mining_state = MiningState()
