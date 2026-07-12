"""Image Intelligence: BLIP captioning, detailed description, and visual
question answering."""

import streamlit as st

from services import image_service

st.title("🖼️ Image Intelligence")
st.caption(
    "Upload an image to run BLIP captioning, a longer description, and "
    "visual question answering. Models lazy-load on first use — the first "
    "click downloads and caches them."
)

uploaded = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "webp"])

if uploaded is None:
    st.info("Upload a PNG, JPG, or WEBP image to get started.")
    st.stop()

load_result = image_service.load_image(uploaded)
if not load_result["ok"]:
    st.error(load_result["error"])
    st.stop()

image = load_result["result"]
st.image(image, caption="Preview", width="stretch")


def _show(response: dict, render) -> None:
    if response["ok"]:
        render(response["result"])
    else:
        st.error(response["error"])


tab_caption, tab_description, tab_vqa = st.tabs(["Caption", "Description", "Visual Q&A"])

with tab_caption:
    if st.button("Generate caption", key="caption_btn"):
        with st.spinner("Captioning..."):
            _show(
                image_service.caption(image),
                lambda r: st.success(f"{r['caption']}  (confidence {r['confidence']})"),
            )

with tab_description:
    st.caption("A longer, more detailed BLIP description than the short caption.")
    if st.button("Generate description", key="describe_btn"):
        with st.spinner("Describing..."):
            _show(
                image_service.describe(image),
                lambda r: st.success(f"{r['caption']}  (confidence {r['confidence']})"),
            )

with tab_vqa:
    question = st.text_input("Ask a question about the image", "What is in this image?", key="vqa_question")
    if st.button("Ask", key="vqa_btn"):
        with st.spinner("Thinking..."):
            _show(
                image_service.visual_question_answer(image, question),
                lambda r: st.success(f"{r['answer']}  (confidence {r['confidence']})"),
            )
