import os

try:
    import streamlit as st
    # Streamlit Cloud: secrets defined in the app dashboard (Settings → Secrets)
    API_URL = st.secrets.get("BACKEND_URL") or st.secrets.get("MEDIBOT_API_URL")
    if not API_URL:
        raise KeyError
except (KeyError, AttributeError, Exception):
    # Local dev fallback: set BACKEND_URL in a .env or environment
    API_URL = os.getenv("BACKEND_URL") or os.getenv("MEDIBOT_API_URL", "https://medical-chatbot-backend-blly.onrender.com")
