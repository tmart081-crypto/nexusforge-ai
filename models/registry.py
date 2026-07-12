"""Lazy-loading pipeline cache.

Nothing downloads or loads until a service actually asks for a pipeline by
key. This keeps app startup fast and lets the shell run on CPU-only
machines with no models installed yet.
"""

from transformers import pipeline as hf_pipeline
from transformers.pipelines.base import Pipeline

from config.device import get_pipeline_device
from config.models import get_model_config
from utils.logger import get_logger

log = get_logger("models.registry")

_PIPELINE_CACHE: dict[str, Pipeline] = {}


def get_pipeline(key: str) -> Pipeline:
    """Return a cached HF pipeline for the given registry key, loading it
    on first use."""
    if key not in _PIPELINE_CACHE:
        cfg = get_model_config(key)
        log.info("Loading pipeline '%s' -> task=%s model=%s", key, cfg["task"], cfg["model"])
        _PIPELINE_CACHE[key] = hf_pipeline(
            task=cfg["task"],
            model=cfg["model"],
            device=get_pipeline_device(),
        )
    return _PIPELINE_CACHE[key]


def loaded_pipelines() -> list[str]:
    return list(_PIPELINE_CACHE.keys())
