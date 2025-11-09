"""
shapes.py - Simple SVG shape library for learning Python
No walking, just drawing. Perfect for building car scenes!
"""

from typing import List, Tuple, Optional, Dict, Union
from dataclasses import dataclass
from enum import Enum
import math
import random


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

class MathDoodlingPalette:
    """
    Ultra-minimal triadic palette for abstract geometric patterns.
    Inspired by classroom compass doodling - overlapping circles creating meditative art.

    Best for: Mathematical patterns, symmetry exploration, transparent layering.
    Use with low opacity (0.15-0.4) for beautiful color mixing effects.
    """
    # Triadic core colors (evenly spaced on color wheel)
    MIST_BLUE = "#93C5FD"       # Soft blue - calm, mathematical, precise
    MIST_ROSE = "#FCA5A5"       # Gentle rose - warmth, creativity, balance
    MIST_MINT = "#86EFAC"       # Light mint - growth, harmony, freshness

    # Extended shades for variety
    DEEP_BLUE = "#3B82F6"       # Deeper blue for contrast
    WARM_CORAL = "#F87171"      # Warmer rose for emphasis
    FRESH_GREEN = "#4ADE80"     # Brighter mint for accents

    # Subtle neutrals for backgrounds
    PAPER_WHITE = "#FAFAFA"     # Very light grey - like notebook paper
    PENCIL_GREY = "#E5E7EB"     # Subtle grey - like pencil guidelines

class OceanPalette:
    """Ocean-themed color palette for sea creatures and underwater scenes."""

    # Blues and greens (water, seaweed)
    DEEP_OCEAN = "#0A2E4D"      # Dark blue depths
    OCEAN_BLUE = "#1E5A8E"      # Medium ocean blue
    SHALLOW_WATER = "#4A90C8"   # Light blue shallows
    SEAFOAM = "#88C7DC"         # Pale blue-green foam
    KELP_GREEN = "#2D5C3F"      # Dark seaweed green
    SEA_GREEN = "#4A8B6F"       # Medium aqua green

    # Creature colors (octopus, fish, coral)
    CORAL = "#E8695C"           # Coral/salmon pink
    PURPLE_CORAL = "#A27BA2"    # Purple octopus
    STARFISH_ORANGE = "#F4A460" # Sandy orange
    TROPICAL_YELLOW = "#FFD966" # Bright yellow fish

    # Accents
    SAND = "#D4C5A9"            # Sandy ocean floor
    SHELL_WHITE = "#F5F1E8"     # Pale shell/pearl

    # Special (semi-transparent concept, rendered as light version)
    TRANSLUCENT_BLUE = "#A8D8EA"  # Light blue for jellyfish

def _bezier_points(p0: Tuple[float, float], p1: Tuple[float, float],
                   p2: Tuple[float, float], p3: Optional[Tuple[float, float]] = None,
                   steps: int = 50) -> List[Tuple[float, float]]:
    """
    Generate points along a Bézier curve.

    Args:
        p0: Start point (x, y)
        p1: First control point (x, y)
        p2: Second control point (x, y) [or end point if quadratic]
        p3: End point (x, y) [None for quadratic]
        steps: Number of sample points

    Returns:
        List of (x, y) tuples along the curve
    """
    points = []
    for i in range(steps + 1):
        t = i / steps
        if p3 is None:  # Quadratic
            x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
            y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
        else:  # Cubic
            x = (1-t)**3 * p0[0] + 3*(1-t)**2*t * p1[0] + 3*(1-t)*t**2 * p2[0] + t**3 * p3[0]
            y = (1-t)**3 * p0[1] + 3*(1-t)**2*t * p1[1] + 3*(1-t)*t**2 * p2[1] + t**3 * p3[1]
        points.append((x, y))
    return points


@dataclass
class Point:
    """A point in 2D space."""
    x: float
    y: float


class GroupContext:
    """Context manager for adding shapes to a named group."""

    def __init__(self, canvas: 'Canvas', name: str):
        self.canvas = canvas
        self.name = name

    def __enter__(self):
        if self.name not in self.canvas.groups:
            self.canvas.groups[self.name] = []
            self.canvas.group_visibility[self.name] = True
            self.canvas.group_transforms[self.name] = ""
        self.canvas.current_group = self.name
        return self.canvas

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.canvas.current_group = None
        return False


class Canvas:
    """Main drawing canvas that collects shapes and renders to SVG."""

    # Class constants for security limits
    MAX_WIDTH = 2000
    MAX_HEIGHT = 2000
    MAX_AREA = 4_000_000  # 2000 * 2000
    MAX_SHAPES = 10_000

    def __init__(self, width: int = 800, height: int = 600, background: str = Color.WHITE):
        """
        Create a canvas with specified dimensions.

        Args:
            width: Canvas width in pixels (max 2000)
            height: Canvas height in pixels (max 2000)
            background: Background color (default: white)

        Raises:
            ValueError: If dimensions exceed limits
        """
        # Security: Enforce size limits
        if width > self.MAX_WIDTH:
            raise ValueError(
                f"Canvas width {width} exceeds maximum {self.MAX_WIDTH}"
            )
        if height > self.MAX_HEIGHT:
            raise ValueError(
                f"Canvas height {height} exceeds maximum {self.MAX_HEIGHT}"
            )
        if width * height > self.MAX_AREA:
            raise ValueError(
                f"Canvas area {width * height} exceeds maximum {self.MAX_AREA}"
            )

        if width <= 0 or height <= 0:
            raise ValueError("Canvas dimensions must be positive")

        self.width = width
        self.height = height
        self.background = background
        self.shapes: List[str] = []
        self.gradients: Dict[str, str] = {}  # gradient_id -> SVG definition
        self.groups: Dict[str, List[str]] = {}  # group_name -> list of shapes
        self.current_group: Optional[str] = None  # active group context
        self.group_transforms: Dict[str, str] = {}  # group_name -> transform attribute
        self.group_visibility: Dict[str, bool] = {}  # group_name -> visible

    def _check_shape_limit(self):
        """Prevent too many shapes (render bomb protection)"""
        total_shapes = len(self.shapes)
        for group_shapes in self.groups.values():
            total_shapes += len(group_shapes)

        if total_shapes >= self.MAX_SHAPES:
            raise ValueError(
                f"Shape limit exceeded ({self.MAX_SHAPES}). "
                "Too many shapes can crash the browser."
            )


    def linear_gradient(self, name: str,
                       start: Tuple[float, float] = (0, 0),
                       end: Tuple[float, float] = (100, 0),
                       colors: Union[List[str], List[Tuple[str, float]], None] = None) -> 'Canvas':
        """
        Define a linear gradient for use in fills.

        Args:
            name: Identifier to use as fill="gradient:{name}"
            start: (x, y) start point in percentages (0-100)
            end: (x, y) end point in percentages (0-100)
            colors: List of (color, offset) tuples. Offset is 0.0-1.0
                    If just colors provided, distribute evenly

        Example:
            canvas.linear_gradient("sunset",
                start=(0, 0), end=(100, 0),
                colors=[("#FF6B6B", 0), ("#FFA500", 0.5), ("#FFD93D", 1.0)])

            # Then use as: canvas.circle(100, 100, 50, fill="gradient:sunset")
        """
        if colors is None:
            colors = [("#000000", 0), ("#FFFFFF", 1)]

        # Auto-distribute offsets if colors is list of strings
        if colors and isinstance(colors[0], str):
            n = len(colors)
            colors = [(color, i/(n-1) if n > 1 else 0) for i, color in enumerate(colors)]

        gradient_id = f"grad_{name}"
        stops = "".join(f'<stop offset="{offset*100}%" stop-color="{color}"/>'
                        for color, offset in colors)

        svg_def = f'''<linearGradient id="{gradient_id}" x1="{start[0]}%" y1="{start[1]}%" x2="{end[0]}%" y2="{end[1]}%">
{stops}
</linearGradient>'''

        self.gradients[name] = svg_def
        return self

    def radial_gradient(self, name: str,
                       center: Tuple[float, float] = (50, 50),
                       radius: float = 50,
                       colors: Union[List[str], List[Tuple[str, float]], None] = None) -> 'Canvas':
        """
        Define a radial gradient for use in fills.

        Args:
            name: Identifier to use as fill="gradient:{name}"
            center: (x, y) center point in percentages (0-100)
            radius: Radius in percentages (0-100)
            colors: List of (color, offset) tuples or just colors
        """
        if colors is None:
            colors = [("#000000", 0), ("#FFFFFF", 1)]

        if colors and isinstance(colors[0], str):
            n = len(colors)
            colors = [(color, i/(n-1) if n > 1 else 0) for i, color in enumerate(colors)]

        gradient_id = f"grad_{name}"
        stops = "".join(f'<stop offset="{offset*100}%" stop-color="{color}"/>'
                        for color, offset in colors)

        svg_def = f'''<radialGradient id="{gradient_id}" cx="{center[0]}%" cy="{center[1]}%" r="{radius}%">
{stops}
</radialGradient>'''

        self.gradients[name] = svg_def
        return self

    def _resolve_fill(self, fill: str) -> str:
        """Convert gradient:{name} to url(#grad_{name}), pass through regular colors."""
        if fill.startswith("gradient:"):
            gradient_name = fill[9:]  # Remove "gradient:" prefix
            return f"url(#grad_{gradient_name})"
        return fill

    def group(self, name: str) -> GroupContext:
        """
        Create a context manager for adding shapes to a named group.

        Example:
            with canvas.group("flower"):
                canvas.circle(100, 100, 20, fill=Color.YELLOW)
                canvas.circle(85, 90, 10, fill=Color.PINK)

            # Later manipulate as a unit
            canvas.move_group("flower", dx=50, dy=30)
            canvas.hide_group("flower")
        """
        return GroupContext(self, name)

    def rect(self, x: float = 0, y: float = 0, width: float = 100, height: float = 100,
             fill: str = Color.BLACK, stroke: str = Color.BLACK,
             stroke_width: float = 1) -> 'Canvas':
        """Draw a rectangle. Returns self for chaining."""
        self._check_shape_limit()
        svg = f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{self._resolve_fill(fill)}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        if self.current_group:
            self.groups[self.current_group].append(svg)
        else:
            self.shapes.append(svg)
        return self
    
    def circle(self, x: float = 50, y: float = 50, radius: float = 25,
               fill: str = Color.BLACK, stroke: str = Color.BLACK,
               stroke_width: float = 1, opacity: float = 1.0) -> 'Canvas':
        """Draw a circle at center (x, y). Returns self for chaining.

        Args:
            opacity: Transparency from 0.0 (invisible) to 1.0 (solid). Default 1.0.
        """
        self._check_shape_limit()
        style_parts = [
            f'fill="{self._resolve_fill(fill)}"',
            f'stroke="{stroke}"',
            f'stroke-width="{stroke_width}"'
        ]
        if opacity < 1.0:
            style_parts.append(f'opacity="{opacity}"')

        svg = f'<circle cx="{x}" cy="{y}" r="{radius}" {" ".join(style_parts)}/>'
        if self.current_group:
            self.groups[self.current_group].append(svg)
        else:
            self.shapes.append(svg)
        return self
    
    def ellipse(self, x: float = 50, y: float = 50, rx: float = 40, ry: float = 25,
                fill: str = Color.BLACK, stroke: str = Color.BLACK,
                stroke_width: float = 1) -> 'Canvas':
        """Draw an ellipse. rx = horizontal radius, ry = vertical radius."""
        self._check_shape_limit()
        svg = f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{self._resolve_fill(fill)}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        if self.current_group:
            self.groups[self.current_group].append(svg)
        else:
            self.shapes.append(svg)
        return self
    
    def line(self, x1: float = 0, y1: float = 0, x2: float = 100, y2: float = 100,
             stroke: str = Color.BLACK, stroke_width: float = 2) -> 'Canvas':
        """Draw a line from (x1, y1) to (x2, y2)."""
        self._check_shape_limit()
        svg = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        if self.current_group:
            self.groups[self.current_group].append(svg)
        else:
            self.shapes.append(svg)
        return self
    
    def polygon(self, points: Optional[List[Tuple[float, float]]] = None,
                fill: str = Color.BLACK, stroke: str = Color.BLACK,
                stroke_width: float = 1) -> 'Canvas':
        """Draw a polygon from a list of (x, y) points."""
        self._check_shape_limit()
        if points is None:
            points = [(50, 0), (100, 100), (0, 100)]  # Default triangle
        points_str = " ".join(f"{x},{y}" for x, y in points)
        svg = f'<polygon points="{points_str}" fill="{self._resolve_fill(fill)}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        if self.current_group:
            self.groups[self.current_group].append(svg)
        else:
            self.shapes.append(svg)
        return self
    
    def text(self, x: float = 0, y: float = 20, text: str = "Hello",
             size: int = 16, fill: str = Color.BLACK,
             font: str = "Arial") -> 'Canvas':
        """Draw text at (x, y). Note: y is the baseline."""
        self._check_shape_limit()
        svg = f'<text x="{x}" y="{y}" font-size="{size}" fill="{self._resolve_fill(fill)}" font-family="{font}">{text}</text>'
        if self.current_group:
            self.groups[self.current_group].append(svg)
        else:
            self.shapes.append(svg)
        return self
    
    def rounded_rect(self, x: float = 0, y: float = 0, width: float = 100, height: float = 100,
                     rx: float = 5, ry: float = 5,
                     fill: str = Color.BLACK, stroke: str = Color.BLACK,
                     stroke_width: float = 1) -> 'Canvas':
        """Draw a rectangle with rounded corners."""
        self._check_shape_limit()
        svg = f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{rx}" ry="{ry}" fill="{self._resolve_fill(fill)}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        if self.current_group:
            self.groups[self.current_group].append(svg)
        else:
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

    def wave(self, x1: float, y1: float, x2: float, y2: float,
             height: float = 20, waves: int = 1,
             stroke: str = Color.BLACK, stroke_width: int = 2) -> 'Canvas':
        """
        Draw a wavy line from (x1, y1) to (x2, y2).

        Args:
            x1, y1: Start point
            x2, y2: End point
            height: Wave amplitude (peak-to-trough distance)
            waves: Number of complete wave cycles
            stroke: Line color
            stroke_width: Line thickness

        Returns:
            self (for method chaining)

        Examples:
            # Gentle ocean wave
            can.wave(0, 300, 800, 300, height=30, waves=3)

            # Choppy water
            can.wave(0, 400, 800, 420, height=10, waves=8)
        """
        self._check_shape_limit()

        # Calculate distance and angle
        dx = x2 - x1
        dy = y2 - y1
        distance = math.sqrt(dx**2 + dy**2)
        angle = math.atan2(dy, dx)

        # Generate points along the wave
        points = []
        steps = max(50, int(waves * 20))  # More points for more waves

        for i in range(steps + 1):
            t = i / steps
            # Position along line
            base_x = x1 + t * dx
            base_y = y1 + t * dy

            # Perpendicular offset (sine wave)
            wave_offset = height * math.sin(t * waves * 2 * math.pi)
            offset_x = -wave_offset * math.sin(angle)
            offset_y = wave_offset * math.cos(angle)

            points.append((base_x + offset_x, base_y + offset_y))

        # Draw as polyline (stroke only, no fill)
        points_str = " ".join(f"{x},{y}" for x, y in points)
        svg = f'<polyline points="{points_str}" fill="none" stroke="{stroke}" stroke-width="{stroke_width}"/>'

        if self.current_group:
            self.groups[self.current_group].append(svg)
        else:
            self.shapes.append(svg)

        return self

    def blob(self, x: float, y: float, radius: float = 50,
             wobble: float = 0.2, points: int = 8,
             fill: str = Color.BLUE, stroke: Optional[str] = None,
             stroke_width: int = 1) -> 'Canvas':
        """
        Draw an organic, irregular circle (like a cartoon cloud or octopus head).
        Uses smooth Bézier curves for a natural, flowing appearance.

        Args:
            x, y: Center point
            radius: Average radius
            wobble: How irregular (0-1, where 0 = perfect circle, 1 = very bumpy)
            points: Number of control points (more = smoother, fewer = bumpier)
            fill: Fill color
            stroke: Optional outline color (defaults to same as fill)
            stroke_width: Outline thickness

        Returns:
            self (for method chaining)

        Examples:
            # Smooth organic shape
            can.blob(400, 300, radius=100, wobble=0.2)

            # Very bumpy cloud
            can.blob(200, 150, radius=60, wobble=0.5, points=6)
        """
        self._check_shape_limit()

        if stroke is None:
            stroke = fill

        # Generate irregular anchor points around a circle
        # To keep shapes convex, only vary radius outward (never inward)
        anchor_points = []
        for i in range(points):
            angle = (i / points) * 2 * math.pi
            # Randomize radius based on wobble, but stay convex (only expand, never shrink)
            # Use a minimum radius to prevent concave shapes
            r = radius * (1 + random.uniform(0, wobble))  # Only positive wobble
            px = x + r * math.cos(angle)
            py = y + r * math.sin(angle)
            anchor_points.append((px, py))

        # Generate smooth curve through anchor points using quadratic Bézier
        # Control points are placed *outside* the direct line to keep convexity
        smooth_points = []

        for i in range(len(anchor_points)):
            # Current anchor point
            p1 = anchor_points[i]
            # Next anchor point (wrap around)
            p2 = anchor_points[(i + 1) % len(anchor_points)]

            # Control point: push it outward from center to maintain convexity
            # Calculate midpoint
            mid_x = (p1[0] + p2[0]) / 2
            mid_y = (p1[1] + p2[1]) / 2

            # Vector from center to midpoint
            dx = mid_x - x
            dy = mid_y - y
            dist = math.sqrt(dx**2 + dy**2)

            # Push control point slightly outward (10-20% further from center)
            if dist > 0:
                push_factor = 1.15  # Push 15% further out
                control_x = x + dx * push_factor
                control_y = y + dy * push_factor
            else:
                control_x = mid_x
                control_y = mid_y

            # Sample the curve between p1 and p2
            curve_points = _bezier_points(
                p1,
                (control_x, control_y),
                p2,
                steps=8  # Fewer steps since we have multiple segments
            )

            # Add all points except the last (to avoid duplicates)
            smooth_points.extend(curve_points[:-1])

        # Use polygon to draw the smooth blob
        return self.polygon(smooth_points, fill=fill, stroke=stroke, stroke_width=stroke_width)

    def tentacle(self, x1: float, y1: float, x2: float, y2: float,
                 curl: float = 0.0, twist: float = 0.0, thickness: float = 20,
                 taper: float = 0.5, fill: str = Color.PURPLE,
                 stroke: Optional[str] = None, stroke_width: int = 1) -> 'Canvas':
        """
        Draw an organic tentacle from (x1, y1) to (x2, y2).
        Can create S-curves and flowing shapes.

        Args:
            x1, y1: Base/thick end
            x2, y2: Tip/thin end
            curl: How much it curves (-1 to 1, 0 = straight)
                  Positive = curves right, negative = curves left
            twist: S-curve amount (0 to 1). Creates secondary curve in opposite direction.
                   0 = simple curve, higher values = more pronounced S-shape
            thickness: Width at base
            taper: How much thinner at tip (0-1, where 1 = same width, 0 = point)
            fill: Tentacle color
            stroke: Optional outline color (defaults to same as fill)
            stroke_width: Outline thickness

        Returns:
            self (for method chaining)

        Examples:
            # Gentle curve to the right
            can.tentacle(400, 300, 300, 500, curl=0.3, thickness=30)

            # S-curve tentacle (natural flowing)
            can.tentacle(400, 300, 300, 500, curl=0.4, twist=0.5, thickness=30)

            # Tight curl to the left
            can.tentacle(400, 300, 500, 500, curl=-0.7, thickness=25)
        """
        self._check_shape_limit()

        if stroke is None:
            stroke = fill

        # Calculate perpendicular direction for control points
        dx = x2 - x1
        dy = y2 - y1
        distance = math.sqrt(dx**2 + dy**2)

        # Perpendicular vector (rotated 90 degrees)
        perp_x = -dy
        perp_y = dx
        perp_len = math.sqrt(perp_x**2 + perp_y**2)
        if perp_len > 0:
            perp_x /= perp_len
            perp_y /= perp_len

        if twist > 0:
            # Use cubic Bézier for S-curve (two control points)
            # First control point: 1/3 along, offset in curl direction
            curl_distance1 = distance * abs(curl) * 0.4
            cx1 = x1 + dx * 0.33 + perp_x * curl_distance1 * (1 if curl > 0 else -1)
            cy1 = y1 + dy * 0.33 + perp_y * curl_distance1 * (1 if curl > 0 else -1)

            # Second control point: 2/3 along, offset in OPPOSITE direction (creates S)
            curl_distance2 = distance * abs(curl) * 0.4 * twist
            cx2 = x1 + dx * 0.67 - perp_x * curl_distance2 * (1 if curl > 0 else -1)
            cy2 = y1 + dy * 0.67 - perp_y * curl_distance2 * (1 if curl > 0 else -1)

            # Generate centerline using cubic Bézier
            centerline = _bezier_points((x1, y1), (cx1, cy1), (cx2, cy2), (x2, y2), steps=50)
        else:
            # Use quadratic Bézier for simple curve (one control point)
            curl_distance = distance * abs(curl) * 0.5
            cx = (x1 + x2) / 2 + perp_x * curl_distance * (1 if curl > 0 else -1)
            cy = (y1 + y2) / 2 + perp_y * curl_distance * (1 if curl > 0 else -1)

            # Generate centerline points using quadratic Bézier
            centerline = _bezier_points((x1, y1), (cx, cy), (x2, y2), steps=50)

        # Generate outline by offsetting perpendicular to centerline
        outline_points = []
        tip_thickness = thickness * taper

        for i, (px, py) in enumerate(centerline):
            t = i / (len(centerline) - 1)
            # Interpolate thickness from base to tip
            current_thickness = thickness * (1 - t) + tip_thickness * t
            half_thickness = current_thickness / 2

            # Calculate perpendicular direction at this point
            if i < len(centerline) - 1:
                next_x, next_y = centerline[i + 1]
                tangent_x = next_x - px
                tangent_y = next_y - py
            else:
                prev_x, prev_y = centerline[i - 1]
                tangent_x = px - prev_x
                tangent_y = py - prev_y

            tangent_len = math.sqrt(tangent_x**2 + tangent_y**2)
            if tangent_len > 0:
                tangent_x /= tangent_len
                tangent_y /= tangent_len

            # Perpendicular offset
            perp_x = -tangent_y
            perp_y = tangent_x

            # Add points on both sides
            outline_points.append((px + perp_x * half_thickness, py + perp_y * half_thickness))

        # Add other side in reverse
        for i in range(len(centerline) - 1, -1, -1):
            px, py = centerline[i]
            t = i / (len(centerline) - 1)
            current_thickness = thickness * (1 - t) + tip_thickness * t
            half_thickness = current_thickness / 2

            # Calculate perpendicular direction
            if i < len(centerline) - 1:
                next_x, next_y = centerline[i + 1]
                tangent_x = next_x - px
                tangent_y = next_y - py
            else:
                prev_x, prev_y = centerline[i - 1]
                tangent_x = px - prev_x
                tangent_y = py - prev_y

            tangent_len = math.sqrt(tangent_x**2 + tangent_y**2)
            if tangent_len > 0:
                tangent_x /= tangent_len
                tangent_y /= tangent_len

            perp_x = -tangent_y
            perp_y = tangent_x

            outline_points.append((px - perp_x * half_thickness, py - perp_y * half_thickness))

        return self.polygon(outline_points, fill=fill, stroke=stroke, stroke_width=stroke_width)

    def move_group(self, name: str, dx: float = 0, dy: float = 0) -> 'Canvas':
        """Move a group by offset (dx, dy)."""
        if name not in self.groups:
            return self

        # Parse existing transform or create new one
        existing = self.group_transforms.get(name, "")
        if existing and "translate" in existing:
            # Extract current translation and add to it
            # For simplicity, replace any existing translate
            import re
            existing = re.sub(r'translate\([^)]+\)', '', existing)

        self.group_transforms[name] = f"translate({dx}, {dy}) {existing}".strip()
        return self

    def rotate_group(self, name: str, angle: float, cx: float = 0, cy: float = 0) -> 'Canvas':
        """Rotate a group by angle degrees around point (cx, cy)."""
        if name not in self.groups:
            return self

        existing = self.group_transforms[name]
        self.group_transforms[name] = f"{existing} rotate({angle}, {cx}, {cy})".strip()
        return self

    def hide_group(self, name: str) -> 'Canvas':
        """Hide a group from rendering."""
        if name in self.group_visibility:
            self.group_visibility[name] = False
        return self

    def show_group(self, name: str) -> 'Canvas':
        """Show a previously hidden group."""
        if name in self.group_visibility:
            self.group_visibility[name] = True
        return self

    def remove_group(self, name: str) -> 'Canvas':
        """Permanently remove a group from the canvas."""
        if name in self.groups:
            del self.groups[name]
            del self.group_visibility[name]
            del self.group_transforms[name]
        return self

    def clear(self) -> 'Canvas':
        """Clear all shapes and groups from the canvas."""
        self.shapes = []
        self.groups = {}
        self.group_transforms = {}
        self.group_visibility = {}
        self.current_group = None
        return self
    
    def to_svg(self) -> str:
        """Generate the complete SVG string."""
        svg_header = f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">'
        svg_background = f'<rect width="100%" height="100%" fill="{self.background}"/>'

        defs_section = ""
        if self.gradients:
            gradient_defs = "".join(self.gradients.values())
            defs_section = f"<defs>{gradient_defs}</defs>"

        # Ungrouped shapes
        ungrouped = ''.join(self.shapes)

        # Grouped shapes
        grouped = ""
        for group_name, shapes in self.groups.items():
            if not self.group_visibility.get(group_name, True):
                continue  # Skip hidden groups

            transform = self.group_transforms.get(group_name, "")
            transform_attr = f' transform="{transform}"' if transform else ""

            group_svg = f'<g id="{group_name}"{transform_attr}>{"".join(shapes)}</g>'
            grouped += group_svg

        svg_footer = '</svg>'

        return svg_header + svg_background + defs_section + ungrouped + grouped + svg_footer
    
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


class OceanShapes:
    """Pre-built ocean creature helpers for educational use."""

    def __init__(self, canvas: Canvas):
        """Initialize with a Canvas instance."""
        self.canvas = canvas

    def octopus(self, x: float, y: float, size: float = 100,
                body_color: str = OceanPalette.CORAL,
                eye_color: str = Color.WHITE) -> 'OceanShapes':
        """
        Draw a cute octopus.

        Args:
            x, y: Center position
            size: Approximate size
            body_color: Main body color
            eye_color: Eye color

        Returns:
            self (for method chaining)

        Example:
            ocean = OceanShapes(can)
            ocean.octopus(400, 200, size=120, body_color=OceanPalette.PURPLE_CORAL)
        """
        head_radius = size * 0.4
        tentacle_length = size * 1.2

        # Draw head (blob for organic look)
        self.canvas.blob(x, y, radius=head_radius, wobble=0.15, points=12,
                        fill=body_color, stroke=body_color, stroke_width=2)

        # Draw 8 tentacles radiating from bottom of head
        num_tentacles = 8
        base_y = y + head_radius * 0.3  # Start tentacles slightly below center

        for i in range(num_tentacles):
            # Spread tentacles in an arc below the octopus
            angle = math.pi * 0.1 + (i / (num_tentacles - 1)) * math.pi * 0.7  # 0.1π to 0.8π

            # Calculate tentacle endpoint
            end_x = x + math.cos(angle) * tentacle_length
            end_y = base_y + math.sin(angle) * tentacle_length

            # Add some curl and twist variation for natural S-curves
            curl = random.uniform(-0.5, 0.5)
            twist = random.uniform(0.6, 0.9)  # Natural flowing S-curves

            # Vary thickness slightly
            thickness = size * 0.15 * random.uniform(0.8, 1.0)

            self.canvas.tentacle(x, base_y, end_x, end_y,
                               curl=curl, twist=twist, thickness=thickness, taper=0.2,
                               fill=body_color, stroke=body_color, stroke_width=1)

        # Draw eyes
        eye_size = size * 0.1
        eye_offset_x = size * 0.15
        eye_offset_y = -size * 0.1

        # Left eye
        self.canvas.circle(x - eye_offset_x, y + eye_offset_y, eye_size,
                          fill=eye_color, stroke=Color.BLACK, stroke_width=2)
        self.canvas.circle(x - eye_offset_x + eye_size * 0.2, y + eye_offset_y,
                          eye_size * 0.5, fill=Color.BLACK, stroke=Color.BLACK)

        # Right eye
        self.canvas.circle(x + eye_offset_x, y + eye_offset_y, eye_size,
                          fill=eye_color, stroke=Color.BLACK, stroke_width=2)
        self.canvas.circle(x + eye_offset_x + eye_size * 0.2, y + eye_offset_y,
                          eye_size * 0.5, fill=Color.BLACK, stroke=Color.BLACK)

        return self

    def jellyfish(self, x: float, y: float, size: float = 80,
                  body_color: str = OceanPalette.TRANSLUCENT_BLUE,
                  tentacle_count: int = 6) -> 'OceanShapes':
        """
        Draw a jellyfish.

        Args:
            x, y: Center of bell (top)
            size: Bell diameter
            body_color: Bell color
            tentacle_count: Number of trailing tentacles

        Returns:
            self (for method chaining)
        """
        bell_radius = size * 0.5

        # Draw bell (slightly flattened blob)
        self.canvas.blob(x, y, radius=bell_radius, wobble=0.1, points=16,
                        fill=body_color, stroke=body_color, stroke_width=1)

        # Draw trailing tentacles
        tentacle_length = size * 1.5
        base_y = y + bell_radius * 0.5

        for i in range(tentacle_count):
            # Spread tentacles across bottom of bell
            offset_x = (i - tentacle_count / 2) * (size * 0.2)
            end_x = x + offset_x + random.uniform(-10, 10)
            end_y = base_y + tentacle_length + random.uniform(-20, 20)

            # Vary curl, twist, and thickness for natural flowing movement
            curl = random.uniform(-0.4, 0.4)
            twist = random.uniform(0.3, 0.8)  # Jellyfish have flowing S-curves
            thickness = size * 0.05 * random.uniform(0.7, 1.0)

            self.canvas.tentacle(x + offset_x * 0.5, base_y, end_x, end_y,
                               curl=curl, twist=twist, thickness=thickness, taper=0.1,
                               fill=body_color, stroke=body_color, stroke_width=1)

        return self

    def seaweed(self, x: float, y: float, height: float = 150,
                sway: float = 0.3, color: str = OceanPalette.KELP_GREEN) -> 'OceanShapes':
        """
        Draw swaying seaweed.

        Args:
            x, y: Base position (ocean floor)
            height: How tall
            sway: How much it curves (0-1)
            color: Seaweed color

        Returns:
            self (for method chaining)
        """
        # Main stem with gentle S-curve for natural sway
        curl = random.uniform(-sway, sway)
        twist = random.uniform(0.2, 0.5)  # Gentle S-curve like underwater plants
        end_x = x + random.uniform(-20, 20)
        end_y = y - height

        self.canvas.tentacle(x, y, end_x, end_y,
                           curl=curl, twist=twist, thickness=height * 0.08, taper=0.6,
                           fill=color, stroke=color, stroke_width=1)

        # Add a few small leaf-like shapes along the stem
        num_leaves = random.randint(3, 5)
        for i in range(num_leaves):
            t = (i + 1) / (num_leaves + 1)  # Position along stem
            leaf_x = x + (end_x - x) * t
            leaf_y = y + (end_y - y) * t

            # Small blob for leaf
            leaf_size = height * 0.08
            self.canvas.blob(leaf_x + random.uniform(-5, 5), leaf_y,
                           radius=leaf_size, wobble=0.3, points=6,
                           fill=color, stroke=color)

        return self
