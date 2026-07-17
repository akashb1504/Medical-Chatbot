<h1 align="center">🩺 MediBot — AI Medical Assistant Chatbot</h1>

<p align="center">
  <b>A dual-mode AI chatbot for general medical Q&A and PDF-based medical document analysis.</b><br/>
  Powered by <b>LLaMA 3.1</b> via Groq · <b>Pinecone</b> vector store · <b>FastEmbed</b> embeddings · <b>LangChain</b> RAG pipeline
</p>

<p align="center">
  <a href="https://medical-chatbot-fhukbyptnm5s8dszi47h4h.streamlit.app/" target="_blank">
    <img src="https://img.shields.io/badge/🩺%20Try%20MediBot%20Live-Streamlit%20App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit App"/>
  </a>
  &nbsp;
  <a href="https://github.com/akashb1504/Medical-Chatbot" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-Medical--Chatbot-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Badge"/>
  </a>
  &nbsp;
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/>
</p>



## 🔍 Overview

**MediBot** is a full-stack AI medical assistant that works in two modes:

| Mode | Trigger | How it works |
|------|---------|--------------|
| 🔵 **General Medical Mode** | Default (no PDF uploaded) | Answers general health questions using LLaMA 3.1. |
| 🟢 **PDF-Assisted Mode (RAG)** | After uploading a PDF | Retrieves relevant chunks from your document via Pinecone, then generates a grounded answer with source citations. |

A medical disclaimer is shown on the page reminding users this is informational only, not medical advice.

---

## ✨ Features

- 💬 **General Medical Q&A** — Ask any health question without uploading anything
- 📄 **PDF Upload + RAG** — Upload medical PDFs and get answers grounded in your documents
- 📌 **Source Citations** — In RAG mode, see exactly which document and page the answer came from
- 🔒 **Session-Based Isolation** — Each user session has its own `session_id`, which is used to filter Pinecone queries so one user's uploaded PDFs never leak into another user's answers
- ⚠️ **Medical Disclaimer** — Displayed on the page as a reminder that responses are educational, not medical advice
- 🧠 **LLaMA 3.1 via Groq** — Fast inference with the latest open-source LLM


---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit |
| **Backend** | FastAPI + Uvicorn |
| **LLM** | LLaMA 3.1 8B Instant via Groq |
| **Embeddings** | FastEmbed (BAAI/bge-small-en-v1.5) |
| **Vector Store** | Pinecone |
| **RAG Framework** | LangChain |
| **PDF Parsing** | PyPDF |
| **Deployment** | Render (backend) + Streamlit Cloud (frontend) |

---

## 💻 Local Setup & Running

### Prerequisites

- Python 3.11+
- API keys for: **Groq**, **Pinecone**

### 1. Clone the Repository

```bash
git clone https://github.com/akashb1504/Medical-Chatbot.git
cd Medical-Chatbot
```

### 2. Set Up the Backend

```bash
cd server

# Create and activate virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file inside the `server/` folder:

```bash
# server/.env
GROQ_API_KEY=your_groq_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=medicalindex
```

### 4. Start the Backend Server

```bash
# From inside the server/ directory (with venv activated)
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Backend will be live at: `http://127.0.0.1:8000`
Swagger docs at: `http://127.0.0.1:8000/docs`

### 5. Set Up the Frontend

Open a **new terminal** in the project root:

```bash
cd client

# Install dependencies
pip install -r requirements.txt
```

The `client/config.py` already defaults to localhost when `MEDIBOT_API_URL` is not set:

```python
# client/config.py  (no changes needed for local dev)
import os
API_URL = os.getenv("MEDIBOT_API_URL", "http://127.0.0.1:8000")
```

### 6. Start the Frontend

```bash
# From inside the client/ directory
streamlit run app.py
```

Frontend will open at: `http://localhost:8501`



## 🌐 Live Deployment

### 🎯 User-Facing App

> **[👉 Open MediBot on Streamlit](https://medical-chatbot-fhukbyptnm5s8dszi47h4h.streamlit.app/)**

Just open the link and start asking medical questions — no sign-in needed.
