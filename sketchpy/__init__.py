"""
sketchpy - Simple SVG shape library for learning Python through visual art.

A browser-first graphics library that works in Jupyter notebooks, marimo,
and web browsers via Pyodide. Emphasizes ease of learning with direct shape
drawing (no turtle paradigm).

Quick Example:
    >>> from sketchpy import Canvas, Color
    >>> can = Canvas(400, 400)
    >>> can.circle(200, 200, 50, fill=Color.RED)
    >>> can.rect(150, 250, 100, 80, fill=Color.BLUE)
    >>> can.save("output.svg")

Key Features:
    - Zero dependencies (pure Python)
    - Browser-native (runs in Pyodide)
    - Notebook-friendly (marimo, Jupyter)
    - Method chaining for elegant code
    - Rich color palettes
    - Organic shapes (blobs, tentacles, waves)
    - Educational helper shapes

Available Classes:
    Canvas: Main drawing surface
    Color: Basic 12-color palette
    CalmOasisPalette: Calming blues/greens
    CreativeGardenPalette: Pastel creative colors
    MathDoodlingPalette: Triadic geometric palette
    OceanPalette: Ocean-themed colors
    OceanShapes: Ocean creature helpers
    CarShapes: Vehicle helpers
"""

# Core classes
from .canvas import Canvas
from .palettes import (
    Color,
    CalmOasisPalette,
    CreativeGardenPalette,
    MathDoodlingPalette,
    OceanPalette
)

# Helper shape classes
from .helpers import OceanShapes, CarShapes

# Utility classes and functions (local development only)
from .utils import Point, quick_draw

__all__ = [
    # Core
    'Canvas',
    # Palettes
    'Color',
    'CalmOasisPalette',
    'CreativeGardenPalette',
    'MathDoodlingPalette',
    'OceanPalette',
    # Helpers
    'OceanShapes',
    'CarShapes',
    # Utils (local only, not in browser)
    'Point',
    'quick_draw',
]

__version__ = '0.1.0'
