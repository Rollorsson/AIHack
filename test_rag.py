#!/usr/bin/env python3
"""Test rápido del RAG antes de lanzar el servidor"""

import os
import sys
from pathlib import Path

# Agregar el path al proyecto
sys.path.insert(0, str(Path(__file__).parent))

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

CHROMA_DIR = "rag/chroma_db"
MODEL_NAME = "all-MiniLM-L6-v2"

def test_rag():
    print("🧪 Test del RAG...")
    print("=" * 60)
    
    # Inicializar embeddings
    print("📚 Cargando modelo de embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    
    # Conectar a ChromaDB
    print(f"🔗 Conectando a ChromaDB... {CHROMA_DIR}")
    db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    
    # Verificar que la BD no está vacía
    collection = db._collection
    total_docs = collection.count()
    print(f"📊 Total de documentos indexados: {total_docs}")
    
    if total_docs == 0:
        print("❌ ERROR: ChromaDB está vacío")
        return False
    
    # Hacer una búsqueda de prueba
    test_query = "SQL injection vulnerability"
    print(f"\n🔍 Búsqueda de prueba: '{test_query}'")
    
    results = db.similarity_search(test_query, k=3)
    
    print(f"✅ Se encontraron {len(results)} resultados relevantes:")
    for i, result in enumerate(results, 1):
        source = result.metadata.get("source", "unknown")
        snippet = result.page_content[:100].replace("\n", " ")
        print(f"\n  [{i}] Fuente: {source}")
        print(f"      Preview: {snippet}...")
    
    print("\n✅ RAG funcionando correctamente")
    return True

if __name__ == "__main__":
    try:
        success = test_rag()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
