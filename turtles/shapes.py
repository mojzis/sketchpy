"""
shapes.py - Simple SVG shape library for learning Python
No walking, just drawing. Perfect for building car scenes!
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class Color:
    """Common colors with good IDE completion."""
    RED = "#FF0000"
    BLUE = "#0000FF"
    GREEN = "#00FF00"
    YELLOW = "#FFFF00"
    BLACK = "#000000"
    WHITE = "#FFFFFF"
    GRAY = "#808080"
    ORANGE = "#FFA500"
    PURPLE = "#800080"
    PINK = "#FFC0CB"
    BROWN = "#8B4513"
    SILVER = "#C0C0C0"


@dataclass
class Point:
    """A point in 2D space."""
    x: float
    y: float


class Canvas:
    """Main drawing canvas that collects shapes and renders to SVG."""
    
    def __init__(self, width: int = 800, height: int = 600, background: str = Color.WHITE):
        self.width = width
        self.height = height
        self.background = background
        self.shapes: List[str] = []
    
    def rect(self, x: float, y: float, width: float, height: float, 
             fill: str = Color.BLACK, stroke: str = Color.BLACK, 
             stroke_width: float = 1) -> 'Canvas':
        """Draw a rectangle. Returns self for chaining."""
        svg = f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        self.shapes.append(svg)
        return self
    
    def circle(self, x: float, y: float, radius: float, 
               fill: str = Color.BLACK, stroke: str = Color.BLACK, 
               stroke_width: float = 1) -> 'Canvas':
        """Draw a circle at center (x, y). Returns self for chaining."""
        svg = f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        self.shapes.append(svg)
        return self
    
    def ellipse(self, x: float, y: float, rx: float, ry: float,
                fill: str = Color.BLACK, stroke: str = Color.BLACK,
                stroke_width: float = 1) -> 'Canvas':
        """Draw an ellipse. rx = horizontal radius, ry = vertical radius."""
        svg = f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        self.shapes.append(svg)
        return self
    
    def line(self, x1: float, y1: float, x2: float, y2: float,
             stroke: str = Color.BLACK, stroke_width: float = 2) -> 'Canvas':
        """Draw a line from (x1, y1) to (x2, y2)."""
        svg = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        self.shapes.append(svg)
        return self
    
    def polygon(self, points: List[Tuple[float, float]], 
                fill: str = Color.BLACK, stroke: str = Color.BLACK,
                stroke_width: float = 1) -> 'Canvas':
        """Draw a polygon from a list of (x, y) points."""
        points_str = " ".join(f"{x},{y}" for x, y in points)
        svg = f'<polygon points="{points_str}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        self.shapes.append(svg)
        return self
    
    def text(self, x: float, y: float, text: str, 
             size: int = 16, fill: str = Color.BLACK,
             font: str = "Arial") -> 'Canvas':
        """Draw text at (x, y). Note: y is the baseline."""
        svg = f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-family="{font}">{text}</text>'
        self.shapes.append(svg)
        return self
    
    def rounded_rect(self, x: float, y: float, width: float, height: float,
                     rx: float = 5, ry: float = 5,
                     fill: str = Color.BLACK, stroke: str = Color.BLACK,
                     stroke_width: float = 1) -> 'Canvas':
        """Draw a rectangle with rounded corners."""
        svg = f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        self.shapes.append(svg)
        return self
    
    def clear(self) -> 'Canvas':
        """Clear all shapes from the canvas."""
        self.shapes = []
        return self
    
    def to_svg(self) -> str:
        """Generate the complete SVG string."""
        svg_header = f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">'
        svg_background = f'<rect width="100%" height="100%" fill="{self.background}"/>'
        svg_footer = '</svg>'
        
        return svg_header + svg_background + ''.join(self.shapes) + svg_footer
    
    def save(self, filename: str) -> None:
        """Save the canvas to an SVG file."""
        with open(filename, 'w') as f:
            f.write(self.to_svg())
        print(f"Saved to {filename}")
    
    def show(self) -> str:
        """Display in Jupyter/marimo. Returns SVG string."""
        from IPython.display import SVG, display
        display(SVG(self.to_svg()))
        return self.to_svg()
    
    def _repr_svg_(self):
        """Automatic display in Jupyter notebooks."""
        return self.to_svg()

    def _repr_html_(self):
        """Automatic display in marimo."""
        return self.to_svg()


# Convenience functions for quick sketching
def quick_draw(width: int = 800, height: int = 600) -> Canvas:
    """Create a canvas quickly for sketching."""
    return Canvas(width, height)


# Higher-level car-themed shapes
class CarShapes:
    """Pre-made car-themed shapes for easy drawing."""
    
    @staticmethod
    def simple_car(canvas: Canvas, x: float, y: float, 
                   width: float = 120, height: float = 50,
                   color: str = Color.RED) -> Canvas:
        """Draw a simple side-view car."""
        # Body
        canvas.rounded_rect(x, y, width, height, rx=5, fill=color, stroke=Color.BLACK, stroke_width=2)
        
        # Roof (windshield area)
        roof_width = width * 0.4
        roof_height = height * 0.6
        canvas.polygon([
            (x + width * 0.25, y),
            (x + width * 0.35, y - roof_height),
            (x + width * 0.65, y - roof_height),
            (x + width * 0.75, y)
        ], fill=color, stroke=Color.BLACK, stroke_width=2)
        
        # Wheels
        wheel_radius = height * 0.35
        canvas.circle(x + width * 0.25, y + height, wheel_radius, 
                     fill=Color.BLACK, stroke=Color.GRAY, stroke_width=2)
        canvas.circle(x + width * 0.75, y + height, wheel_radius,
                     fill=Color.BLACK, stroke=Color.GRAY, stroke_width=2)
        
        return canvas
    
    @staticmethod
    def wheel(canvas: Canvas, x: float, y: float, radius: float = 20,
              tire_color: str = Color.BLACK, rim_color: str = Color.SILVER) -> Canvas:
        """Draw a detailed wheel."""
        # Tire
        canvas.circle(x, y, radius, fill=tire_color)
        # Rim
        canvas.circle(x, y, radius * 0.6, fill=rim_color, stroke=Color.GRAY, stroke_width=2)
        # Hub
        canvas.circle(x, y, radius * 0.2, fill=Color.GRAY)
        return canvas
    
    @staticmethod
    def traffic_light(canvas: Canvas, x: float, y: float,
                      active: str = "red") -> Canvas:
        """Draw a traffic light. active can be 'red', 'yellow', or 'green'."""
        # Housing
        canvas.rounded_rect(x, y, 60, 180, rx=10, fill=Color.BLACK, stroke=Color.GRAY, stroke_width=3)
        
        # Lights
        colors = {
            "red": (Color.RED, Color.GRAY, Color.GRAY),
            "yellow": (Color.GRAY, Color.YELLOW, Color.GRAY),
            "green": (Color.GRAY, Color.GRAY, Color.GREEN)
        }
        
        red, yellow, green = colors.get(active, colors["red"])
        
        canvas.circle(x + 30, y + 30, 20, fill=red, stroke=Color.BLACK, stroke_width=2)
        canvas.circle(x + 30, y + 90, 20, fill=yellow, stroke=Color.BLACK, stroke_width=2)
        canvas.circle(x + 30, y + 150, 20, fill=green, stroke=Color.BLACK, stroke_width=2)
        
        return canvas
    
    @staticmethod
    def road(canvas: Canvas, y: float, lane_width: float = 60,
             num_lanes: int = 2) -> Canvas:
        """Draw a horizontal road with lanes."""
        road_height = lane_width * num_lanes
        
        # Road surface
        canvas.rect(0, y, canvas.width, road_height, fill=Color.GRAY)
        
        # Lane markers (dashed lines)
        dash_width = 40
        gap_width = 20
        
        for lane in range(1, num_lanes):
            line_y = y + lane * lane_width
            x = 0
            while x < canvas.width:
                canvas.rect(x, line_y - 2, dash_width, 4, fill=Color.YELLOW)
                x += dash_width + gap_width
        
        return canvas
