import time

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

    def record_block_time(self, mining_time):
        """Records the mining duration of a block."""
        self.block_times.append(mining_time)

        if len(self.block_times) > self.adjustment_interval:
            self.block_times.pop(0)  # Keep only the latest 'adjustment_interval' times

    def adjust_difficulty(self):
        """Adjusts difficulty dynamically based on average block mining time."""
        if len(self.block_times) < self.adjustment_interval:
            return self.difficulty  # Not enough data to adjust yet

        avg_time = sum(self.block_times) / len(self.block_times)

        if avg_time < self.target_block_time:
            self.difficulty = min(self.max_difficulty, self.difficulty + 1)  # Increase difficulty
        elif avg_time > self.target_block_time:
            self.difficulty = max(1, self.difficulty - 1)  # Decrease but keep at least 1

        return self.difficulty

    def track_failed_difficulty(self, difficulty):
        """Tracks difficulty level when mining fails due to timeout."""
        self.failed_difficulty = difficulty
