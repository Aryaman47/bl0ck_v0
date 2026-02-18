#backend/logger.py
from collections import deque
import logging

MAX_LOGS = 200
log_buffer = deque(maxlen=MAX_LOGS)

class MemoryLogHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        log_buffer.append(log_entry)

def get_logs():
    return list(log_buffer)

# Setup Logger
logger = logging.getLogger("bl0ckchain")
logger.setLevel(logging.INFO)

memory_handler = MemoryLogHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
memory_handler.setFormatter(formatter)

logger.addHandler(memory_handler)