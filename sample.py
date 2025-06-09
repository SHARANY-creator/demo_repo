from http.server import SimpleHTTPRequestHandler, HTTPServer

PORT = 8000
handler = SimpleHTTPRequestHandler
httpd = HTTPServer(("localhost", PORT), handler)
print(f"Serving at http://localhost:{PORT}")
httpd.serve_forever()
