#!/bin/bash
set -e
if [ "$#" -lt 1 ]; then
  echo "Uso: $0 \"consulta RAG\""
  exit 1
fi
QUERY="$1"
SERVER="http://localhost:8000/analyze"

RESPONSE=$(curl -s -X POST "$SERVER" \
  -H "Content-Type: application/json" \
  -d "{\"query\": $(python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' <<< "$QUERY")}\")")

python3 - <<'PY'
import json,sys
try:
    data = json.loads(sys.stdin.read())
except json.JSONDecodeError:
    print('Error: respuesta no es JSON')
    sys.exit(1)

print('\n🤖 AIHack Analysis:')
print('===================')
print(data.get('response', ''))
print() 
print('📚 Contexto RAG usado:')
print(data.get('context_used', ''))
PY <<< "$RESPONSE"
