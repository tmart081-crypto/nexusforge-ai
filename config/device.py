"""Device manager: picks the best available compute device and exposes it
in the formats different libraries expect, so services never hardcode
'cuda'/'cpu' themselves."""

from functools import lru_cache

import torch


@lru_cache(maxsize=1)
def get_torch_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def get_pipeline_device() -> int | str:
    """Device value expected by transformers.pipeline(device=...)."""
    device = get_torch_device()
    if device.type == "cuda":
        return 0
    if device.type == "mps":
        return "mps"
    return -1


def device_summary() -> dict:
    device = get_torch_device()
    return {
        "device_type": device.type,
        "cuda_available": torch.cuda.is_available(),
        "cuda_device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        "mps_available": torch.backends.mps.is_available(),
    }
