"""Tests for the build process."""

import re
import subprocess
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).parent.parent
# Use first lesson file for testing (multi-lesson structure)
OUTPUT_FILE = PROJECT_ROOT / 'output' / 'lessons' / '01-first-flower.html'


def test_build_command_runs_successfully():
    """Test that the build command runs without errors."""
    result = subprocess.run(
        ['uv', 'run', 'build'],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Build failed: {result.stderr}"
    # Build logs to stderr with new format: "🔨 Built output/index.html"
    assert "Built output/index.html" in result.stderr or len(result.stderr) == 0, \
        f"Unexpected build output: {result.stderr}"


def test_output_file_exists():
    """Test that the output file is created."""
    # Run build first
    subprocess.run(['uv', 'run', 'build'], cwd=PROJECT_ROOT, check=True)

    assert OUTPUT_FILE.exists(), f"Output file not found at {OUTPUT_FILE}"
    assert OUTPUT_FILE.stat().st_size > 0, "Output file is empty"


def test_generated_python_syntax():
    """Test that the generated Python code is syntactically valid."""
    # Run build first
    subprocess.run(['uv', 'run', 'build'], cwd=PROJECT_ROOT, check=True)

    # Read the output file
    content = OUTPUT_FILE.read_text()

    # Extract Python code from the template (now in window.SHAPES_CODE)
    match = re.search(
        r'window\.SHAPES_CODE = `(.*?)`;',
        content,
        re.DOTALL
    )
    assert match is not None, "Could not find Python code in generated HTML (window.SHAPES_CODE)"
    python_code = match.group(1)

    # Try to compile the Python code
    try:
        compile(python_code, '<generated>', 'exec')
    except SyntaxError as e:
        pytest.fail(f"Generated Python code has syntax error: {e}\n\nCode:\n{python_code}")


def test_generated_code_has_required_classes():
    """Test that the generated code includes required classes."""
    # Run build first
    subprocess.run(['uv', 'run', 'build'], cwd=PROJECT_ROOT, check=True)

    content = OUTPUT_FILE.read_text()
    match = re.search(
        r'window\.SHAPES_CODE = `(.*?)`;',
        content,
        re.DOTALL
    )
    assert match is not None, "Could not find Python code in generated HTML (window.SHAPES_CODE)"
    python_code = match.group(1)

    # Check for required classes and methods
    assert 'class Color:' in python_code, "Color class not found"
    assert 'class Canvas:' in python_code, "Canvas class not found"
    assert 'def rect(' in python_code, "rect method not found"
    assert 'def circle(' in python_code, "circle method not found"
    assert 'def to_svg(' in python_code, "to_svg method not found"


def test_generated_code_excludes_browser_incompatible():
    """Test that browser-incompatible code is excluded."""
    # Run build first
    subprocess.run(['uv', 'run', 'build'], cwd=PROJECT_ROOT, check=True)

    content = OUTPUT_FILE.read_text()
    match = re.search(
        r'window\.SHAPES_CODE = `(.*?)`;',
        content,
        re.DOTALL
    )
    assert match is not None, "Could not find Python code in generated HTML (window.SHAPES_CODE)"
    python_code = match.group(1)

    # These should NOT be in the generated code
    assert 'def save(' not in python_code, "save() method should be excluded"
    assert 'class Point' not in python_code, "Point class should be excluded"
    assert '@dataclass' not in python_code, "dataclass decorator should be excluded"
    assert 'class CarShapes' not in python_code, "CarShapes should be excluded"


def test_generated_code_has_required_imports():
    """Test that the generated code has required imports."""
    # Run build first
    subprocess.run(['uv', 'run', 'build'], cwd=PROJECT_ROOT, check=True)

    content = OUTPUT_FILE.read_text()
    match = re.search(
        r'window\.SHAPES_CODE = `(.*?)`;',
        content,
        re.DOTALL
    )
    assert match is not None, "Could not find Python code in generated HTML (window.SHAPES_CODE)"
    python_code = match.group(1)

    # Check for required imports
    assert 'from typing import' in python_code, "typing import missing"

    # These should NOT be imported (not needed)
    assert 'from dataclasses import' not in python_code, "dataclasses should not be imported"
    assert 'from enum import' not in python_code, "enum should not be imported"


def test_generated_code_has_repr_html():
    """Test that _repr_html_ is included for marimo support."""
    # Run build first
    subprocess.run(['uv', 'run', 'build'], cwd=PROJECT_ROOT, check=True)

    content = OUTPUT_FILE.read_text()
    match = re.search(
        r'window\.SHAPES_CODE = `(.*?)`;',
        content,
        re.DOTALL
    )
    assert match is not None, "Could not find Python code in generated HTML (window.SHAPES_CODE)"
    python_code = match.group(1)

    # Check for _repr_html_ method (needed for marimo)
    assert '_repr_html_' in python_code, "_repr_html_ method should be included for marimo support"


def test_generated_code_size():
    """Test that the generated code is reasonably sized (not too bloated)."""
    # Run build first
    subprocess.run(['uv', 'run', 'build'], cwd=PROJECT_ROOT, check=True)

    content = OUTPUT_FILE.read_text()
    match = re.search(
        r'window\.SHAPES_CODE = `(.*?)`;',
        content,
        re.DOTALL
    )
    assert match is not None, "Could not find Python code in generated HTML (window.SHAPES_CODE)"
    python_code = match.group(1)

    # The generated Python code should be reasonable size (less than 20KB)
    # Increased from 10KB due to gradients and named groups features
    code_size = len(python_code)
    assert code_size < 20000, f"Generated code is too large: {code_size} bytes (expected < 20KB)"
    assert code_size > 1000, f"Generated code seems too small: {code_size} bytes (expected > 1KB)"


def test_index_page_has_snippets():
    """Test that the index.html landing page includes snippet data."""
    # Run build first
    subprocess.run(['uv', 'run', 'build'], cwd=PROJECT_ROOT, check=True)

    index_file = PROJECT_ROOT / 'output' / 'index.html'
    assert index_file.exists(), "index.html should exist"

    content = index_file.read_text()

    # Check that snippets are embedded
    assert 'const snippets' in content, "index.html should contain snippets data"
    assert '"name":' in content, "Snippets should have name property"
    assert '"code":' in content, "Snippets should have code property"
    assert '"svg":' in content, "Snippets should have svg property"


def test_index_page_has_svg_output():
    """Test that the index.html has SVG output embedded."""
    # Run build first
    subprocess.run(['uv', 'run', 'build'], cwd=PROJECT_ROOT, check=True)

    index_file = PROJECT_ROOT / 'output' / 'index.html'
    content = index_file.read_text()

    # Check that SVG is present in the initial render
    assert '<svg' in content, "index.html should have SVG elements"
    assert 'width=' in content, "SVG should have width attribute"
    assert 'height=' in content, "SVG should have height attribute"


def test_index_page_snippet_rotation():
    """Test that the index.html includes snippet rotation JavaScript."""
    # Run build first
    subprocess.run(['uv', 'run', 'build'], cwd=PROJECT_ROOT, check=True)

    index_file = PROJECT_ROOT / 'output' / 'index.html'
    content = index_file.read_text()

    # Check that the rotation logic is present
    assert 'setInterval' in content, "Should have interval for rotation"
    assert 'currentSnippet' in content, "Should track current snippet index"
    assert 'svgOutput' in content, "Should reference SVG output element"
