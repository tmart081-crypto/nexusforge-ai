"""Text Intelligence: summarize, translate, QA, sentiment, NER, keywords,
fill-mask, generation, zero-shot, feature extraction."""

import streamlit as st

from services import text_service

st.title("📝 Text Intelligence")
st.caption(
    "Each tab calls a Hugging Face model through services/text_service.py. "
    "Models lazy-load on first use — the first click on a new tab downloads "
    "and caches its model, so it can take a while depending on your connection."
)

(
    tab_summary,
    tab_translate,
    tab_qa,
    tab_sentiment,
    tab_ner,
    tab_keywords,
    tab_mask,
    tab_generate,
    tab_zero_shot,
    tab_features,
) = st.tabs(
    [
        "Summarize",
        "Translate",
        "Q&A",
        "Sentiment",
        "Entities",
        "Keywords",
        "Fill-mask",
        "Generate",
        "Zero-shot",
        "Features",
    ]
)


def _show(response: dict, render) -> None:
    if response["ok"]:
        render(response["result"])
    else:
        st.error(response["error"])


with tab_summary:
    text = st.text_area(
        "Text to summarize",
        "Streamlit turns Python scripts into shareable web apps. Hugging Face "
        "Transformers gives access to thousands of pretrained models for text, "
        "vision, and audio tasks, so teams can build AI features without "
        "training models from scratch. Together they make it possible to ship "
        "an interactive AI demo in a single afternoon.",
        height=150,
        key="summary_input",
    )
    if st.button("Summarize", key="summary_btn"):
        with st.spinner("Summarizing..."):
            _show(text_service.summarize(text), lambda r: st.success(r))

with tab_translate:
    text = st.text_area("English text", "The quick brown fox jumps over the lazy dog.", key="translate_input")
    if st.button("Translate to French", key="translate_btn"):
        with st.spinner("Translating..."):
            _show(text_service.translate_en_to_fr(text), lambda r: st.success(r))

with tab_qa:
    context = st.text_area(
        "Context",
        "NexusForge AI Platform is being built for client Aether Dynamics Global "
        "as a final capstone project. The pass mark is 70 out of 100.",
        key="qa_context",
    )
    question = st.text_input("Question", "What is the pass mark?", key="qa_question")
    if st.button("Answer", key="qa_btn"):
        with st.spinner("Finding answer..."):
            _show(
                text_service.answer_question(question, context),
                lambda r: st.success(f"{r['answer']}  (confidence {r['score']})"),
            )

with tab_sentiment:
    text = st.text_area("Text", "I really enjoyed building this project, it turned out great!", key="sentiment_input")
    if st.button("Analyze sentiment", key="sentiment_btn"):
        with st.spinner("Analyzing..."):
            _show(
                text_service.analyze_sentiment(text),
                lambda r: st.success(f"{r['label']}  (confidence {r['score']})"),
            )

with tab_ner:
    text = st.text_area("Text", "Aether Dynamics Global is headquartered in Berlin, Germany.", key="ner_input")
    if st.button("Extract entities", key="ner_btn"):
        with st.spinner("Extracting entities..."):
            _show(text_service.extract_entities(text), lambda r: st.table(r) if r else st.info("No entities found."))

with tab_keywords:
    text = st.text_area(
        "Text",
        "NexusForge AI Platform combines text intelligence, image understanding "
        "with BLIP, document analysis, and Responsible AI dashboards into one "
        "enterprise multi-modal application.",
        key="keywords_input",
    )
    top_n = st.slider("Number of keywords", 3, 10, 5, key="keywords_top_n")
    if st.button("Extract keywords", key="keywords_btn"):
        with st.spinner("Ranking keywords..."):
            _show(
                text_service.extract_keywords(text, top_n=top_n),
                lambda r: st.table(r) if r else st.info("No keyword candidates found."),
            )

with tab_mask:
    text = st.text_input("Text with [MASK]", "Paris is the [MASK] of France.", key="mask_input")
    if st.button("Fill mask", key="mask_btn"):
        with st.spinner("Filling mask..."):
            _show(text_service.fill_mask(text), lambda r: st.table(r))

with tab_generate:
    prompt = st.text_input("Prompt", "Once upon a time,", key="generate_input")
    max_tokens = st.slider("Max new tokens", 10, 100, 50, key="generate_max_tokens")
    if st.button("Generate", key="generate_btn"):
        with st.spinner("Generating..."):
            _show(text_service.generate_text(prompt, max_new_tokens=max_tokens), lambda r: st.success(r))

with tab_zero_shot:
    text = st.text_area("Text", "The new quarterly earnings report exceeded analyst expectations.", key="zs_input")
    labels_raw = st.text_input("Candidate labels (comma-separated)", "business, sports, politics, technology", key="zs_labels")
    if st.button("Classify", key="zs_btn"):
        labels = [label.strip() for label in labels_raw.split(",") if label.strip()]
        with st.spinner("Classifying..."):
            _show(text_service.zero_shot_classify(text, labels), lambda r: st.table(r))

with tab_features:
    text = st.text_area("Text", "Feature extraction turns text into numeric vectors.", key="features_input")
    if st.button("Extract features", key="features_btn"):
        with st.spinner("Extracting..."):
            _show(text_service.extract_features(text), lambda r: st.json(r))
