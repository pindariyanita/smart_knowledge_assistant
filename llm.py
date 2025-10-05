import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

def call_gemini(prompt: str, context: str = "") -> str:
    model = genai.GenerativeModel(MODEL)
    response = model.generate_content([{"text": f"Context:\n{context}\n\nQuestion: {prompt}"}])
    return response.text
