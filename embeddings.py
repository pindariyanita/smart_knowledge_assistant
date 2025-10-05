from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
import os
import pickle
from dotenv import load_dotenv

load_dotenv()

def get_embeddings_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# --- Build FAISS Vector Store ---
def build_vector_store(chunks, persist_path="vector_store.pkl"):
    embeddings = get_embeddings_model()
    documents = [Document(page_content=chunk) for chunk in chunks]
    vectorstore = FAISS.from_documents(documents, embeddings)

    with open(persist_path, "wb") as f:
        pickle.dump(vectorstore, f)

    return vectorstore

# --- Load Vector Store ---
def load_vector_store(persist_path="vector_store.pkl"):
    if not os.path.exists(persist_path):
        raise FileNotFoundError("Vector store not found. Please create it first.")
    with open(persist_path, "rb") as f:
        return pickle.load(f)

def search(query: str, vectorstore_path="uploads/vector_store.pkl", top_k=3):
    """
    Search the FAISS vector store for the most relevant chunks for a query.
    Returns a list of retrieved text chunks.
    """
    import pickle

    if not os.path.exists(vectorstore_path):
        raise FileNotFoundError("Vector store not found. Create it first using build_vector_store().")

    with open(vectorstore_path, "rb") as f:
        vectorstore = pickle.load(f)

    results = vectorstore.similarity_search(query, k=top_k)
    return [doc.page_content for doc in results]

if __name__ == "__main__":
    from pathlib import Path

    folder = Path("uploads")
    chunks = []

    #for pdf
    for file_path in folder.glob("*.pdf"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                chunks.append(f.read())
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="latin-1") as f:
                chunks.append(f.read())

    if chunks:
        vectorstore = build_vector_store(chunks, persist_path="uploads/vector_store.pkl")
        print("Vector store built successfully!")
    else:
        print("No documents found to build vector store.")

