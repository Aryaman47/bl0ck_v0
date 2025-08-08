class DifficultyAdjuster:
    def __init__(self, target_block_time=10, adjustment_interval=5, max_difficulty=10):
        """
        Initializes the difficulty adjuster.
        :param target_block_time: Ideal time (in seconds) to mine a block.
        :param adjustment_interval: Number of blocks after which difficulty is adjusted.
        :param max_difficulty: Maximum difficulty allowed.
        """
        self.target_block_time = target_block_time
        self.adjustment_interval = adjustment_interval
        self.max_difficulty = max_difficulty
        self.difficulty = 1  # Default difficulty
        self.block_times = []  # Store timestamps of last blocks
        self.failed_difficulty = None  # Store difficulty if a timeout occurs

        # Session-only (in-memory) tracking:
        # Tracks how many times mining has failed for a specific difficulty in the current server session.
        self.failure_counts = {}  # e.g., {7: 2}
        # Difficulties that are blocked for auto-increment in the current session (block this difficulty and above).
        self.blocked_thresholds = set()

    def record_block_time(self, mining_time):
        """Records the mining duration of a block."""
        self.block_times.append(mining_time)
        if len(self.block_times) > self.adjustment_interval:
            self.block_times.pop(0)

        print(f"[DEBUG] Block Times: {self.block_times}")

    def adjust_difficulty(self):
        """
        Adjusts difficulty based on average mining time.
        Respects session-level blocked difficulties so Dynamic Difficulty Mode (DDM = Dynamic Difficulty Mode)
        will not auto-increase to a blocked difficulty or beyond.

        NEW: Also prevents auto-increment if there is a non-zero failure count for the current difficulty.
        This avoids skipping up (e.g., 7 -> 8) when difficulty 7 has recent failures.
        """
        if len(self.block_times) < self.adjustment_interval:
            print(f"[DEBUG] Not enough blocks to adjust difficulty: {len(self.block_times)}/{self.adjustment_interval}")
            return self.difficulty  # Not enough data to adjust yet

        avg_time = sum(self.block_times) / len(self.block_times)
        print(f"[DEBUG] Avg Mining Time: {avg_time}s | Current Difficulty: {self.difficulty}")

        if avg_time < self.target_block_time:
            # Candidate increase
            candidate = min(self.max_difficulty, self.difficulty + 1)

            # --- NEW CHECK: if the current difficulty has recorded recent failures, do NOT auto-increase ---
            if self.get_failure_count(self.difficulty) > 0:
                print(f"[DEBUG] Not auto-increasing because FailCount for difficulty {self.difficulty} is {self.get_failure_count(self.difficulty)}")
                candidate = self.difficulty  # keep same for now

            # Respect blocked thresholds: do not allow auto-increment into a blocked difficulty or beyond.
            if self.blocked_thresholds:
                min_blocked = min(self.blocked_thresholds)
                if candidate >= min_blocked:
                    candidate = max(1, min_blocked - 1)

            self.difficulty = candidate

        elif avg_time > self.target_block_time:
            self.difficulty = max(1, self.difficulty - 1)  # Decrease but keep at least 1

        print(f"[DEBUG] New Difficulty: {self.difficulty}")
        return self.difficulty

    def track_failed_difficulty(self, difficulty):
        """Tracks difficulty level when mining fails due to timeout (legacy field kept)."""
        self.failed_difficulty = difficulty

    # ---------- New helpers for session-level failure/block tracking ----------

    def increment_failure_count(self, difficulty):
        """Increment and return the failure count for a particular difficulty in this session."""
        self.failure_counts[difficulty] = self.failure_counts.get(difficulty, 0) + 1
        print(f"[DEBUG] FailCount for difficulty {difficulty}: {self.failure_counts[difficulty]}")
        return self.failure_counts[difficulty]

    def reset_failure_count(self, difficulty):
        """Reset failure count for a given difficulty (on explicit resets)."""
        if difficulty in self.failure_counts:
            del self.failure_counts[difficulty]
            print(f"[DEBUG] FailCount reset for difficulty {difficulty}")

    def get_failure_count(self, difficulty):
        return self.failure_counts.get(difficulty, 0)

    def block_from_difficulty(self, difficulty):
        """
        Block auto-mode from increasing to this difficulty or beyond for the current session.
        Example: block_from_difficulty(7) will prevent auto-increment to 7 or above.
        """
        self.blocked_thresholds.add(difficulty)
        print(f"[DEBUG] Session blocked difficulties (from): {sorted(self.blocked_thresholds)}")

    def is_blocked_for_increase(self, candidate_difficulty):
        """Return True if candidate_difficulty is blocked (i.e., >= any blocked threshold)."""
        return any(block <= candidate_difficulty for block in self.blocked_thresholds)

    # ---------- NEW: setter to commit difficulty changes immediately ----------

    def set_difficulty(self, new_difficulty):
        """Set the authoritative difficulty value (bounded) and print debug."""
        if new_difficulty < 1:
            new_difficulty = 1
        if new_difficulty > self.max_difficulty:
            new_difficulty = self.max_difficulty

        self.difficulty = new_difficulty
        print(f"[DEBUG] Difficulty forcibly set to {self.difficulty}")
        return self.difficulty
