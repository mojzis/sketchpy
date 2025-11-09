"""
sketchpy - Simple SVG shape library for learning Python through visual art.

A browser-first graphics library that works in Jupyter notebooks, marimo,
and web browsers via Pyodide. Emphasizes ease of learning with direct shape
drawing (no turtle paradigm).
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
