# tasks.py
from celery import Celery
from embeddings import build_vector_store
from utils import chunk_text
from pdf_parser import parse_pdf
import os

celery_app = Celery(
    "worker",
    broker="memory://",
    backend="rpc://"
)

@celery_app.task
def process_file_task(file_path):
    try:
        text = parse_pdf(file_path)

        chunks = chunk_text(text)

        persist_path = os.path.splitext(file_path)[0] + "_store.pkl"
        build_vector_store(chunks, persist_path)

        return {"status": "success", "message": f"Embeddings stored at {persist_path}"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
