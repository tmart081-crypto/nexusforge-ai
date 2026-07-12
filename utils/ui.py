"""Shared Streamlit UI helpers used across module pages."""

import streamlit as st


def render_placeholder(title: str, description: str, milestone: str) -> None:
    """Standard 'coming soon' body for modules not yet implemented."""
    st.title(title)
    st.info(f"🚧 Coming soon — planned for **{milestone}**.")
    st.write(description)
    st.caption("Placeholder page. Reachable in navigation per Phase 1 requirements.")
