#!/usr/bin/env python3
import http.server
import ssl
import os
from pathlib import Path

# Generate self-signed certificate if it doesn't exist
cert_file = 'localhost.pem'
if not os.path.exists(cert_file):
    print("Generating self-signed certificate...")
    os.system(f'openssl req -new -x509 -keyout {cert_file} -out {cert_file} -days 365 -nodes -subj "/CN=localhost"')

PORT = 8000
httpd = http.server.HTTPServer(('localhost', PORT), http.server.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile=cert_file, server_side=True)

print(f"Serving HTTPS on https://localhost:{PORT}")
print("You'll need to click 'Advanced' -> 'Proceed to localhost' in Chrome")
httpd.serve_forever()
