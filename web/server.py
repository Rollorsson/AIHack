#!/usr/bin/env python3
"""
AIHack Web Server - Simple HTTP server for the web interface
"""
import http.server
import socketserver
import os
from pathlib import Path

class AIHackHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(__file__), **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

def main():
    web_dir = Path(__file__).parent
    port = 3000

    print("🤖 AIHack Web Interface")
    print(f"📁 Serving from: {web_dir}")
    print(f"🌐 URL: http://localhost:{port}")
    print("💡 Open this URL in your browser to access the interface")
    print("🔗 The API server should be running on http://localhost:8000")
    print("")

    try:
        with socketserver.TCPServer(("", port), AIHackHTTPRequestHandler) as httpd:
            print("🚀 Web server started successfully!")
            print("Press Ctrl+C to stop...")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Web server stopped.")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {port} is already in use. Please close other applications using this port.")
        else:
            print(f"❌ Error starting web server: {e}")

if __name__ == "__main__":
    main()