"""Tests for lesson starter files."""

from pathlib import Path

import pytest

# Import the classes needed by lessons
from sketchpy.shapes import Canvas, Color, CreativeGardenPalette, CalmOasisPalette


PROJECT_ROOT = Path(__file__).parent.parent
LESSONS_DIR = PROJECT_ROOT / 'lessons'


def get_lesson_starter_files():
    """Find all starter.py files in lessons directory."""
    return sorted(LESSONS_DIR.glob('*/starter.py'))


@pytest.mark.parametrize('starter_file', get_lesson_starter_files())
def test_lesson_starter_executes(starter_file):
    """Test that each lesson's starter.py executes without errors."""
    # Read the starter code
    code = starter_file.read_text()

    # Create namespace with required classes
    namespace = {
        'Canvas': Canvas,
        'Color': Color,
        'CreativeGardenPalette': CreativeGardenPalette,
        'CalmOasisPalette': CalmOasisPalette,
    }

    # Execute the starter code
    try:
        exec(code, namespace)
    except Exception as e:
        pytest.fail(f"Lesson {starter_file.parent.name} starter.py failed: {e}")


@pytest.mark.parametrize('starter_file', get_lesson_starter_files())
def test_lesson_creates_canvas(starter_file):
    """Test that each lesson creates and returns a Canvas instance."""
    # Read the starter code
    code = starter_file.read_text()

    # Create namespace with required classes
    namespace = {
        'Canvas': Canvas,
        'Color': Color,
        'CreativeGardenPalette': CreativeGardenPalette,
        'CalmOasisPalette': CalmOasisPalette,
    }

    # Execute the starter code
    exec(code, namespace)

    # Check that 'can' variable exists and is a Canvas
    assert 'can' in namespace, f"Lesson {starter_file.parent.name} does not create 'can' variable"
    assert isinstance(namespace['can'], Canvas), \
        f"Lesson {starter_file.parent.name} 'can' is not a Canvas instance"


@pytest.mark.parametrize('starter_file', get_lesson_starter_files())
def test_lesson_draws_shapes(starter_file):
    """Test that each lesson actually draws shapes on the canvas."""
    # Read the starter code
    code = starter_file.read_text()

    # Create namespace with required classes
    namespace = {
        'Canvas': Canvas,
        'Color': Color,
        'CreativeGardenPalette': CreativeGardenPalette,
        'CalmOasisPalette': CalmOasisPalette,
    }

    # Execute the starter code
    exec(code, namespace)

    # Check that shapes were added
    canvas = namespace['can']
    assert len(canvas.shapes) > 0, \
        f"Lesson {starter_file.parent.name} does not draw any shapes"


@pytest.mark.parametrize('starter_file', get_lesson_starter_files())
def test_lesson_generates_valid_svg(starter_file):
    """Test that each lesson generates valid SVG output."""
    # Read the starter code
    code = starter_file.read_text()

    # Create namespace with required classes
    namespace = {
        'Canvas': Canvas,
        'Color': Color,
        'CreativeGardenPalette': CreativeGardenPalette,
        'CalmOasisPalette': CalmOasisPalette,
    }

    # Execute the starter code
    exec(code, namespace)

    # Generate SVG
    canvas = namespace['can']
    svg = canvas.to_svg()

    # Basic SVG validation
    assert svg.startswith('<svg'), f"Lesson {starter_file.parent.name} SVG doesn't start with <svg"
    assert svg.endswith('</svg>'), f"Lesson {starter_file.parent.name} SVG doesn't end with </svg>"
    assert 'width=' in svg, f"Lesson {starter_file.parent.name} SVG missing width attribute"
    assert 'height=' in svg, f"Lesson {starter_file.parent.name} SVG missing height attribute"
