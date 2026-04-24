#backend/bl0ckchain/mining.py
from logger import logger
from mining_state import mining_state

from .bl0ck import Block
from .mining_backends import get_backend, list_backends

# Default timeout value (in seconds)
timeout_limit = 60
active_backend = "cpu"
supported_backend_modes = ("cpu", "gpu", "auto")


def mine_block(block: Block, timeout=None):
    """
    Mine the given block.

    If `timeout` is provided, use it for this mining attempt;
    otherwise use the global timeout_limit.

    Returns:
        (hash or None, mining_time_seconds)
    """

    global timeout_limit

    if timeout is None:
        timeout = timeout_limit

    backend = get_backend(active_backend)
    if backend is None:
        raise RuntimeError(f"Unsupported mining backend: {active_backend}")

    return backend.mine(block, timeout, mining_state)


def set_mining_timeout(timeout):
    """Allows users to set a manual timeout limit."""
    global timeout_limit
    if timeout > 0:
        timeout_limit = timeout
        print(f"⏳ Mining timeout set to {timeout} seconds.")
        logger.info(f"Mining timeout updated to {timeout} seconds.")
    else:
        print("⚠️ Invalid timeout! Please enter a positive number.")


def get_mining_timeout():
    """Return the current mining timeout (global session value)."""
    return timeout_limit


def get_mining_backend():
    return active_backend


def set_mining_backend(name: str):
    global active_backend
    if get_backend(name) is None:
        raise ValueError(f"Unsupported backend '{name}'")
    active_backend = name


def get_mining_backend_capabilities():
    available = list_backends()
    return {
        "active_backend": active_backend,
        "available_backends": available,
        "supported_modes": list(supported_backend_modes),
        "gpu_available": "gpu" in available,
        "auto_available": "auto" in available,
    }
