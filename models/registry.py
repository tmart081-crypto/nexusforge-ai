"""Lazy-loading pipeline cache.

Nothing downloads or loads until a service actually asks for a pipeline by
key. This keeps app startup fast and lets the shell run on CPU-only
machines with no models installed yet.
"""

from sentence_transformers import SentenceTransformer
from transformers import BlipForConditionalGeneration, BlipForQuestionAnswering, BlipProcessor
from transformers import pipeline as hf_pipeline
from transformers.pipelines.base import Pipeline

from config.device import get_pipeline_device, get_torch_device
from config.models import get_model_config
from utils.logger import get_logger

log = get_logger("models.registry")

_PIPELINE_CACHE: dict[str, Pipeline] = {}
_SENTENCE_MODEL_CACHE: dict[str, SentenceTransformer] = {}
_BLIP_CAPTIONER_CACHE: dict[str, tuple[BlipProcessor, BlipForConditionalGeneration]] = {}
_BLIP_VQA_CACHE: dict[str, tuple[BlipProcessor, BlipForQuestionAnswering]] = {}


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


def get_blip_captioner(key: str = "image_caption") -> tuple[BlipProcessor, BlipForConditionalGeneration]:
    """Return a cached (processor, model) pair, loaded directly rather than
    via pipeline() so callers can use model.generate(output_scores=True) to
    compute a real per-caption confidence score — the generic image-to-text
    pipeline doesn't expose one."""
    if key not in _BLIP_CAPTIONER_CACHE:
        cfg = get_model_config(key)
        log.info("Loading BLIP captioner '%s' -> model=%s", key, cfg["model"])
        processor = BlipProcessor.from_pretrained(cfg["model"])
        model = BlipForConditionalGeneration.from_pretrained(cfg["model"]).to(get_torch_device())
        _BLIP_CAPTIONER_CACHE[key] = (processor, model)
    return _BLIP_CAPTIONER_CACHE[key]


def get_blip_vqa(key: str = "image_vqa") -> tuple[BlipProcessor, BlipForQuestionAnswering]:
    """Return a cached (processor, model) pair for visual QA, loaded
    directly rather than via pipeline() — the visual-question-answering
    pipeline for this generative BLIP model doesn't expose a score, so we
    compute one ourselves the same way get_blip_captioner() does."""
    if key not in _BLIP_VQA_CACHE:
        cfg = get_model_config(key)
        log.info("Loading BLIP VQA model '%s' -> model=%s", key, cfg["model"])
        processor = BlipProcessor.from_pretrained(cfg["model"])
        model = BlipForQuestionAnswering.from_pretrained(cfg["model"]).to(get_torch_device())
        _BLIP_VQA_CACHE[key] = (processor, model)
    return _BLIP_VQA_CACHE[key]


def loaded_pipelines() -> list[str]:
    return (
        list(_PIPELINE_CACHE.keys())
        + [f"st:{k}" for k in _SENTENCE_MODEL_CACHE]
        + [f"blip:{k}" for k in _BLIP_CAPTIONER_CACHE]
        + [f"blip_vqa:{k}" for k in _BLIP_VQA_CACHE]
    )
