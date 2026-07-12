"""NexusForge AI Platform entrypoint.

Run with: streamlit run main.py
"""

import streamlit as st

from config.modules import MODULES
from config.settings import APP_NAME
from utils.logger import get_logger

log = get_logger("main")

st.set_page_config(page_title=APP_NAME, page_icon="🧠", layout="wide")

sections: dict[str, list[st.Page]] = {}
for module in MODULES:
    page = st.Page(
        module["page"],
        title=module["title"],
        icon=module["icon"],
        default=module.get("default", False),
    )
    sections.setdefault(module["section"], []).append(page)

nav = st.navigation(sections)
log.info("App shell loaded with %d modules across %d sections", len(MODULES), len(sections))
nav.run()
