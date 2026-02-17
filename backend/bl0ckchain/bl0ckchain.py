from .bl0ck import Block
from .mining import mine_block, get_mining_timeout
from .storage import save_to_file, load_from_file
from difficulty import DifficultyAdjuster
from logger import logger
import datetime
import threading


class Blockchain:
    def __init__(self):
        self.lock = threading.Lock()
        self.chain = load_from_file()
        self.manual_mode = False  # False = Automatic mode (default)
        self.difficulty_adjuster = DifficultyAdjuster(
            target_block_time=10,
            adjustment_interval=5
        )

        with self.lock:
            if not self.chain:
                self.chain = [self.create_genesis_block()]
                save_to_file(self.chain)

    def create_genesis_block(self):
        return Block(0, str(datetime.datetime.now()), "Genesis Block", "0", difficulty=1)

    # -------------------------
    # MODE CONTROL
    # -------------------------

    def set_manual_difficulty(self, difficulty):
        if 1 <= difficulty <= 10:
            self.difficulty_adjuster.set_difficulty(difficulty)
            self.manual_mode = True
            logger.info(f"Manual Mode enabled. Difficulty set to {difficulty}.")
        else:
            logger.warning(f"Invalid manual difficulty input: {difficulty}")

    def switch_to_auto_mode(self):
        if not self.manual_mode:
            logger.warning("Already in Automatic Mode.")
            return

        self.manual_mode = False
        logger.info("Switched to Automatic Mode.")

        if self.difficulty_adjuster.failed_difficulty:
            new_diff = max(1, self.difficulty_adjuster.failed_difficulty - 1)
            self.difficulty_adjuster.set_difficulty(new_diff)
            logger.info(f"Adjusted difficulty to {new_diff} due to previous failure.")

    # -------------------------
    # BLOCK ADDITION
    # -------------------------

    def add_block(self):
        with self.lock:
            last_block = self.chain[-1]

            # Always use current difficulty (Auto or Manual)
            base_difficulty = self.difficulty_adjuster.difficulty

            # Respect blacklist limits
            max_allowed_diff = base_difficulty
            if self.difficulty_adjuster.blocked_thresholds:
                max_block = min(self.difficulty_adjuster.blocked_thresholds)
                if base_difficulty >= max_block:
                    max_allowed_diff = max(1, max_block - 1)
                    logger.debug(
                        f"Difficulty {base_difficulty} blocked, limiting to {max_allowed_diff}"
                    )

            current_timeout = get_mining_timeout()
            fail_count = self.difficulty_adjuster.get_failure_count(base_difficulty)

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

            # -----------------------------------------
            # FAILURE THRESHOLD HANDLING
            # -----------------------------------------

            if fail_count > 3:
                logger.debug(
                    f"FailCount > 3 for difficulty {base_difficulty}, retrying with extended timeout"
                )

                block, mined_hash, mining_time = attempt_mine(
                    base_difficulty,
                    current_timeout + 60
                )

                if mined_hash is None:
                    self.difficulty_adjuster.block_from_difficulty(base_difficulty)
                    new_diff = max(1, base_difficulty - 1)
                    self.difficulty_adjuster.set_difficulty(new_diff)
                    self.difficulty_adjuster.reset_failure_count(base_difficulty)

                    logger.warning(
                        f"Blacklisting difficulty {base_difficulty}. "
                        f"Limiting max difficulty to {new_diff}."
                    )
                    return None

                else:
                    self.difficulty_adjuster.reset_failure_count(base_difficulty)
                    block.mining_time = round(mining_time, 2)
                    self.chain.append(block)
                    save_to_file(self.chain)

                    logger.info(
                        f"Block {block.index} added at difficulty {block.difficulty} "
                        f"(with extended timeout)."
                    )
                    return block

            # -----------------------------------------
            # NORMAL MINING FLOW
            # -----------------------------------------

            effective_difficulty = min(base_difficulty, max_allowed_diff)

            block, mined_hash, mining_time = attempt_mine(
                effective_difficulty,
                current_timeout
            )

            if mined_hash is None:
                fail_count = self.difficulty_adjuster.increment_failure_count(
                    effective_difficulty
                )

                retry_diff = max(1, effective_difficulty - 1)

                logger.debug(
                    f"Mining failed at difficulty {effective_difficulty}, "
                    f"retrying at {retry_diff} (FailCount={fail_count})"
                )

                block_retry, mined_hash_retry, mining_time_retry = attempt_mine(
                    retry_diff,
                    current_timeout
                )

                if mined_hash_retry is None:
                    logger.warning(
                        f"Mining failed again at retry difficulty {retry_diff}."
                    )
                    return None

                else:
                    self.difficulty_adjuster.reset_failure_count(retry_diff)
                    block_retry.mining_time = round(mining_time_retry, 2)
                    self.chain.append(block_retry)
                    save_to_file(self.chain)

                    self.difficulty_adjuster.set_difficulty(base_difficulty)

                    logger.info(
                        f"Block {block_retry.index} added at difficulty {retry_diff} "
                        f"(retry success)."
                    )
                    return block_retry

            # -----------------------------------------
            # SUCCESS AT BASE DIFFICULTY
            # -----------------------------------------

            block.mining_time = round(mining_time, 2)
            self.chain.append(block)
            save_to_file(self.chain)

            self.difficulty_adjuster.reset_failure_count(base_difficulty)

            logger.info(
                f"Block {block.index} added successfully. "
                f"Difficulty: {block.difficulty}"
            )

            # -------------------------
            # MANUAL MODE
            # -------------------------
            if self.manual_mode:
                logger.debug(
                    f"Manual mode active. Keeping difficulty fixed at {base_difficulty}."
                )
                return block

            # -------------------------
            # AUTOMATIC MODE
            # -------------------------

            self.difficulty_adjuster.record_block_time(block.mining_time)

            new_difficulty = self.difficulty_adjuster.adjust_difficulty()

            if self.difficulty_adjuster.blocked_thresholds:
                min_block = min(self.difficulty_adjuster.blocked_thresholds)
                if new_difficulty >= min_block:
                    new_difficulty = max(1, min_block - 1)

            self.difficulty_adjuster.set_difficulty(new_difficulty)

            logger.debug(
                f"Automatic mode adjusted difficulty to {new_difficulty}."
            )

            return block
