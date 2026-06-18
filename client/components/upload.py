import streamlit as st
from utils.api import upload_pdfs_api


def render_uploader():
    st.sidebar.header("📂 Upload Medical Documents")
    uploaded_files = st.sidebar.file_uploader(
        "Upload PDF(s) to enable document-based answers",
        type="pdf",
        accept_multiple_files=True
    )

    if st.sidebar.button("⬆️ Upload & Process") and uploaded_files:
        with st.sidebar.status("Processing PDFs…", expanded=True) as status:
            response = upload_pdfs_api(uploaded_files)
            if response.status_code == 200:
                st.session_state.pdf_uploaded = True
                status.update(label="✅ PDFs processed!", state="complete")
                st.sidebar.success(f"{len(uploaded_files)} file(s) uploaded successfully.")
            else:
                status.update(label="❌ Upload failed", state="error")
                st.sidebar.error(f"Error: {response.text}")

    # Mode badge
    st.sidebar.divider()
    if st.session_state.get("pdf_uploaded", False):
        st.sidebar.success("🟢 **PDF-Assisted Mode** (RAG)\nAnswers are sourced from your uploaded documents.")
    else:
        st.sidebar.info("🔵 **General Medical Mode**\nNo PDFs uploaded. Using general medical knowledge.")
