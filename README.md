# 🤖 AIHack Copilot v2 — Sistema de Ciberseguridad con IA Local

> Un copiloto inteligente para pentesting y análisis de seguridad, con memoria persistente y base de conocimiento especializada.

[![Estado](https://img.shields.io/badge/Estado-Activo-brightgreen)](https://github.com/usuario/aihack)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)](https://fastapi.tiangolo.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.4+-purple)](https://www.trychroma.com/)

---

## 🎯 ¿Qué es AIHack?

AIHack es un sistema de ciberseguridad asistido por IA que combina:

- **Análisis inteligente** de outputs de herramientas de red (Nmap, etc.)
- **Base de conocimiento RAG** con payloads, exploits y técnicas de pentesting
- **IA local** (Ollama) para análisis sin dependencias de internet
- **Memoria persistente** para consultas contextuales
- **Acceso remoto** seguro desde cualquier dispositivo

### Comando principal
```bash
aihack "$(nmap -sV target)"
```

---

## 🏗️ Arquitectura

```
ThinkPad (Parrot OS) / Browser / Teléfono
    └── UI Web (Fase 3)
        └── FastAPI Server (Nobara OS)
            ├── ChromaDB (RAG Vector Database)
            │   ├── PayloadsAllTheThings
            │   ├── HackTricks
            │   ├── OSCP Notes
            │   ├── CTF Writeups
            │   ├── GTFOBins
            │   └── Ethical Hacking Cheatsheets
            └── Ollama (LLM Local)
                └── Llama3 / otros modelos
```

### Componentes principales

| Componente | Tecnología | Función |
|------------|------------|---------|
| **Servidor API** | FastAPI + Python | Orquestador principal |
| **Base RAG** | ChromaDB | Vector database con embeddings |
| **Modelo LLM** | Ollama | IA local para análisis |
| **Embeddings** | Sentence Transformers | all-MiniLM-L6-v2 |
| **CLI** | Bash + Python | Interfaz de línea de comandos |
| **Conocimiento** | Markdown repos | Base de datos especializada |

---

## 🚀 Instalación y Configuración

### Prerrequisitos

- **Python 3.8+**
- **Ollama** (opcional, para análisis completo)
- **Git** para descargar fuentes de conocimiento

### 1. Clonar el proyecto
```bash
git clone https://github.com/usuario/aihack.git
cd aihack
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Descargar base de conocimiento
```bash
# Descarga automática de todas las fuentes
bash download_knowledge.sh
```

### 4. Indexar documentos en RAG
```bash
# Indexa todos los documentos en ChromaDB
python3 rag/ingest/ingest.py
```

### 5. Configurar Ollama (opcional)
```bash
# Instalar Ollama en servidor Nobara
curl -fsSL https://ollama.ai/install.sh | sh

# Descargar modelo
ollama pull llama3

# Editar configuración con IP del servidor
nano .env
# OLLAMA_URL=http://192.168.1.X:11434
```

### 6. Iniciar sistema completo
```bash
# Opción recomendada: Inicia API + Web interface
bash start_all.sh

# O iniciar componentes individuales:
bash start_server.sh    # Solo API server (puerto 8000)
bash start_web.sh        # Solo web interface (puerto 3000)
```

---

## 📖 Uso

### CLI Básica
```bash
# Análisis de output de Nmap
aihack "$(nmap -sV 192.168.1.1)"

# Consulta directa
aihack "SQL injection bypass techniques"

# Búsqueda rápida (sin Ollama)
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "reverse shell payload"}'
```

### Interfaz Web
```bash
# Iniciar servidor web (puerto 3000)
bash start_web.sh

# Abrir en navegador: http://localhost:3000
# La interfaz web se conecta automáticamente al API server en puerto 8000
```

#### Características de la UI Web
- **Diseño Corporate Elegante** Cyberpunk 2077 style con profesionalismo hitech futurista
- **Interfaz Moderna** con glassmorphism, gradientes profesionales y animaciones suaves
- **Búsqueda RAG** en tiempo real en la base de conocimiento especializada
- **Análisis con IA** usando Ollama local para análisis inteligente
- **Diseño Responsive** para móviles, tablets y desktop con paleta corporativa
- **Paleta de Colores Profesional** Azul corporativo (#0080ff), Cyan elegante (#00d4ff), acentos Magenta (#ff006e)
- **Estado de Conexión** en tiempo real al servidor API con indicadores visuales

### API Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
# {"status":"online","rag_ready":true,"documents_indexed":3200}
```

#### Búsqueda Rápida (sin Ollama)
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "XSS payload", "top_k": 3}'
```

#### Análisis Completo (con Ollama)
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "nmap output: 22/tcp open ssh, 80/tcp open http"}'
```

### Ejemplos de uso

#### 1. Análisis de escaneo de red
```bash
# Input
aihack "PORT   STATE SERVICE  VERSION
22/tcp open  ssh      OpenSSH 8.2p1
80/tcp open  http     Apache httpd 2.4.41
443/tcp open https    Apache httpd 2.4.41"

# Output: Análisis de servicios, vulnerabilidades conocidas, próximos pasos
```

#### 2. Consulta de técnicas específicas
```bash
aihack "bypass WAF SQL injection"
# Devuelve payloads, técnicas y referencias de la base de conocimiento
```

#### 3. Búsqueda de payloads
```bash
aihack "reverse shell php one liner"
# Encuentra payloads relevantes en PayloadsAllTheThings
```

---

## 📊 Estado del Proyecto

### ✅ Completado (Fase 1 - RAG & Backend)
- [x] RAG con ChromaDB y embeddings locales (all-MiniLM-L6-v2)
- [x] Base de conocimiento especializada (6 repositorios + adicionales)
- [x] FastAPI server con endpoints REST completos
- [x] CLI funcional con colores y feedback
- [x] Manejo robusto de errores y encoding (UTF-8)
- [x] Scripts de automatización (download, start)
- [x] 1,710 documentos indexados → 52,000+ fragmentos

### ✅ Completado (Fase 2 - Integración Ollama)
- [x] Ollama local con modelo Llama 3 8B
- [x] Endpoint /analyze con procesamiento de contexto RAG
- [x] Manejo de timeouts y fallbacks
- [x] Logs detallados y debugging

### ✅ Completado (Fase 3 - UI Web Corporate)
- [x] Interfaz web moderna con diseño Corporate Cyberpunk 2077
- [x] Glassmorphic design system con colores profesionales
- [x] Búsqueda RAG integrada en tiempo real
- [x] Análisis con IA (Ollama) desde UI
- [x] Responsive design (mobile, tablet, desktop)
- [x] Estado de conexión y salud del sistema
- [x] JavaScript corporativo sin librería externa

### 🔄 En Desarrollo (Fase 4)
- [ ] Cloudflare Tunnel para acceso remoto seguro
- [ ] Historial de sesiones y guardado de búsquedas
- [ ] Modo estudio con notas personalizadas
- [ ] Multi-agente colaborativo para análisis complejos

---

## 📁 Estructura del Proyecto

```
aihack/
├── api/
│   └── server.py              # FastAPI server con RAG integrado
├── rag/
│   ├── chroma_db/             # Base de datos vectorial (auto-generada)
│   └── ingest/
│       ├── ingest.py          # Script de indexación
│       └── sources/           # Documentos fuente
│           ├── PayloadsAllTheThings/
│           ├── HackTricks/
│           ├── OSCP-Notes/
│           ├── CTF-Notes/
│           ├── GTFOBins/
│           └── Cheatsheets/
├── web/
│   ├── index.html             # Interfaz web principal
│   ├── style.css              # Estilos modernos y responsive
│   ├── script.js              # Lógica JavaScript para API calls
│   └── server.py              # Servidor web simple para archivos estáticos
├── aihack.sh                  # CLI principal
├── start_server.sh           # Script de inicio del servidor API
├── start_web.sh               # Script de inicio del servidor web
├── test_rag.py                # Script de validación
├── download_knowledge.sh      # Descarga de fuentes
├── requirements.txt           # Dependencias Python
├── .env                       # Configuración (IP Ollama, etc.)
└── README.md                  # Este archivo
```

---

## 🔧 Configuración Avanzada

### Variables de Entorno (.env)
```bash
# URL de Ollama (reemplaza con IP del servidor IA)
OLLAMA_URL=http://192.168.1.100:11434

# Modelo LLM a usar
OLLAMA_MODEL=llama3

# Configuración del servidor
HOST=0.0.0.0
PORT=8000
```

### Personalización del RAG

#### Agregar nuevas fuentes de conocimiento
```bash
# 1. Agregar documentos a rag/ingest/sources/
# 2. Re-ejecutar indexación
python3 rag/ingest/ingest.py
```

#### Cambiar modelo de embeddings
```python
# En api/server.py
embedding_model = SentenceTransformer("otro-modelo")
```

---

## 🐛 Solución de Problemas

### "Ollama no está disponible"
```bash
# Verificar que Ollama está corriendo
curl http://localhost:11434/api/tags

# Si no está, iniciarlo
ollama serve

# O cambiar la URL en .env
OLLAMA_URL=http://TU_IP_SERVIDOR:11434
```

### "ChromaDB está vacío"
```bash
# Re-indexar documentos
cd rag/ingest
python3 ingest.py
```

### "Error de permisos"
```bash
# Dar permisos a ChromaDB
chmod -R 777 rag/chroma_db/
```

### "Modelo de embeddings no descarga"
```bash
# Limpiar cache y reintentar
rm -rf ~/.cache/huggingface/
python3 rag/ingest/ingest.py
```

---

## 📚 Base de Conocimiento

El RAG está alimentado por estas fuentes especializadas:

| Fuente | Contenido | Tamaño |
|--------|-----------|--------|
| **PayloadsAllTheThings** | Payloads, bypasses, exploits por tipo de ataque | 333MB |
| **HackTricks** | Enciclopedia completa de pentesting | ~50MB |
| **OSCP Notes** | Notas prácticas de certificación OSCP | ~10MB |
| **CTF Notes** | Writeups y técnicas de CTF | ~5MB |
| **GTFOBins** | Binarios Unix para privilege escalation | ~2MB |
| **Cheatsheets** | Comandos rápidos por herramienta | ~1MB |

**Total:** 1,710 documentos → 52,000+ fragmentos → Indexados en ChromaDB

---

## 🤝 Contribución

### Agregar nuevas fuentes de conocimiento
1. Fork el proyecto
2. Agrega documentos a `rag/ingest/sources/`
3. Ejecuta `python3 rag/ingest/ingest.py`
4. Testea con `python3 test_rag.py`
5. Pull request

### Mejoras al código
- Issues para bugs/features
- Pull requests bien documentadas
- Tests incluidos

### Fuentes sugeridas para agregar
- Notas personales de pentesting
- Writeups de CTF
- Documentación de herramientas
- Papers de seguridad

---

## 📄 Licencia

Este proyecto es open source y está disponible bajo la [MIT License](LICENSE).

---

## 🙏 Agradecimientos

- **PayloadsAllTheThings** por la colección más completa de payloads
- **HackTricks** por la enciclopedia de pentesting
- **Comunidad OSCP** por compartir conocimientos
- **Ollama** por hacer la IA local accesible

---

## 📞 Contacto

- **Autor:** Rollorsson
- **LinkedIn:** https://www.linkedin.com/in/nicolas-gaspari-049624b9/
- **Proyecto:** AIHack Copilot v2

---

*Aprendiendo haciendo proyectos reales.*
