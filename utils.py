import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("smartkb")
handler = RotatingFileHandler("app.log", maxBytes=1000000, backupCount=3)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def chunk_text(text, chunk_size=500, overlap=50):
    """
    Split text into overlapping chunks for embedding.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks