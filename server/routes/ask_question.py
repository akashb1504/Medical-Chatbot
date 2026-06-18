from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from modules.llm import get_llm_chain, get_general_llm, answer_general_question
from modules.query_handlers import query_chain
from modules.load_vectorstore import _get_embed_model
from langchain_core.documents import Document
from langchain.schema import BaseRetriever
from pinecone import Pinecone
from typing import List
from logger import logger
import os


router = APIRouter()


@router.post("/ask/")
async def ask_question(question: str = Form(...), use_rag: bool = Form(False)):
    try:
        logger.info(f"User query: '{question}' | use_rag={use_rag}")

        # GENERAL MODE
        if not use_rag:
            llm = get_general_llm()
            answer = answer_general_question(llm, question)
            logger.info("General mode response generated successfully")
            return {
                "response": answer,
                "sources": [],
                "mode": "general"
            }

        # RAG MODE
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        index = pc.Index(os.environ["PINECONE_INDEX_NAME"])

        embedded_query = next(iter(_get_embed_model().embed([question]))).tolist()
        res = index.query(vector=embedded_query, top_k=3, include_metadata=True)

        docs = [
            Document(
                page_content=match["metadata"].get("text", ""),
                metadata=match["metadata"]
            ) for match in res["matches"]
        ]

        class SimpleRetriever(BaseRetriever):
            docs: List[Document]

            def _get_relevant_documents(self, query: str) -> List[Document]:
                return self.docs

        retriever = SimpleRetriever(docs=docs)
        chain = get_llm_chain(retriever)
        result = query_chain(chain, question)
        
        response_text = result["response"]


        if "I couldn't find relevant information" in response_text or "I'm sorry, but I couldn't find" in response_text:
            logger.info("RAG couldn't find the answer. Falling back to General LLM.")
            llm = get_general_llm()
            fallback_answer = answer_general_question(llm, question)
            return {
                "response": fallback_answer,
                "sources": [],
                "mode": "general (fallback)"
            }


        raw_sources = [doc.metadata.get("source", "") for doc in docs]
        unique_sources = list(dict.fromkeys(
            os.path.basename(s) for s in raw_sources if s
        ))

        logger.info("RAG mode response generated successfully")
        return {
            "response": response_text,
            "sources": unique_sources,
            "mode": "rag"
        }

    except Exception as e:
        logger.exception("Error processing question")
        return JSONResponse(status_code=500, content={"error": str(e)})
