#!/bin/bash
# AIHack Full System Startup Script
# Starts both API server (port 8000) and Web interface (port 3000)

echo "🤖 AIHack Full System Startup"
echo "================================"

# Check if we're in the right directory
if [ ! -f "start_server.sh" ] || [ ! -f "start_web.sh" ]; then
    echo "❌ Error: Startup scripts not found. Please run this script from the aihack root directory."
    exit 1
fi

echo "📁 Working directory: $(pwd)"
echo ""

# Function to check if a port is in use
check_port() {
    local port=$1
    local name=$2
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Warning: Port $port ($name) is already in use"
        return 1
    fi
    return 0
}

# Check ports before starting
echo "🔍 Checking port availability..."
check_port 8000 "API Server"
check_port 3000 "Web Server"
echo ""

# Start API server in background
echo "🚀 Starting API server (port 8000)..."
bash start_server.sh &
API_PID=$!

# Wait a moment for API server to start
sleep 3

# Check if API server started successfully
if ! kill -0 $API_PID 2>/dev/null; then
    echo "❌ Error: API server failed to start"
    exit 1
fi

echo "✅ API server started (PID: $API_PID)"
echo ""

# Start web server in background
echo "🌐 Starting web interface (port 3000)..."
bash start_web.sh &
WEB_PID=$!

# Wait a moment for web server to start
sleep 2

# Check if web server started successfully
if ! kill -0 $WEB_PID 2>/dev/null; then
    echo "❌ Error: Web server failed to start"
    kill $API_PID 2>/dev/null
    exit 1
fi

echo "✅ Web server started (PID: $WEB_PID)"
echo ""

echo "🎉 AIHack system fully operational!"
echo ""
echo "📊 URLs:"
echo "   🌐 Web Interface: http://localhost:3000"
echo "   🔗 API Server:    http://localhost:8000"
echo "   📖 API Docs:      http://localhost:8000/docs"
echo ""
echo "💡 Open http://localhost:3000 in your browser to access the web interface"
echo "🔄 The web interface will automatically connect to the API server"
echo ""
echo "🛑 To stop both servers: kill $API_PID $WEB_PID"
echo "   Or use: pkill -f 'python3.*server.py'"
echo ""

# Wait for user interrupt
trap "echo ''; echo '🛑 Stopping servers...'; kill $API_PID $WEB_PID 2>/dev/null; exit 0" INT

echo "Press Ctrl+C to stop both servers..."
wait