import hashlib
import datetime


class Block:
    def __init__(self, index, timestamp, data, previous_hash, difficulty=1, nonce=0, mining_time=None):
        self.index = index

        # Ensure consistent timestamp formatting
        if isinstance(timestamp, datetime.datetime):
            self.timestamp = timestamp.isoformat()
        elif isinstance(timestamp, str):
            self.timestamp = timestamp
        else:
            self.timestamp = datetime.datetime.now().isoformat()

        self.data = data
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.nonce = nonce
        self.mining_time = mining_time

        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = (
            str(self.index) +
            str(self.timestamp) +
            str(self.data) +
            str(self.previous_hash) +
            str(self.difficulty) +  # Include difficulty
            str(self.nonce)
        )

        return hashlib.sha256(block_data.encode()).hexdigest()
