"""Config-driven model registry, loaded from config/models.yaml.

Services look up models here by key instead of hardcoding model ids, so a
model swap is a config-file edit, not a code change across modules
(MS-03 deliverable, NFR-02: configuration via files, not hardcoded).
"""

from functools import lru_cache
from pathlib import Path

import yaml

_REGISTRY_PATH = Path(__file__).parent / "models.yaml"


@lru_cache(maxsize=1)
def _load_registry() -> dict:
    with open(_REGISTRY_PATH) as f:
        return yaml.safe_load(f)


def get_model_config(key: str) -> dict:
    registry = _load_registry()
    if key not in registry:
        raise KeyError(f"No model registered for '{key}'. Known keys: {sorted(registry)}")
    return registry[key]


def all_model_keys() -> list[str]:
    return sorted(_load_registry())
