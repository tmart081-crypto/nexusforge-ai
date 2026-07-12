"""Dashboard: landing page, module status, environment summary."""

import platform
import time

import streamlit as st

from config.device import device_summary
from config.modules import MODULES
from config.settings import APP_NAME, APP_VERSION, CLIENT_NAME, ENGAGEMENT_CODE, START_TIME
from models.registry import loaded_pipelines


def _format_uptime(seconds: float) -> str:
    minutes, secs = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes}m {secs}s"
    if minutes:
        return f"{minutes}m {secs}s"
    return f"{secs}s"

st.title(f"🏠 {APP_NAME}")
st.caption(f"v{APP_VERSION} · Client: {CLIENT_NAME} · Engagement {ENGAGEMENT_CODE}")

st.write(
    "Enterprise multi-modal AI platform: text intelligence, image understanding, "
    "document analysis, prompt optimization, embeddings, model/pipeline explorers, "
    "Responsible AI, and AI infrastructure — in a single application."
)

implemented_count = sum(1 for m in MODULES if m.get("implemented"))

col1, col2, col3 = st.columns(3)
col1.metric("Modules", len(MODULES))
col2.metric("Implemented", implemented_count)
col3.metric("Pass mark", "70 / 100")

st.divider()

st.subheader("System status")
device = device_summary()
cached = loaded_pipelines()
status = {
    **device,
    "python_version": platform.python_version(),
    "app_uptime": _format_uptime(time.time() - START_TIME),
    "models_cached": len(cached),
}
st.json(status)
if cached:
    st.caption("Cached models: " + ", ".join(cached))
else:
    st.caption("No models loaded yet — they lazy-load on first use in each module.")

st.divider()

st.subheader("Recent history")
st.info("No runs yet — analyses from every module will be logged here once History (MS-12) ships.")

st.divider()

st.subheader("Module status")
sections: dict[str, list[dict]] = {}
for module in MODULES:
    sections.setdefault(module["section"], []).append(module)

for section, mods in sections.items():
    st.markdown(f"**{section}**")
    for m in mods:
        status = "✅ Live" if m.get("implemented") else f"🚧 Planned — {m['milestone']}"
        st.write(f"{m['icon']} {m['title']} — {status}")
