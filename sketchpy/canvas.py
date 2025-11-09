"""
Canvas - main drawing surface with SVG rendering.
"""

from typing import List, Tuple, Optional, Dict, Union
import math
import random

# Import palettes (will be available when combined for browser)
try:
    from .palettes import Color
except ImportError:
    # For standalone browser bundle, Color will be defined in same scope
    pass


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

    def pear(self, x: float, y: float, width: float = 80, height: float = 100,
             fill: str = Color.GREEN, stroke: Optional[str] = None,
             stroke_width: int = 1) -> 'Canvas':
        """
        Draw a pear shape (wide at top, narrow at bottom).

        Args:
            x, y: Top center point
            width: Maximum width (at the shoulders)
            height: Total height
            fill: Fill color
            stroke: Optional outline color (defaults to same as fill)
            stroke_width: Outline thickness

        Returns:
            self (for method chaining)

        Examples:
            # Octopus head
            can.pear(400, 200, width=120, height=100, fill=OceanPalette.CORAL)

            # Fruit
            can.pear(300, 150, width=60, height=80, fill=Color.GREEN)
        """
        self._check_shape_limit()

        if stroke is None:
            stroke = fill

        # Generate pear outline using control points
        # Top portion: wide rounded top (head/shoulders)
        top_y = y
        shoulder_y = y + height * 0.3
        waist_y = y + height * 0.6
        bottom_y = y + height

        # Width at different heights
        top_width = width * 0.75  # Slightly narrower at very top
        shoulder_width = width  # Widest point
        waist_width = width * 0.65  # Narrower in middle
        bottom_width = width * 0.55  # Gently rounded at bottom (less pointy)

        # Build the outline using bezier curves
        points = []

        # Right side (top to bottom)
        # Top curve
        for i in range(13):
            t = i / 12
            # Bezier from top to shoulder
            y_pos = top_y + (shoulder_y - top_y) * t
            w = top_width + (shoulder_width - top_width) * t
            # Use smooth curve
            curve_factor = math.sin(t * math.pi / 2)
            points.append((x + w/2 * curve_factor, y_pos))

        # Shoulder to waist
        for i in range(13):
            t = i / 12
            y_pos = shoulder_y + (waist_y - shoulder_y) * t
            w = shoulder_width + (waist_width - shoulder_width) * t
            points.append((x + w/2, y_pos))

        # Waist to bottom
        for i in range(13):
            t = i / 12
            y_pos = waist_y + (bottom_y - waist_y) * t
            w = waist_width + (bottom_width - waist_width) * t
            # Smooth taper
            curve_factor = 1 - (1 - t)**2
            points.append((x + w/2 * (1 - 0.3 * curve_factor), y_pos))

        # Left side (bottom to top) - mirror
        for i in range(13, -1, -1):
            t = i / 12
            y_pos = waist_y + (bottom_y - waist_y) * t
            w = waist_width + (bottom_width - waist_width) * t
            curve_factor = 1 - (1 - t)**2
            points.append((x - w/2 * (1 - 0.3 * curve_factor), y_pos))

        for i in range(12, -1, -1):
            t = i / 12
            y_pos = shoulder_y + (waist_y - shoulder_y) * t
            w = shoulder_width + (waist_width - shoulder_width) * t
            points.append((x - w/2, y_pos))

        for i in range(12, -1, -1):
            t = i / 12
            y_pos = top_y + (shoulder_y - top_y) * t
            w = top_width + (shoulder_width - top_width) * t
            curve_factor = math.sin(t * math.pi / 2)
            points.append((x - w/2 * curve_factor, y_pos))

        return self.polygon(points, fill=fill, stroke=stroke, stroke_width=stroke_width)

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
