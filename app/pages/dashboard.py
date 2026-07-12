"""Dashboard: landing page, module status, environment summary."""

import streamlit as st

from config.device import device_summary
from config.modules import MODULES
from config.settings import APP_NAME, APP_VERSION, CLIENT_NAME, ENGAGEMENT_CODE

st.title(f"🏠 {APP_NAME}")
st.caption(f"v{APP_VERSION} · Client: {CLIENT_NAME} · Engagement {ENGAGEMENT_CODE}")

st.write(
    "Enterprise multi-modal AI platform: text intelligence, image understanding, "
    "document analysis, prompt optimization, embeddings, model/pipeline explorers, "
    "Responsible AI, and AI infrastructure — in a single application."
)

col1, col2, col3 = st.columns(3)
col1.metric("Modules", len(MODULES))
col2.metric("Implemented", 1)
col3.metric("Pass mark", "70 / 100")

st.divider()

st.subheader("Environment")
device = device_summary()
st.json(device)

st.divider()

st.subheader("Module status")
sections: dict[str, list[dict]] = {}
for module in MODULES:
    sections.setdefault(module["section"], []).append(module)

for section, mods in sections.items():
    st.markdown(f"**{section}**")
    for m in mods:
        status = "✅ Live" if m["key"] == "dashboard" else f"🚧 Planned — {m['milestone']}"
        st.write(f"{m['icon']} {m['title']} — {status}")
