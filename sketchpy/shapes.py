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

class CalmOasisPalette:
    """
    Calming palette focused on therapeutic blues, greens, and lavenders.
    Best for: Focus, relaxation, reducing anxiety, promoting peaceful work.
    """
    SKY_BLUE = "#A5C8E4"        # Soft, calming blue - promotes tranquility
    MINT_FRESH = "#B0E0A8"      # Gentle green - reduces stress, aids focus
    LAVENDER_MIST = "#E5DAFF"   # Soft purple - encourages creativity & calm
    POWDER_BLUE = "#BFEFFF"     # Light blue - soothing, spacious feeling
    SAGE_GREEN = "#C0ECCC"      # Tea green - natural, peaceful, clarity
    PERIWINKLE = "#CCCCFF"      # Blue-purple - thoughtful, gentle
    CREAM = "#FFF7D4"           # Warm neutral - safe, comfortable
    SOFT_AQUA = "#AFDFE5"       # Aqua - refreshing, balanced
    PALE_LILAC = "#E6D5FF"      # Lilac - imaginative, serene
    CLOUD_WHITE = "#F5F5F5"     # Off-white - spacious, clean
    MIST_GRAY = "#D3D3D3"       # Light gray - neutral, grounding
    SEAFOAM = "#C8FFE1"         # Mint-aqua - healing, optimistic

class CreativeGardenPalette:
    """
    Broader pastel palette for creative expression while staying calm.
    Best for: Variety, self-expression, encouraging creativity, balanced energy.
    """
    PEACH_WHISPER = "#FFDAC1"   # Soft peach - warm, friendly, gentle
    ROSE_QUARTZ = "#F6A8A6"     # Muted pink - nurturing, empathetic
    BUTTER_YELLOW = "#FFF0A3"   # Soft yellow - optimistic, clear thinking
    MINT_CREAM = "#C0ECCC"      # Mint green - fresh, balanced, growth
    SKY_BREEZE = "#A5C8E4"      # Powder blue - peaceful, trustworthy
    LILAC_DREAM = "#D5C3E0"     # Soft lilac - creative, sophisticated
    CORAL_BLUSH = "#FFB3B3"     # Gentle coral - energetic but not overwhelming
    LEMON_CHIFFON = "#F9F0C1"   # Pale yellow - joyful, light
    MISTY_MAUVE = "#E8D4E8"     # Soft mauve - elegant, calming
    HONEYDEW = "#E8F5E3"        # Very pale green - restful, natural
    VANILLA_CREAM = "#FAF0E6"   # Warm white - cozy, safe
    DOVE_GRAY = "#D5D5D5"       # Soft gray - stable, grounding

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
    
    def rect(self, x: float = 0, y: float = 0, width: float = 100, height: float = 100,
             fill: str = Color.BLACK, stroke: str = Color.BLACK,
             stroke_width: float = 1) -> 'Canvas':
        """Draw a rectangle. Returns self for chaining."""
        svg = f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        self.shapes.append(svg)
        return self
    
    def circle(self, x: float = 50, y: float = 50, radius: float = 25,
               fill: str = Color.BLACK, stroke: str = Color.BLACK,
               stroke_width: float = 1) -> 'Canvas':
        """Draw a circle at center (x, y). Returns self for chaining."""
        svg = f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        self.shapes.append(svg)
        return self
    
    def ellipse(self, x: float = 50, y: float = 50, rx: float = 40, ry: float = 25,
                fill: str = Color.BLACK, stroke: str = Color.BLACK,
                stroke_width: float = 1) -> 'Canvas':
        """Draw an ellipse. rx = horizontal radius, ry = vertical radius."""
        svg = f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        self.shapes.append(svg)
        return self
    
    def line(self, x1: float = 0, y1: float = 0, x2: float = 100, y2: float = 100,
             stroke: str = Color.BLACK, stroke_width: float = 2) -> 'Canvas':
        """Draw a line from (x1, y1) to (x2, y2)."""
        svg = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        self.shapes.append(svg)
        return self
    
    def polygon(self, points: List[Tuple[float, float]] = None,
                fill: str = Color.BLACK, stroke: str = Color.BLACK,
                stroke_width: float = 1) -> 'Canvas':
        """Draw a polygon from a list of (x, y) points."""
        if points is None:
            points = [(50, 0), (100, 100), (0, 100)]  # Default triangle
        points_str = " ".join(f"{x},{y}" for x, y in points)
        svg = f'<polygon points="{points_str}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        self.shapes.append(svg)
        return self
    
    def text(self, x: float = 0, y: float = 20, text: str = "Hello",
             size: int = 16, fill: str = Color.BLACK,
             font: str = "Arial") -> 'Canvas':
        """Draw text at (x, y). Note: y is the baseline."""
        svg = f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-family="{font}">{text}</text>'
        self.shapes.append(svg)
        return self
    
    def rounded_rect(self, x: float = 0, y: float = 0, width: float = 100, height: float = 100,
                     rx: float = 5, ry: float = 5,
                     fill: str = Color.BLACK, stroke: str = Color.BLACK,
                     stroke_width: float = 1) -> 'Canvas':
        """Draw a rectangle with rounded corners."""
        svg = f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        self.shapes.append(svg)
        return self
    
    def grid(self, spacing: int = 50, color: str = "#E8E8E8",
             show_coords: bool = True) -> 'Canvas':
        """
        Draw a coordinate grid on the canvas with subtle grey lines.

        Args:
            spacing: Distance between grid lines in pixels (default: 50)
            color: Color of grid lines (default: very light grey)
            show_coords: Whether to show coordinate labels (default: True)
        """
        # Draw vertical lines
        x = spacing
        while x < self.width:
            self.line(x, 0, x, self.height, stroke=color, stroke_width=0.5)
            if show_coords and x % (spacing * 2) == 0:  # Show coords every 2nd line
                self.text(x + 2, 12, str(x), size=10, fill="#AAAAAA")
            x += spacing

        # Draw horizontal lines
        y = spacing
        while y < self.height:
            self.line(0, y, self.width, y, stroke=color, stroke_width=0.5)
            if show_coords and y % (spacing * 2) == 0:  # Show coords every 2nd line
                self.text(2, y - 2, str(y), size=10, fill="#AAAAAA")
            y += spacing

        # Draw origin marker (0,0) at top-left
        if show_coords:
            self.text(2, 12, "(0,0)", size=10, fill="#888888")

        return self

    def show_palette(self, palette_class, rect_width: float = 120, rect_height: float = 60,
                     columns: int = 4, padding: float = 10, start_x: float = 20,
                     start_y: float = 20) -> 'Canvas':
        """
        Display all colors from a palette class as colored rectangles with labels.

        Args:
            palette_class: A palette class (e.g., CreativeGardenPalette, CalmOasisPalette)
            rect_width: Width of each color rectangle (default: 120)
            rect_height: Height of each color rectangle (default: 60)
            columns: Number of columns in the grid (default: 4)
            padding: Padding between rectangles (default: 10)
            start_x: Starting x position (default: 20)
            start_y: Starting y position (default: 20)
        """
        # Get all color attributes from the palette class
        colors = [(name, value) for name, value in vars(palette_class).items()
                  if not name.startswith('_') and isinstance(value, str)]

        # Draw each color as a rectangle with label
        for i, (name, color_value) in enumerate(colors):
            row = i // columns
            col = i % columns

            x = start_x + col * (rect_width + padding)
            y = start_y + row * (rect_height + padding)

            # Draw colored rectangle
            self.rounded_rect(x, y, rect_width, rect_height, rx=5,
                            fill=color_value, stroke=Color.GRAY, stroke_width=1)

            # Draw color name
            self.text(x + rect_width / 2 - len(name) * 3, y + rect_height / 2 + 5,
                     name, size=11, fill=Color.BLACK, font="monospace")

            # Draw hex value
            self.text(x + rect_width / 2 - len(color_value) * 3, y + rect_height - 10,
                     color_value, size=9, fill=Color.GRAY, font="monospace")

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
