"""Text Intelligence business logic.

The UI (app/pages/text_intelligence.py) never touches transformers or
sentence-transformers directly — it calls these functions, which go
through models/registry.py for lazy-loaded, cached models. Every function
returns {"ok": True, "result": ...} or {"ok": False, "error": ...} so the
UI has one consistent shape to render instead of catching exceptions.
"""

from typing import Any, Callable

import numpy as np

from models.registry import get_pipeline, get_sentence_transformer
from utils.logger import get_logger

log = get_logger("services.text")


def _safe(name: str, fn: Callable[[], Any]) -> dict:
    try:
        result = fn()
        log.info("text_service.%s ok", name)
        return {"ok": True, "result": result}
    except Exception as exc:  # noqa: BLE001 - surface any model/runtime error to the UI
        log.exception("text_service.%s failed", name)
        return {"ok": False, "error": str(exc)}


def summarize(text: str, max_length: int = 130, min_length: int = 30) -> dict:
    def run():
        out = get_pipeline("text_summarization")(text, max_length=max_length, min_length=min_length)
        return out[0]["summary_text"]

    return _safe("summarize", run)


def translate_en_to_fr(text: str) -> dict:
    def run():
        out = get_pipeline("text_translation")(text)
        return out[0]["translation_text"]

    return _safe("translate_en_to_fr", run)


def answer_question(question: str, context: str) -> dict:
    def run():
        out = get_pipeline("text_qa")(question=question, context=context)
        return {"answer": out["answer"], "score": round(out["score"], 4)}

    return _safe("answer_question", run)


def analyze_sentiment(text: str) -> dict:
    def run():
        out = get_pipeline("text_sentiment")(text)[0]
        return {"label": out["label"], "score": round(out["score"], 4)}

    return _safe("analyze_sentiment", run)


def extract_entities(text: str) -> dict:
    def run():
        out = get_pipeline("text_ner")(text, aggregation_strategy="simple")
        return [
            {"entity": e["entity_group"], "word": e["word"], "score": round(float(e["score"]), 4)}
            for e in out
        ]

    return _safe("extract_entities", run)


def fill_mask(text: str) -> dict:
    def run():
        if "[MASK]" not in text:
            raise ValueError("Input must contain a [MASK] token, e.g. 'Paris is the [MASK] of France.'")
        out = get_pipeline("text_fill_mask")(text)
        return [{"sequence": o["sequence"], "score": round(o["score"], 4)} for o in out]

    return _safe("fill_mask", run)


def generate_text(prompt: str, max_new_tokens: int = 50) -> dict:
    def run():
        out = get_pipeline("text_generation")(prompt, max_new_tokens=max_new_tokens, num_return_sequences=1)
        return out[0]["generated_text"]

    return _safe("generate_text", run)


def zero_shot_classify(text: str, labels: list[str]) -> dict:
    def run():
        out = get_pipeline("text_zero_shot")(text, candidate_labels=labels)
        return [
            {"label": label, "score": round(score, 4)}
            for label, score in zip(out["labels"], out["scores"])
        ]

    return _safe("zero_shot_classify", run)


def extract_features(text: str) -> dict:
    """Raw token-level hidden states, mean-pooled with NumPy into one
    fixed-size vector regardless of input length."""

    def run():
        token_vectors = get_pipeline("text_feature_extraction")(text)
        matrix = np.array(token_vectors[0])  # (tokens, hidden_dim)
        pooled = matrix.mean(axis=0)
        return {
            "num_tokens": matrix.shape[0],
            "hidden_dim": matrix.shape[1],
            "vector_preview": [round(float(v), 4) for v in pooled[:8]],
            "vector_norm": round(float(np.linalg.norm(pooled)), 4),
        }

    return _safe("extract_features", run)


def extract_keywords(text: str, top_n: int = 5) -> dict:
    """KeyBERT-style keyword extraction: NLTK generates candidate n-grams,
    sentence-transformers embeds them, NumPy cosine similarity ranks them
    against the full text's embedding."""

    def run():
        candidates = _candidate_phrases(text)
        if not candidates:
            return []

        model = get_sentence_transformer("sentence_embeddings")
        doc_vec = model.encode([text])[0]
        cand_vecs = model.encode(candidates)

        doc_norm = doc_vec / np.linalg.norm(doc_vec)
        cand_norms = cand_vecs / np.linalg.norm(cand_vecs, axis=1, keepdims=True)
        scores = cand_norms @ doc_norm

        ranked = sorted(zip(candidates, scores), key=lambda pair: pair[1], reverse=True)
        seen = set()
        top = []
        for phrase, score in ranked:
            if phrase.lower() in seen:
                continue
            seen.add(phrase.lower())
            top.append({"keyword": phrase, "score": round(float(score), 4)})
            if len(top) == top_n:
                break
        return top

    return _safe("extract_keywords", run)


def _candidate_phrases(text: str) -> list[str]:
    import nltk

    for resource in ("tokenizers/punkt_tab", "taggers/averaged_perceptron_tagger_eng", "corpora/stopwords"):
        try:
            nltk.data.find(resource)
        except LookupError:
            nltk.download(resource.split("/")[-1], quiet=True)

    from nltk import pos_tag, word_tokenize
    from nltk.corpus import stopwords

    stop_words = set(stopwords.words("english"))
    tokens = pos_tag(word_tokenize(text))

    candidates: list[str] = []
    current: list[str] = []
    for word, tag in tokens:
        is_noun_or_adj = tag.startswith("NN") or tag.startswith("JJ")
        if is_noun_or_adj and word.lower() not in stop_words and word.isalpha():
            current.append(word)
        else:
            if current:
                candidates.append(" ".join(current))
                current = []
    if current:
        candidates.append(" ".join(current))

    return [c for c in candidates if len(c) > 2]
