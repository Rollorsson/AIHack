#!/bin/bash
set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

if [ "$#" -lt 1 ]; then
  echo -e "${BLUE}🤖 AIHack Copilot v2${NC}"
  echo "Uso: $0 \"[consulta de seguridad]\""
  echo ""
  echo "Ejemplos:"
  echo "  $0 \"sql injection en login\""
  echo "  $0 \"nmap output analysis\""
  echo "  $0 \"reverse shell payload \""
  exit 0
fi

QUERY="$1"
SERVER="${SERVER:-http://localhost:8000}"
ANALYZE_URL="$SERVER/analyze"
HEALTH_URL="$SERVER/health"

# Verificar que el servidor está disponible
if ! curl -s "$HEALTH_URL" > /dev/null 2>&1; then
  echo -e "${RED}❌ Error: Servidor no disponible en $SERVER${NC}"
  echo "   Inicia el servidor con: ./start_server.sh"
  exit 1
fi

# Hacer la consulta
echo -e "${BLUE}🔍 Analizando: \"$QUERY\"${NC}"
RESPONSE=$(curl -s -X POST "$ANALYZE_URL" \
  -H "Content-Type: application/json" \
  -d "{\"query\": $(python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' <<< "$QUERY")}" 2>/dev/null)

# Procesar y mostrar respuesta
python3 - "$RESPONSE" <<'PY'
import json, sys, os

try:
    data = json.loads(sys.argv[1])
except json.JSONDecodeError as e:
    print(f'Error JSON: {e}')
    sys.exit(1)

# Colores para Python
RED = '\033[0;31m'
GREEN = '\033[0;32m'
BLUE = '\033[0;34m'
YELLOW = '\033[1;33m'
CYAN = '\033[0;36m'
NC = '\033[0m'

# Mostrar respuesta
if 'response' in data:
    print(f'\n{CYAN}🤖 Respuesta del análisis:{NC}\n')
    print(data['response'])

# Mostrar contexto usado
if 'context_used' in data:
    print(f'\n{YELLOW}📚 Contexto utilizado:{NC}')
    preview = data['context_used'][:200]
    if preview:
        print(f'   {preview}...')
    
    if 'documents_found' in data:
        print(f'{CYAN}   📊 Documentos encontrados: {data["documents_found"]}{NC}')

print()
PY


# Fin del script
exit 0
