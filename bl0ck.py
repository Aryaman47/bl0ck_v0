import hashlib
import datetime
import json
import os
import time
from difficulty import DifficultyAdjuster  # Import difficulty module (external file)

class Block:
    def __init__(self, index, timestamp, data, previous_hash, difficulty=1, nonce=0):
        self.index = index
        self.timestamp = timestamp if isinstance(timestamp, str) else str(datetime.datetime.now())
        self.data = data
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = (
            str(self.index) + str(self.timestamp) + str(self.data) +
            str(self.previous_hash) + str(self.nonce)
        )
        return hashlib.sha256(block_data.encode()).hexdigest()

    def mine_block(self):
        """
        Mines the block by finding a hash with required leading zeroes based on difficulty.
        """
        target_prefix = '0' * self.difficulty
        while not self.hash.startswith(target_prefix):
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.file_name = "blockchain_data.json"
        self.chain = self.load_from_file()
        self.dynamic_difficulty_enabled = False  # Default: Standard Mode
        self.difficulty_adjuster = DifficultyAdjuster(target_block_time=10, adjustment_interval=5)

        if not self.chain:
            self.chain = [self.create_genesis_block()]
            self.save_to_file()

    def create_genesis_block(self):
        return Block(0, str(datetime.datetime.now()), "Genesis Block", "0", difficulty=1)

    def enable_dynamic_difficulty(self):
        self.dynamic_difficulty_enabled = True
        print("\n⚡ Dynamic Difficulty Mode Enabled!")

    def disable_dynamic_difficulty(self):
        self.dynamic_difficulty_enabled = False
        print("\n🔄 Reverted to Standard Mode (bl0ck v0).")

    def add_block(self):
        last_block = self.chain[-1]
        start_time = time.time()

        difficulty = (
            self.difficulty_adjuster.difficulty if self.dynamic_difficulty_enabled else 1
        )

        new_block = Block(
            index=last_block.index + 1,
            timestamp=str(datetime.datetime.now()),
            data=f"Block {last_block.index + 1}",
            previous_hash=last_block.hash,
            difficulty=difficulty
        )

        if self.dynamic_difficulty_enabled:
            new_block.mine_block()
            mining_duration = time.time() - start_time
            self.difficulty_adjuster.record_block_time(start_time)
            new_difficulty = self.difficulty_adjuster.adjust_difficulty()
            print(f"⏳ Mining Time: {round(mining_duration, 2)}s | New Difficulty: {new_difficulty}")

        self.chain.append(new_block)
        self.save_to_file()
        print(f"\n✅ Block {new_block.index} added! Difficulty: {new_block.difficulty}")

    def save_to_file(self):
        with open(self.file_name, "w") as file:
            json.dump([block.__dict__ for block in self.chain], file, indent=4)

    def load_from_file(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as file:
                try:
                    data = json.load(file)
                    if data:
                        return [
                            Block(
                                block["index"],
                                block["timestamp"],
                                block["data"],
                                block["previous_hash"],
                                block.get("difficulty", 1),
                                block.get("nonce", 0)
                            )
                            for block in data
                        ]
                except json.JSONDecodeError:
                    pass
        return []

    def display_chain(self):
        print("\n🔗 Blockchain Data:")
        for block in self.chain:
            print(f"\nIndex: {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.data}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")
            print(f"Difficulty: {block.difficulty}")
            print(f"Nonce: {block.nonce}")
            print("-" * 40)
