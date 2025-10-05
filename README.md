# Smart Knowledge Assistant

A FastAPI-based AI-powered knowledge assistant that allows users to upload documents, process them into embeddings, and ask questions to retrieve relevant information using a vector store. Integrates Celery for asynchronous processing and supports Google Gemini API for text generation.

---

## Features

- **User Authentication:** Register and login functionality.
- **File Upload:** Users can upload PDF and TXT documents.
- **Document Processing:** Documents are split into chunks and stored in a vector database (FAISS).
- **Question Answering:** Ask questions and receive answers using embeddings and AI generation.
- **Asynchronous Tasks:** Celery handles document processing in the background.
- **Persistent Vector Store:** Embeddings are saved locally for fast retrieval.

---

## Tech Stack

- **Backend:** FastAPI, Uvicorn
- **Asynchronous Processing:** Celery, Redis
- **Embeddings & Vector Store:** LangChain, FAISS
- **AI Model:** Google Gemini API
- **Python Libraries:** PyPDF2, python-dotenv, redis, google-generativeai and many more

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/smart-knowledge-assistant.git
cd smart-knowledge-assistant

2. Install dependencies

pip install -r requirements.txt

3. Set up environment variables in a .env file

4. Start Celery Worker

  celery -A main.celery_app worker --loglevel=info

5. Run FastAPI with Uvicorn

  uvicorn main:app --reload

6. Go to http://127.0.0.1:8000.docs for Swagger UI, there you will find

  POST /register – Register a new user

  POST /login – Login and receive access token

  POST /upload – Upload documents for processing

  POST /ask – Ask a question about uploaded documents

