"""Tests for Pyodide worker initialization and execution."""

import http.server
import socketserver
import subprocess
import threading
import time
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright


PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / 'output'
TEST_PORT = 8766  # Different port from main browser tests


@pytest.fixture(scope="module")
def build_output():
    """Build the output file before tests."""
    subprocess.run(['uv', 'run', 'build'], cwd=PROJECT_ROOT, check=True)
    assert (OUTPUT_DIR / 'index.html').exists(), "Build did not create output file"
    return OUTPUT_DIR


@pytest.fixture(scope="module")
def http_server(build_output):
    """Start an HTTP server serving the output directory with CORS headers for Pyodide."""
    port = TEST_PORT
    for attempt_port in range(TEST_PORT, TEST_PORT + 10):
        try:
            with socketserver.TCPServer(("", attempt_port), None) as test_socket:
                port = attempt_port
                break
        except OSError:
            continue

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(OUTPUT_DIR), **kwargs)

        def end_headers(self):
            self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
            self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
            super().end_headers()

        def log_message(self, format, *args):
            pass

    server = socketserver.TCPServer(("", port), Handler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.5)

    base_url = f"http://localhost:{port}"
    yield base_url

    server.shutdown()
    server.server_close()


def test_worker_initializes_without_errors(http_server):
    """Test that the Pyodide worker initializes without import errors.

    This test specifically checks for the 'ast' import issue and other
    initialization problems that would prevent the worker from becoming ready.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Collect ALL console messages (not just errors)
        console_messages = []
        def handle_console(msg):
            console_messages.append(f"[{msg.type}] {msg.text}")
        page.on('console', handle_console)

        # Collect page errors
        page_errors = []
        page.on('pageerror', lambda exc: page_errors.append(str(exc)))

        # Load a LESSON page (not the landing page) - lessons have the editor and status
        page.goto(f'{http_server}/lessons/01-first-flower.html')

        # Wait a bit for page to start loading
        time.sleep(2)

        # Wait for either success or failure (with timeout)
        try:
            # Wait for the loading indicator to disappear
            page.wait_for_selector('#loading', state='hidden', timeout=30000)

            # Check status
            status_text = page.locator('#status').text_content()

            # If we got here, initialization succeeded
            assert 'Ready' in status_text or 'Success' in status_text, \
                f"Expected 'Ready' or 'Success' status, got: {status_text}"

        except Exception as e:
            # Initialization failed - collect diagnostics
            try:
                error_div = page.locator('#error')
                error_div_text = error_div.text_content(timeout=1000) if error_div.count() > 0 else "No error div"
            except:
                error_div_text = "Error div not accessible"

            try:
                status = page.locator('#status')
                status_text = status.text_content(timeout=1000) if status.count() > 0 else "No status"
            except:
                status_text = "Status not accessible"

            # Build comprehensive error report
            error_report = [
                "=" * 80,
                "WORKER INITIALIZATION FAILED",
                "=" * 80,
                "",
                f"Status: {status_text}",
                f"Error div: {error_div_text}",
                "",
                "Console messages (look for Python print statements):",
                "-" * 80,
            ]
            error_report.extend(console_messages)
            error_report.append("")
            error_report.append("Page errors:")
            error_report.append("-" * 80)
            error_report.extend(page_errors if page_errors else ["(none)"])
            error_report.append("")
            error_report.append("Original exception:")
            error_report.append(str(e))
            error_report.append("")
            error_report.append("IMPORTANT: Check console messages above for Python errors from worker!")
            error_report.append("Look for messages like '✓ Initial security applied' or ImportError")
            error_report.append("=" * 80)

            browser.close()

            # Fail with comprehensive report
            pytest.fail("\n".join(error_report))

        # Check for any page errors even on success
        assert len(page_errors) == 0, f"Page errors during initialization: {page_errors}"

        browser.close()


def test_worker_validates_and_executes_code(http_server):
    """Test that the worker can validate and execute simple Python code."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Collect console messages
        console_messages = []
        page.on('console', lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))

        page_errors = []
        page.on('pageerror', lambda exc: page_errors.append(str(exc)))

        # Load the page
        page.goto(f'{http_server}/index.html')

        # Wait for worker to be ready
        try:
            page.wait_for_selector('#loading', state='hidden', timeout=30000)
        except Exception as e:
            error_report = ["Worker failed to initialize"] + console_messages
            pytest.fail("\n".join(error_report))

        # Clear any auto-run results
        page.click('button:has-text("Clear")')

        # Enter simple test code
        test_code = """can = Canvas(200, 200)
can.rect(10, 10, 50, 50, fill=Color.RED)"""

        # Use CodeMirror 6 API to set content
        page.evaluate(f"""
            window.editorView.dispatch({{
                changes: {{
                    from: 0,
                    to: window.editorView.state.doc.length,
                    insert: {repr(test_code)}
                }}
            }});
        """)

        # Run the code
        page.click('#runBtn')

        # Wait for execution to complete
        page.wait_for_selector('#canvas svg', timeout=5000)

        # Check for errors
        error_text = page.locator('#error').text_content()
        assert 'Error' not in error_text, f"Execution error: {error_text}\n\nConsole: {console_messages}"

        # Verify SVG was created
        svg_element = page.locator('#canvas svg')
        assert svg_element.count() > 0, "No SVG element found in canvas"

        assert len(page_errors) == 0, f"Page errors during execution: {page_errors}"

        browser.close()


def test_worker_blocks_forbidden_imports(http_server):
    """Test that the worker correctly blocks import statements."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        console_messages = []
        page.on('console', lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))

        page.goto(f'{http_server}/index.html')

        try:
            page.wait_for_selector('#loading', state='hidden', timeout=30000)
        except Exception as e:
            error_report = ["Worker failed to initialize"] + console_messages
            pytest.fail("\n".join(error_report))

        # Try to execute code with an import
        test_code = """import os
can = Canvas(200, 200)"""

        page.evaluate(f"""
            window.editorView.dispatch({{
                changes: {{
                    from: 0,
                    to: window.editorView.state.doc.length,
                    insert: {repr(test_code)}
                }}
            }});
        """)

        page.click('#runBtn')

        # Wait for error to appear
        page.wait_for_selector('#error', state='visible', timeout=5000)

        # Verify we got an import error
        error_text = page.locator('#error').text_content()
        assert 'Import' in error_text or 'import' in error_text, \
            f"Expected import error, got: {error_text}"

        browser.close()
