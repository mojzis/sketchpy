"""Tests for lesson starter files."""

import ast
from pathlib import Path

import pytest

# Import the classes needed by lessons
from sketchpy.shapes import Canvas, Color, CreativeGardenPalette, CalmOasisPalette


PROJECT_ROOT = Path(__file__).parent.parent
LESSONS_DIR = PROJECT_ROOT / 'lessons'


def get_lesson_starter_files():
    """Find all starter.py files in lessons directory."""
    return sorted(LESSONS_DIR.glob('*/starter.py'))


def create_pyodide_namespace():
    """Create a namespace that mimics the Pyodide environment.

    In Pyodide, classes are available globally and imports are blocked.
    This namespace blocks imports like the real environment does.
    """
    namespace = {
        'Canvas': Canvas,
        'Color': Color,
        'CreativeGardenPalette': CreativeGardenPalette,
        'CalmOasisPalette': CalmOasisPalette,
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
    """Test that lessons don't use imports (matches Pyodide environment)."""
    code = starter_file.read_text()
    lesson_name = starter_file.parent.name
    validate_no_imports(code, lesson_name)


@pytest.mark.parametrize('starter_file', get_lesson_starter_files())
def test_lesson_starter_executes(starter_file):
    """Test that each lesson's starter.py executes without errors."""
    # Read the starter code
    code = starter_file.read_text()
    lesson_name = starter_file.parent.name

    # First validate no imports (matches Pyodide AST validation)
    validate_no_imports(code, lesson_name)

    # Create namespace with required classes (matches Pyodide globals)
    namespace = create_pyodide_namespace()

    # Execute the starter code
    try:
        exec(code, namespace)
    except Exception as e:
        pytest.fail(f"Lesson {lesson_name} starter.py failed: {e}")


@pytest.mark.parametrize('starter_file', get_lesson_starter_files())
def test_lesson_creates_canvas(starter_file):
    """Test that each lesson creates and returns a Canvas instance."""
    code = starter_file.read_text()
    lesson_name = starter_file.parent.name

    # Create namespace (matches Pyodide)
    namespace = create_pyodide_namespace()

    # Execute the starter code
    exec(code, namespace)

    # Check that 'can' variable exists and is a Canvas
    assert 'can' in namespace, f"Lesson {lesson_name} does not create 'can' variable"
    assert isinstance(namespace['can'], Canvas), \
        f"Lesson {lesson_name} 'can' is not a Canvas instance"


@pytest.mark.parametrize('starter_file', get_lesson_starter_files())
def test_lesson_draws_shapes(starter_file):
    """Test that each lesson actually draws shapes on the canvas."""
    code = starter_file.read_text()
    lesson_name = starter_file.parent.name

    # Create namespace (matches Pyodide)
    namespace = create_pyodide_namespace()

    # Execute the starter code
    exec(code, namespace)

    # Check that shapes were added
    canvas = namespace['can']
    assert len(canvas.shapes) > 0, \
        f"Lesson {lesson_name} does not draw any shapes"


@pytest.mark.parametrize('starter_file', get_lesson_starter_files())
def test_lesson_generates_valid_svg(starter_file):
    """Test that each lesson generates valid SVG output."""
    code = starter_file.read_text()
    lesson_name = starter_file.parent.name

    # Create namespace (matches Pyodide)
    namespace = create_pyodide_namespace()

    # Execute the starter code
    exec(code, namespace)

    # Generate SVG
    canvas = namespace['can']
    svg = canvas.to_svg()

    # Basic SVG validation
    assert svg.startswith('<svg'), f"Lesson {lesson_name} SVG doesn't start with <svg"
    assert svg.endswith('</svg>'), f"Lesson {lesson_name} SVG doesn't end with </svg>"
    assert 'width=' in svg, f"Lesson {lesson_name} SVG missing width attribute"
    assert 'height=' in svg, f"Lesson {lesson_name} SVG missing height attribute"
