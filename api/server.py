import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

app = FastAPI()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHROMA_DIR = os.path.join(BASE_DIR, "rag", "chroma_db")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)


class HackRequest(BaseModel):
    query: str


@app.post("/analyze")
def analyze(req: HackRequest):
    results = db.similarity_search(req.query, k=3)
    context = "\n\n".join([r.page_content for r in results])

    prompt = f"""Eres un asistente experto en ciberseguridad y pentesting.

Contexto relevante de tu base de conocimiento:
---
{context}
---

Analiza la siguiente consulta y responde con recomendaciones prácticas, riesgos y próximos pasos:

{req.query}
"""
    response = requests.post(OLLAMA_URL, json={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    })
    response.raise_for_status()
    data = response.json()
    return {
        "response": data.get("response", ""),
        "context_used": context[:1000] + ("..." if len(context) > 1000 else "")
    }


@app.get("/health")
def health():
    return {"status": "online", "rag": "active"}
