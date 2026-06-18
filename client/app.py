import streamlit as st
from components.upload import render_uploader
from components.history_download import render_history_download
from components.chatUI import render_chat


st.set_page_config(
    page_title="MediBot — AI Medical Assistant",
    page_icon="🩺",
    layout="wide"
)
st.title("🩺 MediBot — AI Medical Assistant")
st.caption("Powered by LLaMA 3.1 · General medical information only · Not a substitute for professional advice")

render_uploader()
render_chat()
render_history_download()
