# AIHack RAG Starter

Proyecto inicial de RAG para AIHack v2.

## Estructura

- `rag/ingest/ingest.py`: carga documentos y crea la base de datos Chroma.
- `rag/ingest/sources/`: coloca tus `.txt` y `.md` para indexar.
- `rag/chroma_db/`: carpeta de persistencia de Chroma.
- `api/server.py`: servidor FastAPI que realiza búsqueda semántica y consulta Ollama.
- `aihack.sh`: wrapper local para enviar consultas al servidor.
- `download_knowledge.sh`: script para clonar fuentes de pentesting en `rag/ingest/sources/`.
- `requirements.txt`: dependencias Python.

## Inicio rápido

1. Instalar dependencias:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
2. Copiar tus archivos `.txt` o `.md` a `rag/ingest/sources/`.
3. Generar embeddings e índice:
   ```bash
   python3 rag/ingest/ingest.py
   ```
4. Iniciar FastAPI:
   ```bash
   uvicorn api.server:app --host 0.0.0.0 --port 8000
   ```
5. Consultar desde terminal:
   ```bash
   ./aihack.sh "¿Qué vulnerabilidades puede indicar este output de Nmap?"
   ```
