from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GENERAL_SYSTEM_PROMPT = """You are MediBot, a knowledgeable and empathetic AI medical information assistant.

Your role is to provide clear, accurate, and helpful GENERAL medical and health information to users.

STRICT RULES:
1. ONLY answer questions related to health, medicine, symptoms, diseases, treatments, medications, anatomy, nutrition, mental health, or wellness.
2. If the user asks something completely unrelated to health or medicine (e.g., coding, jokes, recipes unrelated to health), politely refuse and explain you are a medical information assistant only.
3. ALWAYS end every response with this exact disclaimer on a new line:
   ⚠️ *This is general medical information only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.*
4. Never diagnose a specific condition for the user.
5. Never prescribe specific medications or dosages.
6. Respond in a calm, factual, compassionate, and easy-to-understand tone."""

RAG_PROMPT_TEMPLATE = """You are **MediBot**, an AI-powered assistant trained to help users understand medical documents.

Your job is to answer questions based **strictly on the provided document context** below.

---

🔍 **Context from uploaded documents**:
{context}

🙋 **User Question**:
{question}

---

💬 **Instructions**:
- Answer using ONLY the information found in the context above.
- If the context does not contain a clear answer, say: "I'm sorry, but I couldn't find relevant information in the provided documents."
- Do NOT make up facts or add information from outside the context.
- Use clear, simple language.
- Always end your response with:
  ⚠️ *This is general medical information only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.*
"""


def get_general_llm():
    """Returns a ChatGroq LLM configured for general medical Q&A (no retrieval)."""
    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant"
    )


def answer_general_question(llm, question: str) -> str:
    """Calls the LLM directly with a medical-only system prompt."""
    messages = [
        SystemMessage(content=GENERAL_SYSTEM_PROMPT),
        HumanMessage(content=question)
    ]
    response = llm.invoke(messages)
    return response.content


def get_llm_chain(retriever):
    """Returns a RetrievalQA chain for PDF/RAG mode."""
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant"
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=RAG_PROMPT_TEMPLATE
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
