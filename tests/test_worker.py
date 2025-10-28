"""Tests for Pyodide worker initialization and execution."""

import time

import pytest
from playwright.sync_api import sync_playwright


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
        page.goto(f'{http_server}/lessons/theme-1/01-first-flower.html')

        # Wait a bit for page to start loading
        time.sleep(2)

        # Wait for either success or failure (with timeout)
        try:
            # Wait for the loading indicator to disappear
            page.wait_for_selector('#loading', state='hidden', timeout=30000)

            # Check status
            status_text = page.locator('#status').text_content()

            # If we got here, initialization succeeded
            assert status_text and ('Ready' in status_text or 'Success' in status_text), \
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

        # Load a lesson page (not index.html which is a landing page)
        page.goto(f'{http_server}/lessons/theme-1/01-first-flower.html')

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

        # Wait for execution to complete (status should be Success)
        page.wait_for_selector('#status:has-text("Success")', timeout=5000)

        # Verify no error banner appeared
        error_banner = page.locator('#error')
        # Error banner should either not exist or be hidden
        if error_banner.count() > 0:
            is_visible = error_banner.is_visible()
            assert not is_visible, f"Error banner visible when it shouldn't be\n\nConsole: {console_messages}"

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

        # Load a lesson page (not index.html which is a landing page)
        page.goto(f'{http_server}/lessons/theme-1/01-first-flower.html')

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

        # Wait for error banner to appear (indicates code validation/execution failed)
        page.wait_for_selector('#error', state='visible', timeout=5000)

        # Verify error banner appeared (banner just says "Error occurred", details are in Output tab)
        error_banner = page.locator('#error')
        assert error_banner.is_visible(), "Error banner should be visible for forbidden import"

        # The actual error message is in the Output tab, not the banner
        # Just verify that an error occurred, which is what we want

        browser.close()
