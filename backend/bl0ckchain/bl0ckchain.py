from .bl0ck import Block
from .mining import mine_block
from .storage import save_to_file, load_from_file
from backend.difficulty import DifficultyAdjuster
import datetime
import time

class Blockchain:
    def __init__(self):
        self.chain = load_from_file()
        self.dynamic_difficulty_enabled = False
        self.manual_mode = False
        self.difficulty_adjuster = DifficultyAdjuster(target_block_time=10, adjustment_interval=5)

        if not self.chain:
            self.chain = [self.create_genesis_block()]
            save_to_file(self.chain)

    def create_genesis_block(self):
        return Block(0, str(datetime.datetime.now()), "Genesis Block", "0", difficulty=1)

    def enable_dynamic_difficulty(self):
        self.dynamic_difficulty_enabled = True
        self.manual_mode = False
        print("\n⚡ Dynamic Difficulty Mode Enabled! (Automatic Mode)")

    def disable_dynamic_difficulty(self):
        self.dynamic_difficulty_enabled = False
        self.manual_mode = False
        print("\n🔄 Reverted to Standard Mode (bl0ck v0).")

    def set_manual_difficulty(self, difficulty):
        if 1 <= difficulty <= 10:
            self.difficulty_adjuster.difficulty = difficulty
            self.manual_mode = True
            print(f"✅ Manual Difficulty Set: {difficulty} (DDM in Manual Mode)")
        else:
            print("⚠️ Invalid input! Please enter a difficulty between 1 and 10.")

    def switch_to_auto_mode(self):
        if not self.manual_mode:
            print("⚠️ Already in Automatic Mode!")
            return

        self.manual_mode = False
        print("🔄 Switching back to Automatic Difficulty Adjustment!")

        # If a failure occurred, start from a reduced difficulty
        if self.difficulty_adjuster.failed_difficulty:
            new_difficulty = max(1, self.difficulty_adjuster.failed_difficulty - 1)
            self.difficulty_adjuster.difficulty = new_difficulty
            print(f"🔄 Adjusting difficulty to {new_difficulty} due to previous failure.")

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
            new_block.hash, mining_time = mine_block(new_block)
            new_block.mining_time = round(mining_time, 2)

            if new_block.hash is None:
                print(f"❌ [DEBUG] Mining failed! Difficulty {difficulty} exceeded timeout.")
                self.difficulty_adjuster.failed_difficulty = difficulty
                return  # Ensure function exits, preventing further processing

            self.difficulty_adjuster.record_block_time(new_block.mining_time)
            new_difficulty = self.difficulty_adjuster.adjust_difficulty()
            print(f"⏳ [DEBUG] Mining Time: {new_block.mining_time}s | Adjusted Difficulty: {new_difficulty}")

            # If previous failure was recorded and block was mined successfully, try increasing difficulty
            if self.difficulty_adjuster.failed_difficulty:
                if difficulty < self.difficulty_adjuster.failed_difficulty:
                    self.difficulty_adjuster.difficulty += 1  # Try increasing difficulty
                    print(f"🔼 Increasing difficulty to {self.difficulty_adjuster.difficulty}.")

        self.chain.append(new_block)
        save_to_file(self.chain)
        print(f"\n✅ Block {new_block.index} added! Difficulty: {new_block.difficulty}")

        return new_block
