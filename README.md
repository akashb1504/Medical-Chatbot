<h1 align="center">🩺 MediBot — AI Medical Assistant Chatbot</h1>

<p align="center">
  <b>A dual-mode AI chatbot for general medical Q&A and PDF-based medical document analysis.</b><br/>
  Powered by <b>LLaMA 3.1</b> via Groq · <b>Pinecone</b> vector store · <b>HuggingFace</b> embeddings · <b>LangChain</b> RAG pipeline
</p>

<p align="center">
  <a href="https://medical-chatbot-backend.onrender.com/docs" target="_blank">
    <img src="https://img.shields.io/badge/Backend%20API-Live%20on%20Render-46E3B7?style=for-the-badge&logo=render&logoColor=white" alt="Render Badge"/>
  </a>
  &nbsp;
  <a href="https://github.com/akashb1504/Medical-Chatbot" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-Medical--Chatbot-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Badge"/>
  </a>
  &nbsp;
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/>
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Local Setup & Running](#-local-setup--running)
- [Environment Variables](#-environment-variables)
- [Live Deployment](#-live-deployment)
- [API Reference](#-api-reference)
- [Disclaimer](#-disclaimer)

---

## 🔍 Overview

**MediBot** is a full-stack AI medical assistant that works in two modes:

| Mode | Trigger | How it works |
|------|---------|--------------|
| 🔵 **General Medical Mode** | Default (no PDF uploaded) | Answers general health questions using LLaMA 3.1. Refuses non-medical questions. |
| 🟢 **PDF-Assisted Mode (RAG)** | After uploading a PDF | Retrieves relevant chunks from your document via Pinecone, then generates a grounded answer with source citations. |

Every response includes a ⚠️ medical disclaimer reminding users this is informational only.

---

## ✨ Features

- 💬 **General Medical Q&A** — Ask any health question without uploading anything
- 📄 **PDF Upload + RAG** — Upload medical PDFs and get answers grounded in your documents
- 📌 **Source Citations** — In RAG mode, see exactly which document the answer came from
- ⚠️ **Always-On Disclaimer** — Medical disclaimer displayed on every response
- 🚫 **Off-Topic Refusal** — Bot politely declines non-medical questions
- 🧠 **LLaMA 3.1 via Groq** — Fast inference with the latest open-source LLM
- 🔒 **Memory-Safe** — Uses HuggingFace Inference API for embeddings (no local model loading, works on 512MB servers)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Streamlit Cloud (Frontend)              │
│  client/app.py                                          │
│    ├── Sidebar: PDF Upload + Mode Badge                 │
│    ├── Disclaimer Banner (always shown)                 │
│    └── Chat Interface                                   │
└────────────────────┬────────────────────────────────────┘
                     │  HTTP POST /ask/  (use_rag=True/False)
                     │  HTTP POST /upload_pdfs/
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Render (Backend — FastAPI)              │
│  server/main.py                                         │
│    ├── /ask/ with use_rag=False                         │
│    │     └── LLaMA 3.1 (Groq) — General medical mode   │
│    ├── /ask/ with use_rag=True                          │
│    │     ├── HF Inference API → embed query             │
│    │     ├── Pinecone → retrieve top-3 chunks           │
│    │     └── LLaMA 3.1 (Groq) → grounded answer        │
│    └── /upload_pdfs/                                    │
│          ├── PyPDF → load & split into chunks           │
│          ├── HF Inference API → embed chunks (batched)  │
│          └── Pinecone → upsert vectors (batched)        │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit |
| **Backend** | FastAPI + Uvicorn |
| **LLM** | LLaMA 3.1 8B Instant via [Groq](https://groq.com) |
| **Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` via [HuggingFace Inference API](https://huggingface.co/inference-api) |
| **Vector Store** | [Pinecone](https://pinecone.io) (Serverless, AWS us-east-1) |
| **RAG Framework** | LangChain |
| **PDF Parsing** | PyPDF |
| **Deployment** | Render (backend) + Streamlit Cloud (frontend) |

---

## 📁 Project Structure

```
Medical-Chatbot/
├── client/                         # Streamlit frontend
│   ├── app.py                      # Main Streamlit app entry point
│   ├── config.py                   # API URL config (reads from env var)
│   ├── requirements.txt            # Frontend dependencies
│   ├── components/
│   │   ├── chatUI.py               # Chat interface with disclaimer & mode indicator
│   │   ├── upload.py               # PDF uploader + sidebar mode badge
│   │   └── history_download.py     # Chat history download
│   └── utils/
│       └── api.py                  # HTTP client functions for the backend
│
├── server/                         # FastAPI backend
│   ├── main.py                     # FastAPI app, routes, middleware
│   ├── requirements.txt            # Backend dependencies
│   ├── logger.py                   # Logging setup
│   ├── .env                        # ⚠️ NOT committed — add your keys here locally
│   ├── uploaded_docs/              # Temp storage for uploaded PDFs (auto-cleaned)
│   ├── modules/
│   │   ├── llm.py                  # LLM chains (general mode + RAG mode)
│   │   ├── load_vectorstore.py     # PDF processing + Pinecone upsert (batched)
│   │   ├── query_handlers.py       # RAG chain execution
│   │   └── pdf_handlers.py         # PDF utilities
│   ├── routes/
│   │   ├── ask_question.py         # POST /ask/ — routes between general & RAG mode
│   │   └── upload_pdfs.py          # POST /upload_pdfs/
│   └── middlewares/
│       └── exception_handlers.py   # Global error handling
│
├── .gitignore
└── README.md
```

---

## 💻 Local Setup & Running

### Prerequisites

- Python 3.11+
- API keys for: **Groq**, **Pinecone**, **HuggingFace**

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
# On macOS/Linux:
source .venv/bin/activate

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
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

> **Where to get the keys:**
> - **Groq** → [console.groq.com](https://console.groq.com) (free tier available)
> - **Pinecone** → [app.pinecone.io](https://app.pinecone.io) (free Serverless tier — create an index named `medicalindex` with dimension `384` and metric `dotproduct`)
> - **HuggingFace** → [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) (free, needs Inference API access)

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

Update `client/config.py` to point to your local backend:

```python
# client/config.py
import os
API_URL = os.getenv("MEDIBOT_API_URL", "http://127.0.0.1:8000")
```

### 6. Start the Frontend

```bash
# From inside the client/ directory
streamlit run app.py
```

Frontend will open at: `http://localhost:8501`

---

## 🔑 Environment Variables

### Backend (`server/.env`)

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Groq API key for LLaMA 3.1 inference | ✅ |
| `PINECONE_API_KEY` | Pinecone API key for vector storage | ✅ |
| `PINECONE_INDEX_NAME` | Name of your Pinecone index (default: `medicalindex`) | ✅ |
| `HUGGINGFACE_API_KEY` | HuggingFace token for Inference API embeddings | ✅ |

### Frontend (Streamlit Cloud Secrets or local env)

| Variable | Description |
|----------|-------------|
| `MEDIBOT_API_URL` | URL of the deployed backend (e.g. `https://medical-chatbot-backend.onrender.com`) |

---

## 🌐 Live Deployment

| Service | URL |
|---------|-----|
| **Backend API (Render)** | https://medical-chatbot-backend.onrender.com |
| **API Docs (Swagger UI)** | https://medical-chatbot-backend.onrender.com/docs |

> ⏱️ **Note:** The backend is hosted on Render's free tier, which spins down after 15 minutes of inactivity. The first request after inactivity may take **20–30 seconds** to wake up. Subsequent requests are fast.

---

## 📡 API Reference

### `POST /ask/`

Ask a medical question in either general or RAG mode.

**Form fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `question` | `string` | required | The medical question to ask |
| `use_rag` | `boolean` | `false` | Set `true` to use uploaded PDF context |

**Response:**

```json
{
  "response": "Diabetes symptoms include increased thirst, frequent urination...\n⚠️ This is general medical information only...",
  "sources": ["DIABETES.pdf"],
  "mode": "rag"
}
```

| Field | Description |
|-------|-------------|
| `response` | The answer text (always includes disclaimer) |
| `sources` | List of source PDF filenames (empty in general mode) |
| `mode` | `"general"` or `"rag"` |

---

### `POST /upload_pdfs/`

Upload one or more PDF files to be embedded and stored in Pinecone.

**Form fields:**

| Field | Type | Description |
|-------|------|-------------|
| `files` | `List[UploadFile]` | One or more PDF files |

**Response:**

```json
{
  "messages": "Files processed and vectorstore updated"
}
```

---

## ⚠️ Disclaimer

**MediBot is for informational and educational purposes only.**

This chatbot does **not** provide medical advice, diagnosis, or treatment recommendations. Always consult a qualified healthcare professional for any medical concerns. Never disregard professional medical advice or delay seeking it because of something this chatbot says.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/akashb1504">akashb1504</a>
</p>
