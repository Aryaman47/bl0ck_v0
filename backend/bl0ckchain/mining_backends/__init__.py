from .cpu_backend import CpuMiningBackend


_BACKENDS = {
    "cpu": CpuMiningBackend(),
}


def get_backend(name: str):
    return _BACKENDS.get(name)


def list_backends():
    return sorted(_BACKENDS.keys())
