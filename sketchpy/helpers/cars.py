"""
Car-themed shape helpers for drawing vehicles and traffic scenes.
"""

# Imports will be available when combined for browser
try:
    from ..canvas import Canvas
    from ..palettes import Color
except ImportError:
    # For standalone browser bundle, these will be defined in same scope
    pass


class CarShapes:
    """Pre-made car-themed shapes for easy drawing."""

    def __init__(self, canvas: 'Canvas'):
        """Initialize with a Canvas instance."""
        self.canvas = canvas
        self._setup_gradients()

    def _setup_gradients(self):
        """Register predefined gradients for car shapes."""
        # Metallic car body paint with sky reflection
        self.canvas.linear_gradient(
            "car_metallic_shine",
            start=(0, 0),    # Top
            end=(0, 100),    # Bottom
            colors=[
                ("#FFB3B3", 0),      # Highlight (sky reflection)
                ("#FF6B6B", 0.3),    # Upper body
                ("#E04040", 0.7),    # Lower body (darker)
                ("#A03030", 1.0)     # Shadow/undercarriage
            ]
        )

        # Tire rubber shading
        self.canvas.radial_gradient(
            "car_tire_rubber",
            center=(30, 30),  # Light source from upper-left
            radius=70,
            colors=[
                ("#3A3A3A", 0),      # Lighter rubber
                (Color.BLACK, 1.0)   # Deep black
            ]
        )

        # Chrome/silver rim shine
        self.canvas.radial_gradient(
            "car_chrome_rim",
            center=(40, 40),
            radius=60,
            colors=[
                ("#FFFFFF", 0),      # Bright reflection
                (Color.SILVER, 0.5),
                ("#808080", 1.0)     # Darker metal edge
            ]
        )

        # Traffic light glow effects
        self.canvas.radial_gradient(
            "car_light_glow_red",
            center=(50, 50),
            radius=70,
            colors=[
                ("#FFCCCC", 0),      # Bright center
                (Color.RED, 0.6),
                ("#AA0000", 1.0)     # Dark edge
            ]
        )

        self.canvas.radial_gradient(
            "car_light_glow_yellow",
            center=(50, 50),
            radius=70,
            colors=[("#FFFFCC", 0), (Color.YELLOW, 0.6), ("#CCAA00", 1.0)]
        )

        self.canvas.radial_gradient(
            "car_light_glow_green",
            center=(50, 50),
            radius=70,
            colors=[("#CCFFCC", 0), (Color.GREEN, 0.6), ("#00AA00", 1.0)]
        )

    def simple_car(self, x: float, y: float,
                   width: float = 120, height: float = 50,
                   color: str = "gradient:car_metallic_shine") -> 'CarShapes':
        """Draw a simple side-view car."""
        # Body
        self.canvas.rounded_rect(x, y, width, height, rx=5, fill=color, stroke=Color.BLACK, stroke_width=2)

        # Roof (windshield area)
        roof_width = width * 0.4
        roof_height = height * 0.6
        self.canvas.polygon([
            (x + width * 0.25, y),
            (x + width * 0.35, y - roof_height),
            (x + width * 0.65, y - roof_height),
            (x + width * 0.75, y)
        ], fill=color, stroke=Color.BLACK, stroke_width=2)

        # Wheels
        wheel_radius = height * 0.35
        self.canvas.circle(x + width * 0.25, y + height, wheel_radius,
                     fill=Color.BLACK, stroke=Color.GRAY, stroke_width=2)
        self.canvas.circle(x + width * 0.75, y + height, wheel_radius,
                     fill=Color.BLACK, stroke=Color.GRAY, stroke_width=2)

        return self

    def wheel(self, x: float, y: float, radius: float = 20,
              tire_color: str = "gradient:car_tire_rubber",
              rim_color: str = "gradient:car_chrome_rim") -> 'CarShapes':
        """Draw a detailed wheel."""
        # Tire
        self.canvas.circle(x, y, radius, fill=tire_color)
        # Rim
        self.canvas.circle(x, y, radius * 0.6, fill=rim_color, stroke=Color.GRAY, stroke_width=2)
        # Hub
        self.canvas.circle(x, y, radius * 0.2, fill=Color.GRAY)
        return self

    def traffic_light(self, x: float, y: float,
                      active: str = "red") -> 'CarShapes':
        """Draw a traffic light. active can be 'red', 'yellow', or 'green'."""
        # Housing
        self.canvas.rounded_rect(x, y, 60, 180, rx=10, fill=Color.BLACK, stroke=Color.GRAY, stroke_width=3)

        # Lights with gradient glow when active
        colors = {
            "red": ("gradient:car_light_glow_red", Color.GRAY, Color.GRAY),
            "yellow": (Color.GRAY, "gradient:car_light_glow_yellow", Color.GRAY),
            "green": (Color.GRAY, Color.GRAY, "gradient:car_light_glow_green")
        }

        red, yellow, green = colors.get(active, colors["red"])

        self.canvas.circle(x + 30, y + 30, 20, fill=red, stroke=Color.BLACK, stroke_width=2)
        self.canvas.circle(x + 30, y + 90, 20, fill=yellow, stroke=Color.BLACK, stroke_width=2)
        self.canvas.circle(x + 30, y + 150, 20, fill=green, stroke=Color.BLACK, stroke_width=2)

        return self

    def road(self, y: float, lane_width: float = 60,
             num_lanes: int = 2) -> 'CarShapes':
        """Draw a horizontal road with lanes."""
        road_height = lane_width * num_lanes

        # Road surface
        self.canvas.rect(0, y, self.canvas.width, road_height, fill=Color.GRAY)

        # Lane markers (dashed lines)
        dash_width = 40
        gap_width = 20

        for lane in range(1, num_lanes):
            line_y = y + lane * lane_width
            x = 0
            while x < self.canvas.width:
                self.canvas.rect(x, line_y - 2, dash_width, 4, fill=Color.YELLOW)
                x += dash_width + gap_width

        return self
