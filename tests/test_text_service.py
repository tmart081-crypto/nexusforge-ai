import numpy as np

from services import text_service


def test_fill_mask_requires_mask_token():
    result = text_service.fill_mask("Paris is the capital of France.")
    assert result["ok"] is False
    assert "[MASK]" in result["error"]


def test_candidate_phrases_extracts_noun_phrases():
    phrases = text_service._candidate_phrases(
        "NexusForge AI Platform combines text intelligence and image understanding."
    )
    assert any("NexusForge" in phrase for phrase in phrases)


def test_extract_keywords_ranks_with_mocked_embeddings(monkeypatch):
    class FakeModel:
        def encode(self, texts):
            # Deterministic fake embeddings: longer strings get a larger
            # first dimension so ranking is predictable without downloading
            # a real model.
            return np.array([[len(t), 1.0, 0.0] for t in texts])

    monkeypatch.setattr(text_service, "get_sentence_transformer", lambda key: FakeModel())

    result = text_service.extract_keywords("NexusForge AI Platform builds text intelligence tools.", top_n=3)
    assert result["ok"] is True
    assert len(result["result"]) <= 3
    assert all("keyword" in item and "score" in item for item in result["result"])
