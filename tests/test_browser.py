"""Browser tests for the web interface."""

import subprocess
import time
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright, expect


PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_FILE = PROJECT_ROOT / 'output' / 'index.html'
LESSON_FILE = PROJECT_ROOT / 'output' / 'lessons' / '01-first-flower.html'


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


def test_keyboard_shortcut_runs_code(build_output):
    """Test that Ctrl-Enter (or Cmd-Enter on Mac) runs the code."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the page
        page.goto(f'file://{build_output.absolute()}')

        # Wait for Pyodide to load
        page.wait_for_selector('#loading', state='hidden', timeout=30000)

        # Wait for initial auto-run to complete
        page.wait_for_selector('#canvas svg', timeout=10000)

        # Clear the canvas first
        page.click('button:has-text("Clear")')

        # Wait a moment for clear to take effect
        page.wait_for_timeout(100)

        # Verify canvas is cleared
        canvas_content = page.locator('#canvas').inner_text()
        assert 'cleared' in canvas_content.lower() or 'click' in canvas_content.lower(), "Canvas should be cleared"

        # Focus the editor by clicking on it
        page.locator('.cm-editor').click()

        # Press Ctrl-Enter (Playwright automatically uses Cmd on Mac)
        page.keyboard.press('Control+Enter')

        # Wait for SVG to appear (code should run)
        page.wait_for_selector('#canvas svg', timeout=5000)

        # Verify SVG content is present
        svg_content = page.locator('#canvas svg').inner_html()
        assert '<circle' in svg_content or '<rect' in svg_content, "Canvas should contain shapes after keyboard shortcut"

        # Verify success status
        status_text = page.locator('#status').text_content()
        assert 'Success' in status_text, f"Expected success status after keyboard shortcut, got: {status_text}"

        browser.close()


def test_lesson_page_editor_loads(build_output):
    """Test that the lesson page editor loads and is visible."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Track console messages
        errors = []
        console_messages = []

        def handle_console(msg):
            console_messages.append(f"{msg.type}: {msg.text}")
            if msg.type == 'error':
                errors.append(msg.text)

        page.on('console', handle_console)

        # Track page errors
        page_errors = []
        page.on('pageerror', lambda exc: page_errors.append(str(exc)))

        # Verify lesson file exists
        assert LESSON_FILE.exists(), f"Lesson file not found at {LESSON_FILE}"

        # Load the lesson page
        page.goto(f'file://{LESSON_FILE.absolute()}')

        # Take screenshot before waiting for anything
        screenshot_dir = PROJECT_ROOT / 'test-screenshots'
        screenshot_dir.mkdir(exist_ok=True)
        page.screenshot(path=str(screenshot_dir / 'lesson-page-initial.png'))

        # Wait for the page to be ready - check for CodeMirror editor
        try:
            page.wait_for_selector('.cm-editor', timeout=5000, state='visible')
        except Exception as e:
            # Take screenshot on failure
            page.screenshot(path=str(screenshot_dir / 'lesson-page-editor-failure.png'))
            # Print console messages to help debug
            print("\n=== Console messages ===")
            for msg in console_messages:
                print(msg)
            print(f"\n=== Page errors ===")
            for err in page_errors:
                print(err)
            print(f"\n=== Screenshot saved to {screenshot_dir / 'lesson-page-editor-failure.png'} ===")
            raise AssertionError(f"CodeMirror editor not visible: {e}")

        # Take screenshot after editor loads
        page.screenshot(path=str(screenshot_dir / 'lesson-page-editor-loaded.png'))

        # Verify the editor is visible
        editor = page.locator('.cm-editor')
        expect(editor).to_be_visible()

        # Verify the editor has content (starter code)
        editor_content = page.locator('.cm-editor').inner_text()
        assert len(editor_content) > 0, "Editor should have starter code"
        assert 'Canvas' in editor_content, "Editor should contain Canvas code"

        # Check for critical errors
        assert len(page_errors) == 0, f"Page errors on lesson page: {page_errors}"
        critical_errors = [e for e in errors if 'Cross-Origin' not in e]
        assert len(critical_errors) == 0, f"Console errors on lesson page: {critical_errors}"

        browser.close()


def test_lesson_page_run_button_visible(build_output):
    """Test that the Run button is visible on the lesson page."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Verify lesson file exists
        assert LESSON_FILE.exists(), f"Lesson file not found at {LESSON_FILE}"

        # Load the lesson page
        page.goto(f'file://{LESSON_FILE.absolute()}')

        # Take screenshot
        screenshot_dir = PROJECT_ROOT / 'test-screenshots'
        screenshot_dir.mkdir(exist_ok=True)
        page.screenshot(path=str(screenshot_dir / 'lesson-page-run-button.png'))

        # Check if run button exists and is visible
        run_button = page.locator('#runBtn')

        try:
            expect(run_button).to_be_visible(timeout=2000)
        except Exception as e:
            # Get computed styles to debug visibility
            is_displayed = page.evaluate('''() => {
                const btn = document.getElementById('runBtn');
                if (!btn) return 'button not found';
                const style = window.getComputedStyle(btn);
                const parentStyle = window.getComputedStyle(btn.parentElement);
                return {
                    button_display: style.display,
                    button_visibility: style.visibility,
                    button_opacity: style.opacity,
                    parent_display: parentStyle.display,
                    parent_visibility: parentStyle.visibility,
                    button_exists: !!btn,
                    button_offsetParent: !!btn.offsetParent
                };
            }''')
            page.screenshot(path=str(screenshot_dir / 'lesson-page-run-button-hidden.png'))
            raise AssertionError(f"Run button not visible. Styles: {is_displayed}. Screenshot saved.")

        # Verify button text
        button_text = run_button.text_content()
        assert '▶' in button_text or 'Run' in button_text, f"Expected 'Run' button text, got: {button_text}"

        browser.close()
