"""Shared fixtures for browser tests."""

import http.server
import socket
import socketserver
import subprocess
import threading
import time
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / 'output'
OUTPUT_FILE = OUTPUT_DIR / 'index.html'
LESSON_FILE = OUTPUT_DIR / 'lessons' / '01-first-flower.html'

# Default port for test server, with fallback
TEST_PORT = 8765


@pytest.fixture(scope="session")
def build_output():
    """Build the output files once per test session."""
    subprocess.run(['uv', 'run', 'build'], cwd=PROJECT_ROOT, check=True)
    assert OUTPUT_FILE.exists(), "Build did not create output file"
    assert LESSON_FILE.exists(), "Build did not create lesson file"
    return OUTPUT_DIR


@pytest.fixture(scope="session")
def http_server(build_output):
    """
    Start an HTTP server serving the output directory with CORS headers.

    This fixture is shared across all browser tests to avoid repeatedly
    starting/stopping the server. Uses session scope for efficiency.
    """
    # Find an available port
    port = TEST_PORT
    for attempt_port in range(TEST_PORT, TEST_PORT + 10):
        try:
            # Try to bind to the port
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.bind(("", attempt_port))
            test_socket.close()
            port = attempt_port
            break
        except OSError:
            continue

    # Create a custom handler that serves from OUTPUT_DIR with CORS headers
    # and simulates GitHub Pages path structure (/sketchpy/)
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(OUTPUT_DIR), **kwargs)

        def translate_path(self, path):
            # Strip /sketchpy prefix to serve from OUTPUT_DIR root
            # This simulates GitHub Pages where repo is served at /sketchpy/
            if path.startswith('/sketchpy/'):
                path = path[9:]  # Remove '/sketchpy'
            elif path.startswith('/sketchpy'):
                path = path[8:]  # Remove '/sketchpy'
            return super().translate_path(path)

        def end_headers(self):
            # Add headers required for Pyodide/SharedArrayBuffer
            self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
            self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
            super().end_headers()

        def log_message(self, format, *args):
            # Suppress server logs during tests
            pass

    # Create the server
    server = socketserver.TCPServer(("", port), Handler)

    # Run server in background thread
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    # Wait a moment for server to start
    time.sleep(0.5)

    # Provide the base URL to tests (with /sketchpy prefix to match GitHub Pages)
    base_url = f"http://localhost:{port}/sketchpy"

    yield base_url

    # Cleanup: shutdown server
    server.shutdown()
    server.server_close()
