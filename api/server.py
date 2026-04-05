import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title="AIHack RAG Server", version="2.0")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHROMA_DIR = os.path.join(BASE_DIR, "rag", "chroma_db")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3")

# Inicializar variables globales (lazy loading)
chroma_client = None
embedding_model = None
collection = None

def get_chroma_client():
    global chroma_client, embedding_model, collection
    if chroma_client is None:
        print("🔧 Inicializando ChromaDB...")
        chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
        print("🧠 Cargando modelo de embeddings...")
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        
        try:
            collection = chroma_client.get_collection(name="pentesting_knowledge")
            print("✅ ChromaDB listo")
        except:
            collection = None
            print("❌ Colección no encontrada")
    
    return collection


class HackRequest(BaseModel):
    query: str
    top_k: int = 3


class HealthResponse(BaseModel):
    status: str
    rag_ready: bool
    documents_indexed: int


@app.get("/health", response_model=HealthResponse)
def health():
    collection = get_chroma_client()
    rag_ready = collection is not None
    doc_count = 0
    if rag_ready:
        try:
            doc_count = collection.count()
        except:
            doc_count = 0
    
    return {
        "status": "online",
        "rag_ready": rag_ready,
        "documents_indexed": doc_count
    }


@app.post("/search")
def search(req: HackRequest):
    """Búsqueda de conocimiento sin pasar por Ollama - respuesta rápida"""
    collection = get_chroma_client()
    if collection is None:
        raise HTTPException(status_code=503, detail="RAG no está inicializado.")
    
    try:
        # Generar embeddings para la query
        query_embedding = embedding_model.encode(req.query).tolist()
        
        # Buscar documentos similares
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=req.top_k
        )
        
        # Preparar respuesta
        documents = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        
        search_results = []
        for doc, distance, metadata in zip(documents, distances, metadatas):
            relevance = max(0, 1 - distance)  # Convertir distance a relevance score
            search_results.append({
                "content": doc[:300] + ("..." if len(doc) > 300 else ""),
                "source": metadata.get("source", "unknown"),
                "relevance": f"{relevance*100:.1f}%"
            })
        
        return {
            "query": req.query,
            "results": search_results,
            "total_found": len(search_results)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de búsqueda: {str(e)}")


@app.post("/analyze")
def analyze(req: HackRequest):
    print(f"🔍 Analyzing query: {req.query}")
    collection = get_chroma_client()
    if collection is None:
        print("❌ RAG not ready")
        raise HTTPException(status_code=503, detail="RAG no está listo. ChromaDB vacío o no inicializado.")
    
    try:
        print("🧠 Generating embeddings...")
        # Generar embeddings para la query
        query_embedding = embedding_model.encode(req.query).tolist()
        
        print("🔍 Searching ChromaDB...")
        # Buscar documentos similares
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=req.top_k
        )
        
        # Extraer contexto limitado
        documents = results.get("documents", [[]])[0][:req.top_k]
        context = "\n\n".join([doc[:500] for doc in documents])  # Limitar cada doc a 500 chars
        
        if not context:
            context = "[No se encontraron documentos relevantes en la base de conocimiento]"
        
        print(f"📝 Context length: {len(context)}")
        print(f"🤖 Calling Ollama at: {OLLAMA_URL}")
        
        # Generar prompt más corto
        prompt = f"""Contexto: {context[:1000]}

Pregunta: {req.query}

Responde como experto en ciberseguridad:"""
        
        print("📡 Sending to Ollama...")
        # Consultar Ollama
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        print(f"📡 Ollama response status: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        
        print("✅ Analysis complete")
        return {
            "response": data.get("response", "Error: sin respuesta del modelo"),
            "context_used": context[:500] + ("..." if len(context) > 500 else ""),
            "documents_found": len(results.get("documents", [[]])[0])
        }
    
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {e}")
        raise HTTPException(status_code=503, detail="Ollama no está disponible. Asegúrate de que está corriendo en localhost:11434")
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/health")
def health():
    return {"status": "online", "rag": "active"}
