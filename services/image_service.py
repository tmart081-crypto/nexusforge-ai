"""Image Intelligence business logic (BLIP captioning, description, VQA).

Same pattern as services/text_service.py: the UI never touches models or
PIL directly. Every function returns {"ok": True, "result": ...} or
{"ok": False, "error": ...}.
"""

from typing import Any, Callable

import numpy as np
import torch
from PIL import Image, UnidentifiedImageError

from models.registry import get_blip_captioner, get_blip_vqa
from utils.logger import get_logger

log = get_logger("services.image")

MAX_DIMENSION = 4096  # guard against absurdly large / decompression-bomb-style uploads


def _safe(name: str, fn: Callable[[], Any]) -> dict:
    try:
        result = fn()
        log.info("image_service.%s ok", name)
        return {"ok": True, "result": result}
    except Exception as exc:  # noqa: BLE001 - surface any decode/model/runtime error to the UI
        log.exception("image_service.%s failed", name)
        return {"ok": False, "error": str(exc)}


def load_image(file) -> dict:
    """Validate and decode an uploaded file into a PIL Image, handling
    corrupt or unsupported files gracefully instead of crashing the page."""

    def run():
        try:
            probe = Image.open(file)
            probe.verify()  # raises on corrupt/truncated data; invalidates `probe` after
        except (UnidentifiedImageError, OSError) as exc:
            raise ValueError("Unsupported or corrupt image file — could not decode it as an image.") from exc

        file.seek(0)
        image = Image.open(file).convert("RGB")
        if max(image.size) > MAX_DIMENSION:
            raise ValueError(
                f"Image too large ({image.size[0]}x{image.size[1]}px); max dimension is {MAX_DIMENSION}px."
            )
        return image

    return _safe("load_image", run)


def _generate_caption(image: Image.Image, prompt: str | None, max_new_tokens: int) -> dict:
    processor, model = get_blip_captioner()
    device = next(model.parameters()).device
    inputs = processor(image, text=prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            output_scores=True,
            return_dict_in_generate=True,
        )

    caption = processor.decode(outputs.sequences[0], skip_special_tokens=True).strip()
    transition_scores = model.compute_transition_scores(outputs.sequences, outputs.scores, normalize_logits=True)
    confidence = float(np.exp(transition_scores[0].mean().cpu()))
    return {"caption": caption, "confidence": round(confidence, 4)}


def caption(image: Image.Image) -> dict:
    """Short BLIP caption (unconditional generation)."""
    return _safe("caption", lambda: _generate_caption(image, prompt=None, max_new_tokens=30))


def describe(image: Image.Image) -> dict:
    """Longer, more detailed caption — same model, steered with a prompt
    prefix and a larger token budget rather than a second model."""
    return _safe(
        "describe",
        lambda: _generate_caption(image, prompt="a detailed photography of", max_new_tokens=60),
    )


def visual_question_answer(image: Image.Image, question: str) -> dict:
    """BLIP-VQA is generative (free-form answer text), not a fixed-vocab
    classifier, so transformers' visual-question-answering pipeline doesn't
    expose a score for it. Use the model directly, same as captioning, to
    compute one via compute_transition_scores."""

    def run():
        if not question.strip():
            raise ValueError("Enter a question to ask about the image.")

        processor, model = get_blip_vqa()
        device = next(model.parameters()).device
        inputs = processor(image, question, return_tensors="pt").to(device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=15,
                output_scores=True,
                return_dict_in_generate=True,
            )

        answer = processor.decode(outputs.sequences[0], skip_special_tokens=True).strip()
        transition_scores = model.compute_transition_scores(outputs.sequences, outputs.scores, normalize_logits=True)
        confidence = float(np.exp(transition_scores[0].mean().cpu()))
        return {"answer": answer, "confidence": round(confidence, 4)}

    return _safe("visual_question_answer", run)
