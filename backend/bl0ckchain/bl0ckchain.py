# bl0ckchain.py
from .bl0ck import Block
from .mining import mine_block, get_mining_timeout #, set_mining_timeout
from .storage import save_to_file, load_from_file
from difficulty import DifficultyAdjuster
import datetime
#import time

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
            self.difficulty_adjuster.set_difficulty(difficulty)
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

        if self.difficulty_adjuster.failed_difficulty:
            new_diff = max(1, self.difficulty_adjuster.failed_difficulty - 1)
            self.difficulty_adjuster.set_difficulty(new_diff)
            print(f"🔄 Adjusting difficulty to {new_diff} due to previous failure.")

    def add_block(self):
        last_block = self.chain[-1]
        base_difficulty = (
            self.difficulty_adjuster.difficulty
            if self.dynamic_difficulty_enabled or self.manual_mode
            else 1
        )

        # Check if difficulty is blocked by fail count blacklist
        max_allowed_diff = base_difficulty
        if self.difficulty_adjuster.blocked_thresholds:
            max_block = min(self.difficulty_adjuster.blocked_thresholds)
            if base_difficulty >= max_block:
                max_allowed_diff = max(1, max_block - 1)
                print(f"[DEBUG] Difficulty {base_difficulty} blocked, limiting to {max_allowed_diff}")

        current_timeout = get_mining_timeout()
        fail_count = self.difficulty_adjuster.get_failure_count(base_difficulty)

        # Function to attempt mining with a specific difficulty and timeout
        def attempt_mine(difficulty, timeout):
            block = Block(
                index=last_block.index + 1,
                timestamp=str(datetime.datetime.now()),
                data=f"Block {last_block.index + 1}",
                previous_hash=last_block.hash,
                difficulty=difficulty,
            )
            mined_hash, mining_time = mine_block(block, timeout)
            return block, mined_hash, mining_time

        # If fail count > 3 for this difficulty, try once with increased timeout before blacklisting
        if fail_count > 3:
            print(f"[DEBUG] FailCount > 3 for difficulty {base_difficulty}, increasing timeout and retrying")
            block, mined_hash, mining_time = attempt_mine(base_difficulty, current_timeout + 60)
            if mined_hash is None:
                # blacklist difficulty - do not allow increment to this or beyond
                self.difficulty_adjuster.block_from_difficulty(base_difficulty)
                # set current difficulty to base_difficulty -1 as upper limit
                new_diff = max(1, base_difficulty - 1)
                self.difficulty_adjuster.set_difficulty(new_diff)
                self.difficulty_adjuster.reset_failure_count(base_difficulty)
                print(f"[DEBUG] Blacklisting difficulty {base_difficulty}. Limiting max difficulty to {new_diff}.")
                return None  # fail without adding block
            else:
                # success with increased timeout, reset fail count and continue
                self.difficulty_adjuster.reset_failure_count(base_difficulty)
                block.mining_time = round(mining_time, 2)
                self.chain.append(block)
                save_to_file(self.chain)
                # difficulty stays same, no increment for next round
                print(f"\n✅ Block {block.index} added! Difficulty: {block.difficulty} (with increased timeout)")
                return block

        # Normal mining flow: try base difficulty, if fail decrement once and retry
        block, mined_hash, mining_time = attempt_mine(base_difficulty, current_timeout)
        if mined_hash is None:
            # Mining failed at base difficulty
            fail_count = self.difficulty_adjuster.increment_failure_count(base_difficulty)

            # Retry at one difficulty lower if possible
            retry_diff = max(1, base_difficulty - 1)
            print(f"[DEBUG] Mining failed at difficulty {base_difficulty}, retrying at {retry_diff} (FailCount={fail_count})")

            block_retry, mined_hash_retry, mining_time_retry = attempt_mine(retry_diff, current_timeout)
            if mined_hash_retry is None:
                # Fail again at retry difficulty, do NOT increment fail count again for retry difficulty
                print(f"[DEBUG] Mining also failed at retry difficulty {retry_diff}.")
                return None  # give up, do not add block

            else:
                # Retry succeeded: keep fail count for base difficulty, reset for retry difficulty if any
                self.difficulty_adjuster.reset_failure_count(retry_diff)
                block_retry.mining_time = round(mining_time_retry, 2)
                self.chain.append(block_retry)
                save_to_file(self.chain)

                # Keep fail count for base difficulty, but difficulty stays at base difficulty for next round (no increment)
                print(f"\n✅ Block {block_retry.index} added! Difficulty: {retry_diff} (Retry success, fail count kept at {fail_count})")

                # Keep difficulty at base difficulty for next call (do not increment to base_difficulty + 1)
                self.difficulty_adjuster.set_difficulty(base_difficulty)
                return block_retry

        else:
            # Mining succeeded at base difficulty
            block.mining_time = round(mining_time, 2)
            self.chain.append(block)
            save_to_file(self.chain)

            # Reset fail count on success for this difficulty
            self.difficulty_adjuster.reset_failure_count(base_difficulty)

            # Increment difficulty for next round, but respect blacklist limits
            new_difficulty = base_difficulty + 1
            if self.difficulty_adjuster.blocked_thresholds:
                min_block = min(self.difficulty_adjuster.blocked_thresholds)
                if new_difficulty >= min_block:
                    new_difficulty = max(1, min_block - 1)

            self.difficulty_adjuster.set_difficulty(new_difficulty)

            print(f"\n✅ Block {block.index} added! Difficulty: {block.difficulty}")
            print(f"[DEBUG] Difficulty incremented to {new_difficulty} for next round.")
            return block