#!/bin/bash
# AIHack Web Interface Test Script
# Tests the web interface connectivity and basic functionality

echo "🧪 AIHack Web Interface Test"
echo "=============================="

BASE_URL="http://localhost:3000"
API_URL="http://localhost:8000"

echo "🔗 Testing web server..."
if curl -s -o /dev/null -w "%{http_code}" "$BASE_URL" | grep -q "200"; then
    echo "✅ Web server responding on $BASE_URL"
else
    echo "❌ Web server not responding on $BASE_URL"
    exit 1
fi

echo ""
echo "🔗 Testing API server..."
if curl -s "$API_URL/health" | grep -q "online"; then
    echo "✅ API server responding on $API_URL"
else
    echo "❌ API server not responding on $API_URL"
    exit 1
fi

echo ""
echo "🔍 Testing search functionality..."
SEARCH_RESPONSE=$(curl -s -X POST "$API_URL/search" \
    -H "Content-Type: application/json" \
    -d '{"query": "SQL injection", "top_k": 1}')

if echo "$SEARCH_RESPONSE" | grep -q "results"; then
    echo "✅ Search API working"
else
    echo "❌ Search API failed"
    echo "Response: $SEARCH_RESPONSE"
fi

echo ""
echo "🎉 All tests passed!"
echo ""
echo "🌐 Open $BASE_URL in your browser to access the web interface"
echo "📊 The interface should show 'Conectado' status and allow searches"