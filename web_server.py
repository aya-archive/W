#!/usr/bin/env python3
"""
A.U.R.A Web Server
Serves the modern web interface for the A.U.R.A platform
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

class AURAHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler for A.U.R.A"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def end_headers(self):
        # Add CORS headers for development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Serve the main web interface
        if self.path == '/' or self.path == '/index.html':
            self.path = '/web_interface.html'
        return super().do_GET()

def start_web_server(port=8080):
    """Start the A.U.R.A web server"""
    try:
        # Change to the AURA directory
        aura_dir = Path(__file__).parent
        os.chdir(aura_dir)
        
        # Create the server
        with socketserver.TCPServer(("", port), AURAHTTPRequestHandler) as httpd:
            print("🤖 A.U.R.A Web Server Starting...")
            print("=" * 50)
            print(f"🌐 Server running at: http://localhost:{port}")
            print(f"📁 Serving from: {aura_dir}")
            print("=" * 50)
            print("🚀 Opening browser...")
            
            # Open browser automatically
            webbrowser.open(f'http://localhost:{port}')
            
            print("\n✨ A.U.R.A Web Interface is now live!")
            print("📊 Features available:")
            print("   • Interactive Dashboard")
            print("   • AI Chatbot Assistant")
            print("   • Risk Analysis")
            print("   • Forecasting")
            print("   • Client Data Management")
            print("\n🛑 Press Ctrl+C to stop the server")
            print("=" * 50)
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {port} is already in use. Trying port {port + 1}...")
            start_web_server(port + 1)
        else:
            print(f"❌ Error starting server: {e}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

def main():
    """Main function"""
    print("🤖 A.U.R.A - Adaptive User Retention Assistant")
    print("🌐 Modern Web Interface Server")
    print("=" * 50)
    
    # Check if web_interface.html exists
    if not Path("web_interface.html").exists():
        print("❌ Error: web_interface.html not found!")
        print("Please ensure the web interface file exists in the current directory.")
        sys.exit(1)
    
    # Get port from command line or use default
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ Invalid port number. Using default port 8080.")
    
    # Start the server
    start_web_server(port)

if __name__ == "__main__":
    main()
