#!/usr/bin/env python3
"""Script de indexación para AIHack RAG - Versión simplificada"""

import os
import chromadb
from sentence_transformers import SentenceTransformer

SOURCES_DIR = os.path.join(os.path.dirname(__file__), "sources")
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")

def load_documents_safely():
    """Carga documents de forma robusta, saltando archivos problemáticos"""
    docs = []
    errors = 0

    # Buscar todos los .txt y .md usando os.walk
    files = []
    for root, dirs, filenames in os.walk(SOURCES_DIR):
        for filename in filenames:
            if filename.endswith(('.txt', '.md')):
                files.append(os.path.join(root, filename))

    print(f"📂 Encontrados {len(files)} archivos para procesar...")

    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if content.strip() and len(content) > 50:  # Solo si no está vacío y tiene contenido mínimo
                    rel_path = os.path.relpath(filepath, SOURCES_DIR)
                    doc = {
                        "content": content,
                        "metadata": {"source": rel_path}
                    }
                    docs.append(doc)
        except Exception as e:
            errors += 1
            if errors < 5:  # Solo mostrar primeros 5 errores
                print(f"⚠️  Saltando: {os.path.relpath(filepath, SOURCES_DIR)} ({type(e).__name__})")

    if errors > 0:
        print(f"⚠️  {errors} archivos saltados por errores")

    print(f"✅ {len(docs)} documentos cargados correctamente")
    return docs

def split_documents(docs, chunk_size=500, overlap=50):
    """Divide documentos en fragmentos con overlap"""
    chunks = []
    for doc in docs:
        content = doc['content']
        for i in range(0, len(content), chunk_size - overlap):
            chunk_content = content[i:i+chunk_size]
            if chunk_content.strip():
                chunks.append({
                    "content": chunk_content,
                    "metadata": doc['metadata']
                })
    return chunks

def ingest():
    print("📂 Cargando documentos...")

    docs = load_documents_safely()

    if len(docs) == 0:
        print("⚠️  No hay archivos válidos en rag/ingest/sources/.")
        return

    print("✂️  Generando fragmentos...")
    chunks = split_documents(docs)
    print(f"✂️  {len(chunks)} fragmentos generados")

    print("🧠 Inicializando modelo de embeddings...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print("🗃️ Inicializando ChromaDB...")
    os.makedirs(CHROMA_DIR, exist_ok=True)

    client = chromadb.PersistentClient(path=os.path.abspath(CHROMA_DIR))

    # Crear o conseguir la colección
    collection = client.get_or_create_collection(
        name="pentesting_knowledge"
    )

    print(f"📝 Indexando {len(chunks)} fragmentos...")

    # Procesar en batches pequeños para evitar problemas de memoria
    batch_size = 50  # Batch más pequeño para estabilidad
    total_batches = (len(chunks) + batch_size - 1) // batch_size

    chunk_id = 0
    for i in range(0, len(chunks), batch_size):
        batch_num = i // batch_size + 1
        batch = chunks[i:i+batch_size]

        # Preparar datos para ChromaDB
        ids = [f"chunk_{chunk_id + j}" for j in range(len(batch))]
        metadatas = [c['metadata'] for c in batch]
        documents = [c['content'] for c in batch]

        # Generar embeddings para este batch
        embeddings = model.encode(documents).tolist()

        # Añadir a la colección
        collection.add(
            ids=ids,
            metadatas=metadatas,
            documents=documents,
            embeddings=embeddings
        )

        chunk_id += len(batch)
        print(f"  ✅ Lote {batch_num}/{total_batches} completado ({len(batch)} fragmentos)")

    print("✅ Base de conocimiento actualizada correctamente")
    print(f"📊 Total fragmentos indexados: {len(chunks)}")


if __name__ == "__main__":
    ingest()
