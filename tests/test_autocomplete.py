"""Browser tests for CodeMirror autocomplete functionality."""

import pytest
from playwright.sync_api import sync_playwright, expect


def test_codemirror_initialized(http_server):
    """Test that CodeMirror 6 editor is initialized."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the lesson page (not index.html which is a landing page)
        page.goto(f'{http_server}/lessons/theme-1/01-first-flower.html')

        # Wait for editor to be initialized (CodeMirror 6 uses .cm-editor)
        page.wait_for_selector('.cm-editor', timeout=10000)

        # Verify CodeMirror is visible
        editor = page.locator('.cm-editor')
        expect(editor).to_be_visible()

        browser.close()


def test_api_definitions_extracted(http_server):
    """Test that API definitions are extracted from Python code."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the lesson page
        page.goto(f'{http_server}/lessons/theme-1/01-first-flower.html')

        # Wait for page to load (CodeMirror 6)
        page.wait_for_selector('.cm-editor', timeout=10000)

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

                // Extract labels from objects (CodeMirror 6 format)
                const labels = canMethods.map(m => m.label || m);

                return {
                    success: true,
                    canMethodCount: canMethods.length,
                    sampleMethods: labels.slice(0, 3)
                };
            }
        ''')

        assert result['success'], f"API extraction failed: {result.get('error')}"
        assert result['canMethodCount'] > 5, f"Expected at least 5 Canvas methods, got {result['canMethodCount']}"

        # Verify some methods exist
        sample_methods = ' '.join(str(m) for m in result['sampleMethods'])
        assert 'rect' in sample_methods or 'circle' in sample_methods, "Expected rect or circle method"

        browser.close()


def test_canvas_methods_have_defaults(http_server):
    """Test that Canvas methods show default parameter values."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the lesson page
        page.goto(f'{http_server}/lessons/theme-1/01-first-flower.html')

        # Wait for page to load (CodeMirror 6)
        page.wait_for_selector('.cm-editor', timeout=10000)

        # Check that methods have default values
        result = page.evaluate('''
            () => {
                const canMethods = window.API_DEFINITIONS['can'];

                // Find rect method (CodeMirror 6 format with label/detail)
                const rectMethod = canMethods.find(m => (m.label || m) === 'rect');
                const rectDetail = rectMethod ? rectMethod.detail : '';

                // Find circle method
                const circleMethod = canMethods.find(m => (m.label || m) === 'circle');
                const circleDetail = circleMethod ? circleMethod.detail : '';

                return {
                    rectDetail: rectDetail,
                    circleDetail: circleDetail,
                    hasDefaults: rectDetail && rectDetail.includes('=')
                };
            }
        ''')

        assert result['hasDefaults'], "Methods should have default values"
        assert result['rectDetail'], "rect method detail should exist"
        assert result['circleDetail'], "circle method detail should exist"

        # Verify defaults are present
        assert '=' in result['rectDetail'], f"rect should have defaults: {result['rectDetail']}"
        assert '=' in result['circleDetail'], f"circle should have defaults: {result['circleDetail']}"

        browser.close()


def test_autocomplete_triggers_on_dot(http_server):
    """Test that autocomplete popup appears when typing 'can.'"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the lesson page
        page.goto(f'{http_server}/lessons/theme-1/01-first-flower.html')

        # Wait for CodeMirror 6 to load
        page.wait_for_selector('.cm-editor', timeout=10000)

        # Focus the editor (CodeMirror 6 uses .cm-content for the editable area)
        page.click('.cm-content')

        # Clear existing content first
        page.keyboard.press('Control+A')
        page.keyboard.press('Backspace')

        # Type "can." to trigger autocomplete
        page.keyboard.type('can.', delay=50)  # Small delay between keystrokes

        # Wait for autocomplete hint popup to appear (CodeMirror 6 uses different classes)
        page.wait_for_selector('.cm-tooltip-autocomplete', timeout=3000)

        # Verify hint popup is visible
        hints = page.locator('.cm-tooltip-autocomplete')
        expect(hints).to_be_visible()

        # Check that hints contain Canvas methods
        hint_text = page.locator('.cm-tooltip-autocomplete').inner_text()
        assert 'rect' in hint_text or 'circle' in hint_text, f"Hints should contain Canvas methods, got: {hint_text}"

        browser.close()


def test_autocomplete_filters_on_typing(http_server):
    """Test that autocomplete filters results when typing."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the lesson page
        page.goto(f'{http_server}/lessons/theme-1/01-first-flower.html')

        # Wait for CodeMirror 6 to load
        page.wait_for_selector('.cm-editor', timeout=10000)

        # Focus the editor
        page.click('.cm-content')

        # Clear existing content first
        page.keyboard.press('Control+A')
        page.keyboard.press('Backspace')

        # Type "can.cir" to trigger filtered autocomplete
        page.keyboard.type('can.cir', delay=50)

        # Wait for autocomplete hint popup (CodeMirror 6)
        page.wait_for_selector('.cm-tooltip-autocomplete', timeout=3000)

        # Verify only circle method is shown (filtered)
        hint_text = page.locator('.cm-tooltip-autocomplete').inner_text()
        assert 'circle' in hint_text, f"Should show circle method, got: {hint_text}"

        # Rect should not be in filtered results
        assert 'rect' not in hint_text.lower(), f"Should not show rect when filtering for 'cir', got: {hint_text}"

        browser.close()


def test_palette_colors_available(http_server):
    """Test that palette color constants are available in autocomplete."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the lesson page
        page.goto(f'{http_server}/lessons/theme-1/01-first-flower.html')

        # Wait for page to load (CodeMirror 6)
        page.wait_for_selector('.cm-editor', timeout=10000)

        # Check that palette colors are extracted
        result = page.evaluate('''
            () => {
                const gardenColors = window.API_DEFINITIONS['CreativeGardenPalette'];
                const oasisColors = window.API_DEFINITIONS['CalmOasisPalette'];
                const basicColors = window.API_DEFINITIONS['Color'];

                // Extract labels from objects (CodeMirror 6 format)
                const gardenLabels = gardenColors ? gardenColors.map(c => c.label || c) : [];
                const basicLabels = basicColors ? basicColors.map(c => c.label || c) : [];

                return {
                    hasGarden: gardenColors && gardenColors.length > 0,
                    hasOasis: oasisColors && oasisColors.length > 0,
                    hasBasic: basicColors && basicColors.length > 0,
                    sampleGarden: gardenLabels.slice(0, 3),
                    sampleBasic: basicLabels.slice(0, 3)
                };
            }
        ''')

        assert result['hasGarden'], "CreativeGardenPalette colors should be available"
        assert result['hasOasis'], "CalmOasisPalette colors should be available"
        assert result['hasBasic'], "Color class colors should be available"

        # Verify some specific colors
        garden_colors = ' '.join(str(c) for c in result['sampleGarden'])
        basic_colors = ' '.join(str(c) for c in result['sampleBasic'])

        assert any(color in garden_colors for color in ['ROSE_QUARTZ', 'BUTTER_YELLOW', 'PEACH_WHISPER']), \
            f"Should have CreativeGardenPalette colors, got: {garden_colors}"
        assert any(color in basic_colors for color in ['RED', 'BLUE', 'GREEN']), \
            f"Should have basic colors, got: {basic_colors}"

        browser.close()


def test_autocomplete_shows_palette_colors(http_server):
    """Test that autocomplete shows palette colors when typing 'CreativeGardenPalette.'"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the lesson page
        page.goto(f'{http_server}/lessons/theme-1/01-first-flower.html')

        # Wait for CodeMirror 6 to load
        page.wait_for_selector('.cm-editor', timeout=10000)

        # Focus the editor
        page.click('.cm-content')

        # Clear existing content first
        page.keyboard.press('Control+A')
        page.keyboard.press('Backspace')

        # Type to trigger palette color autocomplete
        page.keyboard.type('fill = CreativeGardenPalette.')

        # Wait for autocomplete hint popup (CodeMirror 6)
        page.wait_for_selector('.cm-tooltip-autocomplete', timeout=2000)

        # Verify palette colors are shown
        hint_text = page.locator('.cm-tooltip-autocomplete').inner_text()

        # Check for some expected palette colors
        has_palette_colors = any(color in hint_text for color in [
            'ROSE_QUARTZ', 'BUTTER_YELLOW', 'MINT_CREAM',
            'PEACH_WHISPER', 'CORAL_BLUSH'
        ])

        assert has_palette_colors, f"Should show CreativeGardenPalette colors, got: {hint_text}"

        browser.close()


def test_method_signatures_are_single_line(http_server):
    """Test that method signatures are formatted as single lines."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the lesson page
        page.goto(f'{http_server}/lessons/theme-1/01-first-flower.html')

        # Wait for page to load (CodeMirror 6)
        page.wait_for_selector('.cm-editor', timeout=10000)

        # Check that method signatures don't have newlines
        result = page.evaluate('''
            () => {
                const canMethods = window.API_DEFINITIONS['can'];

                // Check detail field for newlines (CodeMirror 6 format)
                const hasNewlines = canMethods.some(m => {
                    const detail = m.detail || '';
                    return detail.includes('\\n');
                });

                // Get sample methods
                const rectMethod = canMethods.find(m => (m.label || m) === 'rect');
                const circleMethod = canMethods.find(m => (m.label || m) === 'circle');

                return {
                    hasNewlines: hasNewlines,
                    rectDetail: rectMethod ? rectMethod.detail : '',
                    circleDetail: circleMethod ? circleMethod.detail : ''
                };
            }
        ''')

        assert not result['hasNewlines'], "Method signatures should not contain newlines"

        # Verify methods are readable single lines
        rect = result['rectDetail']
        circle = result['circleDetail']

        assert rect and '=' in rect, f"rect should be a single line with defaults: {rect}"
        assert circle and '=' in circle, f"circle should be a single line with defaults: {circle}"

        # Verify they're reasonably formatted (not too long)
        assert len(rect) < 200, f"rect signature too long ({len(rect)} chars): {rect}"
        assert len(circle) < 200, f"circle signature too long ({len(circle)} chars): {circle}"

        browser.close()
