#!/bin/bash
#!/bin/bash
# start_server.sh - Inicia el servidor FastAPI del RAG

set -e
cd "$(dirname "$0")"

echo "🚀 AIHack RAG Server v2"
echo "="

# Verificar que ChromaDB existe
if [ ! -d "rag/chroma_db" ]; then
    echo "❌ ChromaDB no encontrado. Ejecutando indexación..."
    PYTHONSTARTUP= python3 rag/ingest/ingest.py
fi

# Verificar que Ollama está accesible
OLLAMA_URL=${OLLAMA_URL:-"http://localhost:11434"}
echo "🔗 Verificando Ollama..."
if ! timeout 5 curl -s "$OLLAMA_URL/api/tags" > /dev/null 2>&1; then
    echo "⚠️  Ollama no está disponible en $OLLAMA_URL"
    echo "   Para análisis completo, configura OLLAMA_URL en .env"
fi

echo "🌐 Iniciando servidor en http://localhost:8000"
echo "   Health check: curl http://localhost:8000/health"
echo "   Documentación: http://localhost:8000/docs"
echo ""

# Iniciar servidor con PYTHONSTARTUP vacío para evitar problemas de VS Code
PYTHONSTARTUP= python3 -m uvicorn api.server:app --reload --host 0.0.0.0 --port 8000
    echo "   Asegúrate de que Ollama está corriendo en el servidor de IA (Nobara)"
    echo "   O configura OLLAMA_URL para apuntar a la dirección correcta"
fi

# Verificar dependencias Python
echo "📦 Verificando dependencias..."
python3 -c "import fastapi, chromadb, sentence_transformers" 2>/dev/null || {
    echo "Instalando dependencias faltantes..."
    pip install -q fastapi uvicorn chromadb sentence-transformers requests
}

# Iniciar el servidor
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-8000}

echo ""
echo "✅ Iniciando servidor en http://$HOST:$PORT"
echo "📚 Documentos indexados en RAG: $(python3 -c 'import chromadb; c = chromadb.PersistentClient("rag/chroma_db"); print(c.get_collection("pentesting_knowledge").count())' 2>/dev/null || echo "?") fragmentos"
echo ""
echo "📝 Endpoints disponibles:"
echo "   GET  /health           - Estado del servidor"
echo "   POST /analyze          - Analizar consulta de seguridad"
echo ""

python3 -m uvicorn api.server:app --reload --host "$HOST" --port "$PORT"
