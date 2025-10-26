"""Tests for snippet execution and SVG generation."""

import pytest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.build import execute_snippet, load_snippets


def test_snippet_execution():
    """Test that snippets can be executed successfully."""
    project_root = Path(__file__).parent.parent
    snippets_dir = project_root / 'snippets'

    # Ensure snippets directory exists
    assert snippets_dir.exists(), "Snippets directory should exist"

    # Get all snippet files
    snippet_files = list(snippets_dir.glob('*.py'))
    assert len(snippet_files) > 0, "Should have at least one snippet file"

    # Test each snippet
    for snippet_file in snippet_files:
        result = execute_snippet(snippet_file, project_root)
        assert result is not None, f"Snippet {snippet_file.name} failed to execute"
        assert 'name' in result, f"Result should have 'name' key"
        assert 'code' in result, f"Result should have 'code' key"
        assert 'svg' in result, f"Result should have 'svg' key"


def test_snippet_svg_generation():
    """Test that snippets generate valid SVG output."""
    project_root = Path(__file__).parent.parent
    snippets = load_snippets(project_root)

    assert len(snippets) > 0, "Should load at least one snippet"

    for snippet in snippets:
        svg = snippet['svg']
        # Check that SVG contains expected tags
        assert '<svg' in svg, f"Snippet {snippet['name']} should generate SVG with <svg> tag"
        assert 'width=' in svg, f"Snippet {snippet['name']} should have width attribute"
        assert 'height=' in svg, f"Snippet {snippet['name']} should have height attribute"
        assert '</svg>' in svg, f"Snippet {snippet['name']} should have closing </svg> tag"


def test_snippet_uses_palettes():
    """Test that snippets use the new color palettes."""
    project_root = Path(__file__).parent.parent
    snippets = load_snippets(project_root)

    assert len(snippets) > 0, "Should load at least one snippet"

    palette_found = False
    for snippet in snippets:
        code = snippet['code']
        # Check if any snippet uses CreativeGardenPalette or CalmOasisPalette
        if 'CreativeGardenPalette' in code or 'CalmOasisPalette' in code:
            palette_found = True
            break

    assert palette_found, "At least one snippet should use CreativeGardenPalette or CalmOasisPalette"


def test_snippet_code_not_empty():
    """Test that snippet code is not empty."""
    project_root = Path(__file__).parent.parent
    snippets = load_snippets(project_root)

    assert len(snippets) > 0, "Should load at least one snippet"

    for snippet in snippets:
        code = snippet['code']
        assert len(code) > 0, f"Snippet {snippet['name']} should have non-empty code"
        assert 'can = Canvas(' in code, f"Snippet {snippet['name']} should create a Canvas"
        assert 'can' in code, f"Snippet {snippet['name']} should reference 'can' variable"


def test_snippet_names():
    """Test that snippet names are correctly extracted."""
    project_root = Path(__file__).parent.parent
    snippets = load_snippets(project_root)

    assert len(snippets) > 0, "Should load at least one snippet"

    for snippet in snippets:
        name = snippet['name']
        assert len(name) > 0, "Snippet name should not be empty"
        assert ' ' not in name or '_' in name, "Snippet name should be snake_case"
