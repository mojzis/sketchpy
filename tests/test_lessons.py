"""Tests for lesson starter files."""

import ast
from pathlib import Path

import pytest

# Import the classes needed by lessons
from sketchpy.shapes import Canvas, Color, CreativeGardenPalette, CalmOasisPalette

# Import the extraction function from build.py
from scripts.build import extract_main_function_body


PROJECT_ROOT = Path(__file__).parent.parent
LESSONS_DIR = PROJECT_ROOT / 'themes'


def get_lesson_starter_files():
    """Find all starter.py files in lessons directory."""
    return sorted(LESSONS_DIR.glob('*/*/starter.py'))


def create_pyodide_namespace():
    """Create a namespace that mimics the Pyodide environment.

    In Pyodide, classes are available globally and imports are blocked.
    This namespace blocks imports like the real environment does.
    """
    import math
    from sketchpy.shapes import MathDoodlingPalette

    namespace = {
        'Canvas': Canvas,
        'Color': Color,
        'CreativeGardenPalette': CreativeGardenPalette,
        'CalmOasisPalette': CalmOasisPalette,
        'MathDoodlingPalette': MathDoodlingPalette,
        'math': math,  # Math module for trigonometry
        '__builtins__': __builtins__,
    }
    return namespace


def validate_no_imports(code, lesson_name):
    """Validate that code doesn't use imports (matches Pyodide AST validation)."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        pytest.fail(f"Lesson {lesson_name} has syntax error: {e}")

    # Check for imports - matches pyodide-worker.js validation
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest.fail(
                f"Lesson {lesson_name} uses 'import' statement (line {node.lineno}). "
                "Imports are blocked in Pyodide. Canvas, Color, and palettes are "
                "already available!"
            )

        if isinstance(node, ast.ImportFrom):
            pytest.fail(
                f"Lesson {lesson_name} uses 'from...import' statement (line {node.lineno}). "
                "Imports are blocked in Pyodide. Canvas, Color, and palettes are "
                "already available!"
            )


@pytest.mark.parametrize('starter_file', get_lesson_starter_files())
def test_lesson_no_imports(starter_file):
    """Test that the extracted web code doesn't use imports (matches Pyodide environment).

    Note: The raw starter.py files now have imports for local execution,
    but the build process extracts only the main() function body without imports.
    """
    full_code = starter_file.read_text()
    lesson_name = starter_file.parent.name

    # Extract the main function body (what actually gets sent to the browser)
    web_code = extract_main_function_body(full_code)

    # Validate that the web code has no imports
    validate_no_imports(web_code, lesson_name)


@pytest.mark.parametrize('starter_file', get_lesson_starter_files())
def test_lesson_starter_executes(starter_file):
    """Test that each lesson's starter.py executes without errors (both locally and in browser).

    Tests two scenarios:
    1. Local execution: Full file with imports and main() function
    2. Browser execution: Extracted main() body without imports
    """
    full_code = starter_file.read_text()
    lesson_name = starter_file.parent.name

    # Test 1: Local execution (full file with imports)
    try:
        exec(full_code, {})  # Execute with empty namespace (imports will load classes)
    except Exception as e:
        pytest.fail(f"Lesson {lesson_name} starter.py local execution failed: {e}")

    # Test 2: Browser execution (extracted main body without imports)
    web_code = extract_main_function_body(full_code)
    validate_no_imports(web_code, lesson_name)

    namespace = create_pyodide_namespace()
    try:
        exec(web_code, namespace)
    except Exception as e:
        pytest.fail(f"Lesson {lesson_name} web code execution failed: {e}")


@pytest.mark.parametrize('starter_file', get_lesson_starter_files())
def test_lesson_creates_canvas(starter_file):
    """Test that each lesson creates and returns a Canvas instance."""
    full_code = starter_file.read_text()
    lesson_name = starter_file.parent.name

    # Extract web code and execute in Pyodide-like environment
    web_code = extract_main_function_body(full_code)
    namespace = create_pyodide_namespace()
    exec(web_code, namespace)

    # Check that 'can' variable exists and is a Canvas
    assert 'can' in namespace, f"Lesson {lesson_name} does not create 'can' variable"
    assert isinstance(namespace['can'], Canvas), \
        f"Lesson {lesson_name} 'can' is not a Canvas instance"


@pytest.mark.parametrize('starter_file', get_lesson_starter_files())
def test_lesson_draws_shapes(starter_file):
    """Test that each lesson actually draws shapes on the canvas."""
    full_code = starter_file.read_text()
    lesson_name = starter_file.parent.name

    # Extract web code and execute in Pyodide-like environment
    web_code = extract_main_function_body(full_code)
    namespace = create_pyodide_namespace()
    exec(web_code, namespace)

    # Check that shapes were added
    canvas = namespace['can']
    assert len(canvas.shapes) > 0, \
        f"Lesson {lesson_name} does not draw any shapes"


@pytest.mark.parametrize('starter_file', get_lesson_starter_files())
def test_lesson_generates_valid_svg(starter_file):
    """Test that each lesson generates valid SVG output."""
    full_code = starter_file.read_text()
    lesson_name = starter_file.parent.name

    # Extract web code and execute in Pyodide-like environment
    web_code = extract_main_function_body(full_code)
    namespace = create_pyodide_namespace()
    exec(web_code, namespace)

    # Generate SVG
    canvas = namespace['can']
    svg = canvas.to_svg()

    # Basic SVG validation
    assert svg.startswith('<svg'), f"Lesson {lesson_name} SVG doesn't start with <svg"
    assert svg.endswith('</svg>'), f"Lesson {lesson_name} SVG doesn't end with </svg>"
    assert 'width=' in svg, f"Lesson {lesson_name} SVG missing width attribute"
    assert 'height=' in svg, f"Lesson {lesson_name} SVG missing height attribute"
