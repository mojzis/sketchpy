"""Browser tests for CodeMirror autocomplete functionality."""

import subprocess
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


def test_codemirror_initialized(build_output):
    """Test that CodeMirror editor is initialized."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the page
        page.goto(f'file://{build_output.absolute()}')

        # Wait for editor to be initialized
        page.wait_for_selector('.CodeMirror', timeout=5000)

        # Verify CodeMirror is visible
        editor = page.locator('.CodeMirror')
        expect(editor).to_be_visible()

        browser.close()


def test_api_definitions_extracted(build_output):
    """Test that API definitions are extracted from Python code."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the page
        page.goto(f'file://{build_output.absolute()}')

        # Wait for page to load
        page.wait_for_selector('.CodeMirror', timeout=5000)

        # Check that API_DEFINITIONS exists and has Canvas methods
        result = page.evaluate('''
            () => {
                if (!window.API_DEFINITIONS) {
                    return { success: false, error: 'API_DEFINITIONS not found' };
                }

                const canMethods = API_DEFINITIONS['can'];
                if (!canMethods || !Array.isArray(canMethods)) {
                    return { success: false, error: 'can methods not found' };
                }

                return {
                    success: true,
                    canMethodCount: canMethods.length,
                    sampleMethods: canMethods.slice(0, 3)
                };
            }
        ''')

        assert result['success'], f"API extraction failed: {result.get('error')}"
        assert result['canMethodCount'] > 5, f"Expected at least 5 Canvas methods, got {result['canMethodCount']}"

        # Verify some methods exist
        sample_methods = ' '.join(result['sampleMethods'])
        assert 'rect' in sample_methods or 'circle' in sample_methods, "Expected rect or circle method"

        browser.close()


def test_canvas_methods_have_defaults(build_output):
    """Test that Canvas methods show default parameter values."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the page
        page.goto(f'file://{build_output.absolute()}')

        # Wait for page to load
        page.wait_for_selector('.CodeMirror', timeout=5000)

        # Check that methods have default values
        result = page.evaluate('''
            () => {
                const canMethods = window.API_DEFINITIONS['can'];

                // Find rect method
                const rectMethod = canMethods.find(m => m.startsWith('rect('));

                // Find circle method
                const circleMethod = canMethods.find(m => m.startsWith('circle('));

                return {
                    rectMethod: rectMethod,
                    circleMethod: circleMethod,
                    hasDefaults: rectMethod && rectMethod.includes('=')
                };
            }
        ''')

        assert result['hasDefaults'], "Methods should have default values"
        assert result['rectMethod'], "rect method should exist"
        assert result['circleMethod'], "circle method should exist"

        # Verify defaults are present
        assert '=' in result['rectMethod'], f"rect should have defaults: {result['rectMethod']}"
        assert '=' in result['circleMethod'], f"circle should have defaults: {result['circleMethod']}"

        browser.close()


def test_autocomplete_triggers_on_dot(build_output):
    """Test that autocomplete popup appears when typing 'can.'"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the page
        page.goto(f'file://{build_output.absolute()}')

        # Wait for CodeMirror to load
        page.wait_for_selector('.CodeMirror', timeout=5000)

        # Focus the editor
        page.click('.CodeMirror')

        # Type "can." to trigger autocomplete
        page.keyboard.type('can.')

        # Wait for autocomplete hint popup to appear
        page.wait_for_selector('.CodeMirror-hints', timeout=2000)

        # Verify hint popup is visible
        hints = page.locator('.CodeMirror-hints')
        expect(hints).to_be_visible()

        # Check that hints contain Canvas methods
        hint_text = page.locator('.CodeMirror-hints').inner_text()
        assert 'rect' in hint_text or 'circle' in hint_text, f"Hints should contain Canvas methods, got: {hint_text}"

        browser.close()


def test_autocomplete_filters_on_typing(build_output):
    """Test that autocomplete filters results when typing."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the page
        page.goto(f'file://{build_output.absolute()}')

        # Wait for CodeMirror to load
        page.wait_for_selector('.CodeMirror', timeout=5000)

        # Focus the editor
        page.click('.CodeMirror')

        # Type "can.cir" to trigger filtered autocomplete
        page.keyboard.type('can.cir')

        # Wait for autocomplete hint popup
        page.wait_for_selector('.CodeMirror-hints', timeout=2000)

        # Verify only circle method is shown (filtered)
        hint_text = page.locator('.CodeMirror-hints').inner_text()
        assert 'circle' in hint_text, f"Should show circle method, got: {hint_text}"

        # Rect should not be in filtered results
        assert 'rect' not in hint_text.lower(), f"Should not show rect when filtering for 'cir', got: {hint_text}"

        browser.close()


def test_palette_colors_available(build_output):
    """Test that palette color constants are available in autocomplete."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the page
        page.goto(f'file://{build_output.absolute()}')

        # Wait for page to load
        page.wait_for_selector('.CodeMirror', timeout=5000)

        # Check that palette colors are extracted
        result = page.evaluate('''
            () => {
                const gardenColors = window.API_DEFINITIONS['CreativeGardenPalette'];
                const oasisColors = window.API_DEFINITIONS['CalmOasisPalette'];
                const basicColors = window.API_DEFINITIONS['Color'];

                return {
                    hasGarden: gardenColors && gardenColors.length > 0,
                    hasOasis: oasisColors && oasisColors.length > 0,
                    hasBasic: basicColors && basicColors.length > 0,
                    sampleGarden: gardenColors ? gardenColors.slice(0, 3) : [],
                    sampleBasic: basicColors ? basicColors.slice(0, 3) : []
                };
            }
        ''')

        assert result['hasGarden'], "CreativeGardenPalette colors should be available"
        assert result['hasOasis'], "CalmOasisPalette colors should be available"
        assert result['hasBasic'], "Color class colors should be available"

        # Verify some specific colors
        garden_colors = ' '.join(result['sampleGarden'])
        basic_colors = ' '.join(result['sampleBasic'])

        assert any(color in garden_colors for color in ['ROSE_QUARTZ', 'BUTTER_YELLOW', 'PEACH_WHISPER']), \
            f"Should have CreativeGardenPalette colors, got: {garden_colors}"
        assert any(color in basic_colors for color in ['RED', 'BLUE', 'GREEN']), \
            f"Should have basic colors, got: {basic_colors}"

        browser.close()


def test_autocomplete_shows_palette_colors(build_output):
    """Test that autocomplete shows palette colors when typing 'CreativeGardenPalette.'"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the page
        page.goto(f'file://{build_output.absolute()}')

        # Wait for CodeMirror to load
        page.wait_for_selector('.CodeMirror', timeout=5000)

        # Focus the editor
        page.click('.CodeMirror')

        # Clear existing content first
        page.keyboard.press('Control+A')
        page.keyboard.press('Backspace')

        # Type to trigger palette color autocomplete
        page.keyboard.type('fill = CreativeGardenPalette.')

        # Wait for autocomplete hint popup
        page.wait_for_selector('.CodeMirror-hints', timeout=2000)

        # Verify palette colors are shown
        hint_text = page.locator('.CodeMirror-hints').inner_text()

        # Check for some expected palette colors
        has_palette_colors = any(color in hint_text for color in [
            'ROSE_QUARTZ', 'BUTTER_YELLOW', 'MINT_CREAM',
            'PEACH_WHISPER', 'CORAL_BLUSH'
        ])

        assert has_palette_colors, f"Should show CreativeGardenPalette colors, got: {hint_text}"

        browser.close()


def test_method_signatures_are_single_line(build_output):
    """Test that method signatures are formatted as single lines."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the page
        page.goto(f'file://{build_output.absolute()}')

        # Wait for page to load
        page.wait_for_selector('.CodeMirror', timeout=5000)

        # Check that method signatures don't have newlines
        result = page.evaluate('''
            () => {
                const canMethods = window.API_DEFINITIONS['can'];

                // Check if any method has newlines
                const hasNewlines = canMethods.some(m => m.includes('\\n'));

                // Get sample methods
                const rectMethod = canMethods.find(m => m.startsWith('rect('));
                const circleMethod = canMethods.find(m => m.startsWith('circle('));

                return {
                    hasNewlines: hasNewlines,
                    rectMethod: rectMethod,
                    circleMethod: circleMethod
                };
            }
        ''')

        assert not result['hasNewlines'], "Method signatures should not contain newlines"

        # Verify methods are readable single lines
        rect = result['rectMethod']
        circle = result['circleMethod']

        assert rect and '=' in rect, f"rect should be a single line with defaults: {rect}"
        assert circle and '=' in circle, f"circle should be a single line with defaults: {circle}"

        # Verify they're reasonably formatted (not too long)
        assert len(rect) < 200, f"rect signature too long ({len(rect)} chars): {rect}"
        assert len(circle) < 200, f"circle signature too long ({len(circle)} chars): {circle}"

        browser.close()
