#!/usr/bin/env python3
"""
Simple web server to serve the visual dashboard.

This avoids CORS issues when accessing the API from the HTML file.
"""
import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

def serve_dashboard(port=8080):
    """Serve the visual dashboard on specified port."""
    
    # Change to examples directory
    examples_dir = Path(__file__).parent / "examples"
    if not examples_dir.exists():
        print("❌ Examples directory not found!")
        return
    
    os.chdir(examples_dir)
    
    # Check if dashboard file exists
    dashboard_file = "visual_dashboard.html"
    if not os.path.exists(dashboard_file):
        print(f"❌ {dashboard_file} not found in examples directory!")
        return
    
    # Create simple HTTP server
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            dashboard_url = f"http://localhost:{port}/{dashboard_file}"
            
            print(f"🌐 Serving Visual Dashboard at: {dashboard_url}")
            print(f"📁 Serving from: {examples_dir}")
            print(f"🛑 Press Ctrl+C to stop the server")
            print()
            print("📋 Make sure your API server is also running:")
            print("   uvicorn src.api:app --reload --port 8001")
            print()
            
            # Try to open browser automatically
            try:
                webbrowser.open(dashboard_url)
                print(f"🚀 Opened {dashboard_url} in your default browser")
            except:
                print(f"💡 Manually open: {dashboard_url}")
            
            print("\n" + "="*60)
            httpd.serve_forever()
            
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use. Try a different port:")
            print(f"   python serve_dashboard.py --port 8081")
        else:
            print(f"❌ Error starting server: {e}")
    except KeyboardInterrupt:
        print(f"\n🛑 Dashboard server stopped")

def main():
    """Main function with command line argument parsing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Serve NIST-AI-SCM Visual Dashboard")
    parser.add_argument("--port", type=int, default=8080, 
                       help="Port to serve dashboard on (default: 8080)")
    
    args = parser.parse_args()
    
    print("🎯 NIST-AI-SCM Toolkit Visual Dashboard Server")
    print("=" * 50)
    
    serve_dashboard(args.port)

if __name__ == "__main__":
    main()