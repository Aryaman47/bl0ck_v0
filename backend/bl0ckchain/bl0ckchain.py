from .bl0ck import Block
from .mining import mine_block, get_mining_timeout
from .storage import save_to_file, load_from_file
from difficulty import DifficultyAdjuster
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

        # Use difficulty from adjuster if dynamic or manual mode, else default to 1
        original_difficulty = (
            self.difficulty_adjuster.difficulty
            if self.dynamic_difficulty_enabled or self.manual_mode
            else 1
        )

        # We'll attempt retries only when Dynamic Difficulty Mode (DDM = Dynamic Difficulty Mode) is enabled AND we're in auto mode (not manual).
        advanced_retry = self.dynamic_difficulty_enabled and (not self.manual_mode)

        attempt_difficulty = original_difficulty
        temporary_timeout = None  # used when we temporarily increase timeout for a session-span

        while True:
            new_block = Block(
                index=last_block.index + 1,
                timestamp=str(datetime.datetime.now()),
                data=f"Block {last_block.index + 1}",
                previous_hash=last_block.hash,
                difficulty=attempt_difficulty
            )

            # Mining process (supports per-attempt timeout)
            new_block.hash, mining_time = mine_block(new_block, timeout=temporary_timeout)

            # Handle mining failure
            if new_block.hash is None:
                print(f"❌ [DEBUG] Mining failed! Difficulty {attempt_difficulty} exceeded timeout.")

                # If not in advanced retry mode, just record the failure and exit
                if not advanced_retry:
                    self.difficulty_adjuster.track_failed_difficulty(attempt_difficulty)
                    return  # Exit without appending

                # Advanced retry logic for DDM auto-mode:
                fail_count = self.difficulty_adjuster.increment_failure_count(attempt_difficulty)
                # Record as last failed difficulty (legacy field)
                self.difficulty_adjuster.track_failed_difficulty(attempt_difficulty)

                # If fail_count in 1..3: decrement locally and retry immediately (do not persistally change authoritative difficulty)
                if fail_count <= 3:
                    if attempt_difficulty > 1:
                        attempt_difficulty -= 1
                        temporary_timeout = None  # reset to default for immediate retries
                        print(f"🔽 Decrementing difficulty to {attempt_difficulty} and retrying (FailCount={fail_count})...")
                        continue
                    else:
                        print("⚠️ Cannot decrement below difficulty 1; aborting attempt.")
                        return

                # If fail_count == 4: increase timeout temporarily and retry at same difficulty
                if fail_count == 4:
                    base_timeout = get_mining_timeout()
                    increased_timeout = base_timeout + 60  # extra 60 seconds as per spec
                    temporary_timeout = increased_timeout
                    print(f"⏳ FailCount==4 for difficulty {attempt_difficulty}. Increasing timeout to {temporary_timeout}s and retrying...")
                    # Next loop iteration will attempt mining at the same attempt_difficulty with the larger timeout
                    continue

                # If fail_count >= 5 (i.e., the increased-timeout attempt also failed): block this difficulty and above for the current session and set max difficulty to attempt_difficulty-1
                if fail_count >= 5:
                    # Block auto increases into this difficulty (and above) for the remainder of the session
                    self.difficulty_adjuster.block_from_difficulty(attempt_difficulty)
                    # Lower the authoritative difficulty to the next lower value (so new difficulty won't be set back to attempt_difficulty)
                    new_committed = max(1, attempt_difficulty - 1)
                    self.difficulty_adjuster.set_difficulty(new_committed)
                    print(f"🚫 After repeated failures, blocking difficulty {attempt_difficulty} and above for this session; set max difficulty to {new_committed}.")
                    self.difficulty_adjuster.failed_difficulty = attempt_difficulty
                    return

            # ----------------- SUCCESS PATH -----------------
            new_block.mining_time = round(mining_time, 2)
            print(f"⏳ [DEBUG] Mining Time: {new_block.mining_time}s")

            # If we were in advanced retry mode and we succeeded at a lower difficulty than the original target
            # we MUST NOT reset the failure count for that original difficulty (per your spec), and we MUST keep
            # the authoritative difficulty (so next call still begins with original_difficulty).
            if advanced_retry and attempt_difficulty != original_difficulty:
                # Keep failure count as-is. Restore the authoritative difficulty value to original so
                # next add attempts start from the "new difficulty" user expects.
                self.difficulty_adjuster.difficulty = original_difficulty
                print(f"🔼 Success at lower difficulty {attempt_difficulty}; keeping target difficulty at {original_difficulty} (FailCount preserved).")
            else:
                # If success at the original difficulty, we can clear its failure counter (optional; keeps behaviour sane).
                # You can remove this reset if you prefer to keep success/failure counters across successes too.
                if advanced_retry:
                    self.difficulty_adjuster.reset_failure_count(attempt_difficulty)

            # Record mining time and adjust difficulty if DDM is enabled
            if self.dynamic_difficulty_enabled:
                # Use the existing record_block_time behavior
                self.difficulty_adjuster.record_block_time(new_block.mining_time)

                # Keep only the last `adjustment_interval` block times (handled by record_block_time)
                new_difficulty = self.difficulty_adjuster.adjust_difficulty()
                print(f"⚙️ [DEBUG] Adjusted Difficulty: {new_difficulty}")

                # Additional safety: if there exists a fail count for the original difficulty, do not allow the adjuster to jump beyond original_difficulty
                if self.difficulty_adjuster.get_failure_count(original_difficulty) > 0:
                    # Force it back to original_difficulty (so we don't skip upward while a failure count exists)
                    self.difficulty_adjuster.set_difficulty(original_difficulty)
                    print(f"[DEBUG] Prevented auto-increment due to existing FailCount for difficulty {original_difficulty}.")

                # Clear failed_difficulty legacy field if recovery is implied
                if self.difficulty_adjuster.failed_difficulty:
                    if attempt_difficulty < self.difficulty_adjuster.failed_difficulty:
                        # If we succeeded at a lower difficulty and previously had a failed difficulty, attempt small recovery
                        self.difficulty_adjuster.difficulty = min(self.difficulty_adjuster.max_difficulty, self.difficulty_adjuster.difficulty + 1)
                        print(f"🔼 Increasing difficulty to {self.difficulty_adjuster.difficulty}.")
                    self.difficulty_adjuster.failed_difficulty = None  # Reset after recovery

            # Append and save the new block
            self.chain.append(new_block)
            save_to_file(self.chain)

            print(f"\n✅ Block {new_block.index} added! Difficulty: {new_block.difficulty}")
            return new_block
