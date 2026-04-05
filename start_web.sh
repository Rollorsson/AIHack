#!/bin/bash
# AIHack Web Server Startup Script
# Starts the web interface server on port 3000

echo "🤖 AIHack Web Interface Server"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "web/server.py" ]; then
    echo "❌ Error: web/server.py not found. Please run this script from the aihack root directory."
    exit 1
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH."
    exit 1
fi

echo "📁 Working directory: $(pwd)"
echo "🌐 Starting web server on http://localhost:3000"
echo ""

# Change to web directory and start server
cd web
python3 server.py