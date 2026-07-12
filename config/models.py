"""Config-driven model registry.

Services look up models here by key instead of hardcoding model ids, so a
model swap is a one-line config change, not a code change across modules.
"""

MODEL_REGISTRY = {
    # Text Intelligence
    "text_summarization": {"task": "summarization", "model": "facebook/bart-large-cnn"},
    "text_translation": {"task": "translation_en_to_fr", "model": "Helsinki-NLP/opus-mt-en-fr"},
    "text_qa": {"task": "question-answering", "model": "deepset/roberta-base-squad2"},
    "text_sentiment": {"task": "sentiment-analysis", "model": "distilbert-base-uncased-finetuned-sst-2-english"},
    "text_ner": {"task": "ner", "model": "dslim/bert-base-NER"},
    "text_fill_mask": {"task": "fill-mask", "model": "bert-base-uncased"},
    "text_generation": {"task": "text-generation", "model": "gpt2"},
    "text_zero_shot": {"task": "zero-shot-classification", "model": "facebook/bart-large-mnli"},
    "text_feature_extraction": {"task": "feature-extraction", "model": "sentence-transformers/all-MiniLM-L6-v2"},

    # Image Understanding
    "image_caption": {"task": "image-to-text", "model": "Salesforce/blip-image-captioning-base"},
    "image_vqa": {"task": "visual-question-answering", "model": "Salesforce/blip-vqa-base"},

    # Embeddings
    "sentence_embeddings": {"task": "feature-extraction", "model": "sentence-transformers/all-MiniLM-L6-v2"},
}


def get_model_config(key: str) -> dict:
    if key not in MODEL_REGISTRY:
        raise KeyError(f"No model registered for '{key}'. Known keys: {sorted(MODEL_REGISTRY)}")
    return MODEL_REGISTRY[key]
