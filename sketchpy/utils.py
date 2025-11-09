"""
Utility classes and functions for local development (not included in browser bundle).
"""

from dataclasses import dataclass
from .canvas import Canvas


@dataclass
class Point:
    """A point in 2D space."""
    x: float
    y: float


def quick_draw(width: int = 800, height: int = 600) -> Canvas:
    """Create a canvas quickly for sketching."""
    return Canvas(width, height)
