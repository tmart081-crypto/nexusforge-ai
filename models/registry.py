"""Lazy-loading pipeline cache.

Nothing downloads or loads until a service actually asks for a pipeline by
key. This keeps app startup fast and lets the shell run on CPU-only
machines with no models installed yet.
"""

from sentence_transformers import SentenceTransformer
from transformers import pipeline as hf_pipeline
from transformers.pipelines.base import Pipeline

from config.device import get_pipeline_device, get_torch_device
from config.models import get_model_config
from utils.logger import get_logger

log = get_logger("models.registry")

_PIPELINE_CACHE: dict[str, Pipeline] = {}
_SENTENCE_MODEL_CACHE: dict[str, SentenceTransformer] = {}


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


def get_sentence_transformer(key: str) -> SentenceTransformer:
    """Return a cached SentenceTransformer for the given registry key,
    loading it on first use. Separate cache from get_pipeline() because
    sentence-transformers models aren't transformers.Pipeline objects."""
    if key not in _SENTENCE_MODEL_CACHE:
        cfg = get_model_config(key)
        log.info("Loading sentence-transformer '%s' -> model=%s", key, cfg["model"])
        _SENTENCE_MODEL_CACHE[key] = SentenceTransformer(cfg["model"], device=get_torch_device().type)
    return _SENTENCE_MODEL_CACHE[key]


def loaded_pipelines() -> list[str]:
    return list(_PIPELINE_CACHE.keys()) + [f"st:{k}" for k in _SENTENCE_MODEL_CACHE]
