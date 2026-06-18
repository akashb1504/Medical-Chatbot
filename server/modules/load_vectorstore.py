import os
import time
import gc
import threading
from pathlib import Path
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from fastembed import TextEmbedding

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = "us-east-1"
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "medicalindex")


PROCESS_BATCH_SIZE = 32

_embed_model = None
_embed_model_lock = threading.Lock()


def _get_embed_model() -> TextEmbedding:
    """Return the fastembed singleton, initialising it on first call."""
    global _embed_model
    if _embed_model is None:
        with _embed_model_lock:        
            if _embed_model is None:
                print("[fastembed] Loading BAAI/bge-small-en-v1.5 model...")
                _embed_model = TextEmbedding(
                    model_name="BAAI/bge-small-en-v1.5",
                    cache_dir=os.getenv("FASTEMBED_CACHE_PATH", None),
                )
                print("[fastembed] Model ready.")
    return _embed_model

UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


pc = Pinecone(api_key=PINECONE_API_KEY)
spec = ServerlessSpec(cloud="aws", region=PINECONE_ENV)
existing_indexes = [i["name"] for i in pc.list_indexes()]

if PINECONE_INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=384,
        metric="dotproduct",
        spec=spec
    )
    while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
        time.sleep(1)

index = pc.Index(PINECONE_INDEX_NAME)


def _embed_texts(texts: list) -> list:
    """
    Embed a list of texts using the fastembed lazy singleton.
    Returns a plain list of float vectors.
    """
    model = _get_embed_model()
    return [vec.tolist() for vec in model.embed(texts)]


def load_vectorstore(uploaded_files):
    """
    Process uploaded PDFs and store embeddings in Pinecone.

    Memory strategy — stream in PROCESS_BATCH_SIZE chunks at a time:
      load pages → split → embed (fastembed) → upsert → discard
    Peak RAM stays flat regardless of PDF size, well within Render's 512 MB.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR) / file.filename
        print(f"\nProcessing: {file.filename}")


        with open(save_path, "wb") as f:
            for chunk_bytes in iter(lambda: file.file.read(65536), b""):
                f.write(chunk_bytes)

        try:

            loader = PyPDFLoader(str(save_path))
            pages = loader.load()
            print(f"  Loaded {len(pages)} pages")


            all_chunks = splitter.split_documents(pages)
            total_chunks = len(all_chunks)
            print(f"  Split into {total_chunks} chunks — processing in batches of {PROCESS_BATCH_SIZE}")


            del pages
            gc.collect()

            chunk_index = 0 


            for batch_start in range(0, total_chunks, PROCESS_BATCH_SIZE):
                batch_chunks = all_chunks[batch_start: batch_start + PROCESS_BATCH_SIZE]

                texts = [c.page_content for c in batch_chunks]
                metadatas = [
                    {**c.metadata, "text": c.page_content}
                    for c in batch_chunks
                ]
                ids = [
                    f"{save_path.stem}-{chunk_index + j}"
                    for j in range(len(batch_chunks))
                ]
                chunk_index += len(batch_chunks)


                embeddings = _embed_texts(texts)


                vectors = list(zip(ids, embeddings, metadatas))
                index.upsert(vectors=vectors)
                print(f"  Upserted {min(batch_start + PROCESS_BATCH_SIZE, total_chunks)}/{total_chunks} chunks")


                del batch_chunks, texts, metadatas, ids, embeddings, vectors
                gc.collect()

            print(f"  Done: {file.filename}")

        finally:

            if save_path.exists():
                save_path.unlink()
            gc.collect()
