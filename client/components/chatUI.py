import streamlit as st
from utils.api import ask_question


def render_chat():
    use_rag = st.session_state.get("pdf_uploaded", False)

    # Disclaimer banner 
    st.warning(
        "⚠️ **Medical Disclaimer:** This chatbot provides **general health information only** "
        "and is **not a substitute for professional medical advice, diagnosis, or treatment.** "
        "Always consult a qualified healthcare provider for medical concerns.",
        icon="🏥"
    )

    # Mode indicator
    if use_rag:
        st.success("🟢 **PDF-Assisted Mode** — Answers are based on your uploaded medical documents.")
    else:
        st.info("🔵 **General Medical Mode** — Ask any general health or medical question.")

    st.subheader("💬 Chat with MediBot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render existing chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                st.markdown("📄 **Sources (from your documents):**")
                for src in msg["sources"]:
                    st.markdown(f"- `{src}`")

    # Input and response
    user_input = st.chat_input("Ask a medical question…")
    if user_input:
        # Display user message
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Call backend
        with st.spinner("MediBot is thinking…"):
            response = ask_question(user_input, use_rag=use_rag)

        if response.status_code == 200:
            data = response.json()
            answer = data["response"]
            sources = data.get("sources", [])
            mode = data.get("mode", "general")

            with st.chat_message("assistant"):
                st.markdown(answer)
                if mode == "rag" and sources:
                    st.markdown("📄 **Sources (from your documents):**")
                    for src in sources:
                        st.markdown(f"- `{src}`")

            # Store in history (include sources only for RAG mode)
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources if mode == "rag" else []
            })
        else:
            st.error(f"Error from server: {response.text}")
