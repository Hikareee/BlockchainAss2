import http.server
import socketserver
import webbrowser

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Allow browser auto-refresh without CORS issues
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

# Start the server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    webbrowser.open(f"http://localhost:{PORT}")  # auto-open browser
    httpd.serve_forever()
import http.server
import socketserver
import webbrowser

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Allow browser auto-refresh without CORS issues
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

# Start the server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    webbrowser.open(f"http://localhost:{PORT}")  # auto-open browser
    httpd.serve_forever()
