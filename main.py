from fastapi import FastAPI, UploadFile, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import SessionLocal, User, QueryHistory
import auth, schemas
from tasks import process_file_task
from embeddings import search
from llm import call_gemini
from utils import logger
import os

app = FastAPI(title="Smart Knowledge Assistant API", version="1.0.0")

@app.post("/register", response_model=schemas.Token)
def register(user: schemas.UserCreate):
    db = SessionLocal()
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="User exists")
    hashed = auth.get_password_hash(user.password)
    new_user = User(email=user.email, password=hashed)
    db.add(new_user); db.commit()
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not auth.verify_password(form.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/upload")
def upload_file(file: UploadFile, user=Depends(auth.get_current_user)):
    if not file.filename.endswith((".pdf", ".txt", ".md")):
        raise HTTPException(status_code=400, detail="Invalid format")
    
    os.makedirs("uploads", exist_ok=True)
    path = os.path.join("uploads", f"temp_{file.filename}")
    with open(path, "wb") as f:
        f.write(file.file.read())
    process_file_task.delay(path)
    logger.info(f"{user} uploaded {file.filename}")
    return {"message": "File received, embedding in background"}

@app.post("/ask")
def ask_question(req: schemas.AskRequest, user=Depends(auth.get_current_user)):
    context_chunks = search(req.question)
    context = "\n".join(context_chunks)
    answer = call_gemini(req.question, context)
    db = SessionLocal()
    db.add(QueryHistory(user=user, question=req.question, answer=answer))
    db.commit()
    return {"answer": answer}
