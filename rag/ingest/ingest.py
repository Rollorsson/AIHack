import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

SOURCES_DIR = os.path.join(os.path.dirname(__file__), "sources")
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")


def ingest():
    print("📂 Cargando documentos...")

    loaders = [
        DirectoryLoader(SOURCES_DIR, glob="**/*.txt", loader_cls=TextLoader),
        DirectoryLoader(SOURCES_DIR, glob="**/*.md", loader_cls=TextLoader),
    ]

    docs = []
    for loader in loaders:
        docs.extend(loader.load())

    print(f"✅ {len(docs)} documentos encontrados")
    if len(docs) == 0:
        print("⚠️  No hay archivos .txt o .md en rag/ingest/sources/. Agrega documentos y vuelve a ejecutar.")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    print(f"✂️  {len(chunks)} fragmentos generados")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=os.path.abspath(CHROMA_DIR), embedding_function=embeddings)
    db.add_documents(chunks)
    db.persist()
    print("🧠 Base de conocimiento actualizada correctamente")


if __name__ == "__main__":
    ingest()
