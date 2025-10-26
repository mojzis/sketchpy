"""Browser tests for the web interface."""

import subprocess
import time
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright, expect


PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_FILE = PROJECT_ROOT / 'output' / 'index.html'


@pytest.fixture(scope="module")
def build_output():
    """Build the output file before tests."""
    subprocess.run(['uv', 'run', 'build'], cwd=PROJECT_ROOT, check=True)
    assert OUTPUT_FILE.exists(), "Build did not create output file"
    return OUTPUT_FILE


def test_page_loads_without_errors(build_output):
    """Test that the page loads in a browser without errors."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Track console messages
        errors = []
        warnings = []

        def handle_console(msg):
            if msg.type == 'error':
                errors.append(msg.text)
            elif msg.type == 'warning':
                warnings.append(msg.text)

        page.on('console', handle_console)

        # Track page errors (uncaught exceptions)
        page_errors = []
        page.on('pageerror', lambda exc: page_errors.append(str(exc)))

        # Load the page
        page.goto(f'file://{build_output.absolute()}')

        # Wait for the page to be ready (CodeMirror 6 editor)
        page.wait_for_selector('.cm-editor', timeout=5000)

        # Check for critical errors
        assert len(page_errors) == 0, f"Page errors: {page_errors}"

        # Filter out expected warnings (like CORS warnings from file:// protocol)
        critical_errors = [e for e in errors if 'Cross-Origin' not in e]
        assert len(critical_errors) == 0, f"Console errors: {critical_errors}"

        browser.close()


def test_pyodide_loads_successfully(build_output):
    """Test that Pyodide loads and initializes."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Track errors
        errors = []
        page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
        page_errors = []
        page.on('pageerror', lambda exc: page_errors.append(str(exc)))

        # Load the page
        page.goto(f'file://{build_output.absolute()}')

        # Wait for loading indicator to disappear (Pyodide loaded)
        page.wait_for_selector('#loading', state='hidden', timeout=30000)

        # Check that status shows either "Ready" or "Success" (auto-run may have executed)
        status_text = page.locator('#status').text_content()
        assert 'Ready' in status_text or 'Success' in status_text, f"Expected 'Ready' or 'Success' status, got: {status_text}"

        # Check for errors
        assert len(page_errors) == 0, f"Page errors during Pyodide load: {page_errors}"

        browser.close()


def test_python_code_executes_without_errors(build_output):
    """Test that the embedded Python code runs without errors."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Track console errors
        python_errors = []

        def handle_console(msg):
            if msg.type == 'error' and 'PythonError' in msg.text:
                python_errors.append(msg.text)

        page.on('console', handle_console)

        # Track page errors
        page_errors = []
        page.on('pageerror', lambda exc: page_errors.append(str(exc)))

        # Load the page
        page.goto(f'file://{build_output.absolute()}')

        # Wait for Pyodide to load
        page.wait_for_selector('#loading', state='hidden', timeout=30000)

        # Click the "Run Code" button
        page.click('#runBtn')

        # Wait for the canvas to render
        page.wait_for_selector('#canvas svg', timeout=10000)

        # Check for Python errors
        assert len(python_errors) == 0, f"Python execution errors: {python_errors}"
        assert len(page_errors) == 0, f"Page errors during execution: {page_errors}"

        browser.close()


def test_canvas_renders_svg(build_output):
    """Test that the Canvas actually renders SVG output."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the page
        page.goto(f'file://{build_output.absolute()}')

        # Wait for Pyodide to load
        page.wait_for_selector('#loading', state='hidden', timeout=30000)

        # Run the code
        page.click('#runBtn')

        # Wait for SVG to appear
        page.wait_for_selector('#canvas svg', timeout=10000)

        # Verify SVG content
        svg = page.locator('#canvas svg')
        expect(svg).to_be_visible()

        # Check that the SVG has some content (shapes)
        svg_content = page.locator('#canvas svg').inner_html()
        assert '<rect' in svg_content, "SVG should contain rectangles"
        assert '<circle' in svg_content, "SVG should contain circles"

        # Verify success status
        status_text = page.locator('#status').text_content()
        assert 'Success' in status_text, f"Expected success status, got: {status_text}"

        browser.close()


def test_color_class_available(build_output):
    """Test that the Color class is available in the Python environment."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the page
        page.goto(f'file://{build_output.absolute()}')

        # Wait for Pyodide to load
        page.wait_for_selector('#loading', state='hidden', timeout=30000)

        # Execute Python code to check Color class
        result = page.evaluate('''
            async () => {
                try {
                    await pyodide.runPythonAsync(`
                        # Check Color class exists and has attributes
                        assert hasattr(Color, 'RED')
                        assert hasattr(Color, 'BLUE')
                        assert Color.RED == "#FF0000"
                        result = "OK"
                    `);
                    return { success: true, result: pyodide.globals.get('result') };
                } catch (e) {
                    return { success: false, error: e.toString() };
                }
            }
        ''')

        assert result['success'], f"Color class check failed: {result.get('error', 'Unknown error')}"
        assert result['result'] == 'OK'

        browser.close()


def test_canvas_class_available(build_output):
    """Test that the Canvas class is available and functional."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the page
        page.goto(f'file://{build_output.absolute()}')

        # Wait for Pyodide to load
        page.wait_for_selector('#loading', state='hidden', timeout=30000)

        # Execute Python code to test Canvas
        result = page.evaluate('''
            async () => {
                try {
                    await pyodide.runPythonAsync(`
                        # Create a canvas and draw
                        c = Canvas(100, 100)
                        c.rect(10, 10, 20, 20, fill=Color.RED)
                        svg = c.to_svg()
                        assert '<svg' in svg
                        assert '<rect' in svg
                        assert 'width="100"' in svg
                        result = "OK"
                    `);
                    return { success: true, result: pyodide.globals.get('result') };
                } catch (e) {
                    return { success: false, error: e.toString() };
                }
            }
        ''')

        assert result['success'], f"Canvas class check failed: {result.get('error', 'Unknown error')}"
        assert result['result'] == 'OK'

        browser.close()


def test_grid_method_works(build_output):
    """Test that the grid method works and draws grid lines."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the page
        page.goto(f'file://{build_output.absolute()}')

        # Wait for Pyodide to load
        page.wait_for_selector('#loading', state='hidden', timeout=30000)

        # Execute Python code to test grid
        result = page.evaluate('''
            async () => {
                try {
                    await pyodide.runPythonAsync(`
                        # Create a canvas with grid
                        c = Canvas(200, 200)
                        c.grid(spacing=50, show_coords=True)
                        svg = c.to_svg()

                        # Verify grid lines are present
                        assert '<line' in svg, "Grid should contain lines"
                        assert 'stroke="#E8E8E8"' in svg, "Grid should have light grey color"

                        # Verify coordinate labels
                        assert '<text' in svg, "Grid should have coordinate labels"
                        assert '(0,0)' in svg, "Grid should show origin"

                        result = "OK"
                    `);
                    return { success: true, result: pyodide.globals.get('result') };
                } catch (e) {
                    return { success: false, error: e.toString() };
                }
            }
        ''')

        assert result['success'], f"Grid method check failed: {result.get('error', 'Unknown error')}"
        assert result['result'] == 'OK'

        browser.close()


def test_show_palette_method_works(build_output):
    """Test that the show_palette method works and displays palette colors."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the page
        page.goto(f'file://{build_output.absolute()}')

        # Wait for Pyodide to load
        page.wait_for_selector('#loading', state='hidden', timeout=30000)

        # Execute Python code to test show_palette
        result = page.evaluate('''
            async () => {
                try {
                    await pyodide.runPythonAsync(`
                        # Create a canvas and show palette
                        c = Canvas(600, 400)
                        c.show_palette(CreativeGardenPalette)
                        svg = c.to_svg()

                        # Verify palette rectangles are present
                        assert '<rect' in svg, "Palette should contain rectangles"
                        assert '<text' in svg, "Palette should have color labels"

                        # Verify some specific colors from CreativeGardenPalette
                        assert 'PEACH_WHISPER' in svg, "Palette should show color names"
                        assert '#FFDAC1' in svg, "Palette should show hex values"

                        result = "OK"
                    `);
                    return { success: true, result: pyodide.globals.get('result') };
                } catch (e) {
                    return { success: false, error: e.toString() };
                }
            }
        ''')

        assert result['success'], f"show_palette method check failed: {result.get('error', 'Unknown error')}"
        assert result['result'] == 'OK'

        browser.close()
