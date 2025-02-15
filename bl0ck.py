import hashlib
import datetime
import json
import os
import time
from difficulty import DifficultyAdjuster  # Import difficulty module

class Block:
    def __init__(self, index, timestamp, data, previous_hash, difficulty=1, nonce=0, mining_time=None):
        self.index = index
        self.timestamp = timestamp if isinstance(timestamp, str) else str(datetime.datetime.now())
        self.data = data
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.nonce = nonce
        self.mining_time = mining_time  # Stores the time taken to mine the block
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = (
            str(self.index) + str(self.timestamp) + str(self.data) +
            str(self.previous_hash) + str(self.nonce)
        )
        return hashlib.sha256(block_data.encode()).hexdigest()

    def mine_block(self, timeout_limit=30):
        """
        Mines the block by finding a hash with required leading zeroes based on difficulty.
        Includes a timeout mechanism to handle excessive mining time.
        """
        target_prefix = '0' * self.difficulty
        start_time = time.time()

        while not self.hash.startswith(target_prefix):
            self.nonce += 1
            self.hash = self.calculate_hash()

            # Timeout check
            if time.time() - start_time > timeout_limit:
                return None, time.time() - start_time  # Mining failed due to timeout

        return self.hash, time.time() - start_time  # Successful mining

class Blockchain:
    def __init__(self):
        self.file_name = "blockchain_data.json"
        self.chain = self.load_from_file()
        self.dynamic_difficulty_enabled = False  # Default: Standard Mode
        self.manual_mode = False  # Tracks if manual difficulty is active
        self.difficulty_adjuster = DifficultyAdjuster(target_block_time=10, adjustment_interval=5)

        if not self.chain:
            self.chain = [self.create_genesis_block()]
            self.save_to_file()

    def create_genesis_block(self):
        return Block(0, str(datetime.datetime.now()), "Genesis Block", "0", difficulty=1)

    def enable_dynamic_difficulty(self):
        self.dynamic_difficulty_enabled = True
        self.manual_mode = False  # Ensure it starts in automatic mode
        print("\n⚡ Dynamic Difficulty Mode Enabled! (Automatic Mode)")

    def disable_dynamic_difficulty(self):
        self.dynamic_difficulty_enabled = False
        self.manual_mode = False
        print("\n🔄 Reverted to Standard Mode (bl0ck v0).")

    def set_manual_difficulty(self, difficulty):
        """Allows the user to manually set difficulty when DDM is enabled."""
        if 1 <= difficulty <= 10:
            self.difficulty_adjuster.difficulty = difficulty
            self.manual_mode = True  # Switch to manual mode
            print(f"✅ Manual Difficulty Set: {difficulty} (DDM in Manual Mode)")
        else:
            print("⚠️ Invalid input! Please enter a difficulty between 1 and 10.")

    def switch_to_auto_mode(self):
        """Switches back to automatic difficulty adjustment in DDM."""
        if not self.manual_mode:
            print("⚠️ Already in Automatic Mode!")
            return

        self.manual_mode = False
        print("🔄 Switching back to Automatic Difficulty Adjustment!")

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
            new_block.hash, mining_time = new_block.mine_block()
            new_block.mining_time = round(mining_time, 2)

            if new_block.hash is None:
                print(f"❌ Mining failed! Difficulty {difficulty} exceeded the timeout.")
                self.difficulty_adjuster.failed_difficulty = difficulty  # Store failed difficulty
                return

            self.difficulty_adjuster.record_block_time(start_time)
            new_difficulty = self.difficulty_adjuster.adjust_difficulty()
            print(f"⏳ Mining Time: {new_block.mining_time}s | New Difficulty: {new_difficulty}")

        self.chain.append(new_block)
        self.save_to_file()
        print(f"\n✅ Block {new_block.index} added! Difficulty: {new_block.difficulty}")

    def retry_failed_mining(self):
        """Retries mining with the last failed difficulty level if available."""
        if not self.dynamic_difficulty_enabled:
            print("⚠️ Enable Dynamic Difficulty Mode first!")
            return

        if self.difficulty_adjuster.failed_difficulty is None:
            print("⚠️ No failed difficulty recorded.")
            return

        print(f"\n🔄 Retrying with Difficulty {self.difficulty_adjuster.failed_difficulty}...")
        self.difficulty_adjuster.difficulty = self.difficulty_adjuster.failed_difficulty
        self.difficulty_adjuster.failed_difficulty = None  # Reset after retry
        self.add_block()

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
                                block.get("nonce", 0),
                                block.get("mining_time", None)
                            )
                            for block in data
                        ]
                except json.JSONDecodeError:
                    pass
        return []

    def display_chain(self):
        print("\n🔗 Blockchain Data:")
        for block in self.chain:
            print(f"\nIndex: {block.index} | Time: {block.mining_time}s")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.data}")
            print(f"Difficulty: {block.difficulty}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")
            print("-" * 40)

    def last_block(self):
        print(f"\nIndex: {self.chain[-1].index} | Time: {self.chain[-1].mining_time}s")
        print(f"Timestamp: {self.chain[-1].timestamp}")
        print(f"Data: {self.chain[-1].data}")
        print(f"Difficulty: {self.chain[-1].difficulty}")
        print(f"Previous Hash: {self.chain[-1].previous_hash}") 
        print(f"Hash: {self.chain[-1].hash}")