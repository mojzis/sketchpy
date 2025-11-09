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

    @staticmethod
    def simple_car(canvas: 'Canvas', x: float, y: float,
                   width: float = 120, height: float = 50,
                   color: str = Color.RED) -> 'Canvas':
        """Draw a simple side-view car with slightly rounded body."""
        # Body (slightly more rounded)
        canvas.rounded_rect(x, y, width, height, rx=10, ry=8, fill=color, stroke=Color.BLACK, stroke_width=2)

        # Roof (windshield area) - slightly more rounded
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
    def rounded_car(canvas: 'Canvas', x: float, y: float,
                    width: float = 140, height: float = 50,
                    color: str = Color.BLUE) -> 'Canvas':
        """Draw a modern car with smooth, curvy body using organic shapes."""
        # Main body - use ellipse for smooth, rounded appearance
        body_height = height * 0.8
        canvas.ellipse(x + width/2, y + body_height/2,
                      rx=width/2, ry=body_height/2,
                      fill=color, stroke=Color.BLACK, stroke_width=2)

        # Roof/cabin - smaller ellipse on top
        roof_width = width * 0.5
        roof_height = height * 0.5
        canvas.ellipse(x + width/2, y + roof_height/2 - height * 0.1,
                      rx=roof_width/2, ry=roof_height/2,
                      fill=color, stroke=Color.BLACK, stroke_width=2)

        # Windows - semi-transparent ellipses
        window_color = "#87CEEB"  # Sky blue
        window_width = roof_width * 0.35
        window_height = roof_height * 0.6
        # Front window
        canvas.ellipse(x + width * 0.6, y + roof_height/2 - height * 0.1,
                      rx=window_width/2, ry=window_height/2,
                      fill=window_color, stroke=Color.BLACK, stroke_width=1,
                      opacity=0.6)
        # Back window
        canvas.ellipse(x + width * 0.4, y + roof_height/2 - height * 0.1,
                      rx=window_width/2, ry=window_height/2,
                      fill=window_color, stroke=Color.BLACK, stroke_width=1,
                      opacity=0.6)

        # Wheels - use ellipses for modern look
        wheel_width = height * 0.4
        wheel_height = height * 0.35
        # Front wheel
        canvas.ellipse(x + width * 0.7, y + height,
                      rx=wheel_width/2, ry=wheel_height/2,
                      fill=Color.BLACK, stroke=Color.GRAY, stroke_width=2)
        canvas.circle(x + width * 0.7, y + height, wheel_height * 0.4,
                     fill=Color.SILVER)
        # Back wheel
        canvas.ellipse(x + width * 0.3, y + height,
                      rx=wheel_width/2, ry=wheel_height/2,
                      fill=Color.BLACK, stroke=Color.GRAY, stroke_width=2)
        canvas.circle(x + width * 0.3, y + height, wheel_height * 0.4,
                     fill=Color.SILVER)

        # Headlights - small circles
        canvas.circle(x + width * 0.95, y + body_height * 0.6,
                     radius=height * 0.1, fill=Color.YELLOW)

        return canvas

    @staticmethod
    def sports_car(canvas: 'Canvas', x: float, y: float,
                   width: float = 160, height: float = 40,
                   color: str = Color.RED) -> 'Canvas':
        """Draw a sleek sports car with aerodynamic curves."""
        # Low, wide body - elongated ellipse
        body_height = height * 0.7
        canvas.ellipse(x + width/2, y + body_height/2,
                      rx=width/2, ry=body_height/2,
                      fill=color, stroke=Color.BLACK, stroke_width=2)

        # Sleek windshield - very flat ellipse
        roof_width = width * 0.35
        roof_height = height * 0.45
        canvas.ellipse(x + width * 0.55, y + roof_height/2 - height * 0.05,
                      rx=roof_width/2, ry=roof_height/2,
                      fill=color, stroke=Color.BLACK, stroke_width=2)

        # Dark tinted window
        canvas.ellipse(x + width * 0.55, y + roof_height/2 - height * 0.05,
                      rx=roof_width/2 * 0.8, ry=roof_height/2 * 0.7,
                      fill="#1a1a1a", stroke=Color.BLACK, stroke_width=1,
                      opacity=0.8)

        # Small spoiler at back - use polygon
        spoiler_y = y + roof_height/2 - height * 0.2
        canvas.polygon([
            (x + width * 0.15, spoiler_y),
            (x + width * 0.15, spoiler_y - height * 0.15),
            (x + width * 0.25, spoiler_y - height * 0.15),
            (x + width * 0.25, spoiler_y)
        ], fill=Color.BLACK, stroke=Color.BLACK, stroke_width=1)

        # Wide, low-profile wheels
        wheel_width = height * 0.5
        wheel_height = height * 0.4
        # Front wheel
        canvas.ellipse(x + width * 0.75, y + height,
                      rx=wheel_width/2, ry=wheel_height/2,
                      fill=Color.BLACK, stroke=Color.GRAY, stroke_width=2)
        canvas.circle(x + width * 0.75, y + height, wheel_height * 0.35,
                     fill=Color.SILVER)
        # Back wheel
        canvas.ellipse(x + width * 0.25, y + height,
                      rx=wheel_width/2, ry=wheel_height/2,
                      fill=Color.BLACK, stroke=Color.GRAY, stroke_width=2)
        canvas.circle(x + width * 0.25, y + height, wheel_height * 0.35,
                     fill=Color.SILVER)

        # Aggressive headlights
        canvas.circle(x + width * 0.97, y + body_height * 0.5,
                     radius=height * 0.12, fill=Color.WHITE)

        return canvas

    @staticmethod
    def bus(canvas: 'Canvas', x: float, y: float,
            width: float = 200, height: float = 120,
            color: str = Color.YELLOW) -> 'Canvas':
        """Draw a city bus with rounded corners and windows."""
        # Main body - large rounded rectangle
        canvas.rounded_rect(x, y, width, height, rx=15, ry=15,
                           fill=color, stroke=Color.BLACK, stroke_width=3)

        # Windows - grid of rounded rectangles
        window_width = width * 0.15
        window_height = height * 0.25
        window_spacing = width * 0.18
        window_y = y + height * 0.25

        for i in range(4):
            window_x = x + width * 0.15 + i * window_spacing
            canvas.rounded_rect(window_x, window_y, window_width, window_height,
                               rx=5, ry=5, fill="#87CEEB",
                               stroke=Color.BLACK, stroke_width=2,
                               opacity=0.7)

        # Destination sign on top front
        canvas.rounded_rect(x + width * 0.05, y + height * 0.05,
                           width * 0.3, height * 0.12, rx=3, ry=3,
                           fill=Color.BLACK, stroke=Color.BLACK, stroke_width=1)
        canvas.text(x + width * 0.08, y + height * 0.12, "CITY",
                   size=int(height * 0.08), fill=Color.YELLOW)

        # Front door - rounded rectangle
        canvas.rounded_rect(x + width * 0.85, y + height * 0.4,
                           width * 0.1, height * 0.5, rx=5, ry=5,
                           fill="#666666", stroke=Color.BLACK, stroke_width=2)

        # Multiple wheels
        wheel_radius = height * 0.15
        # Front wheels
        canvas.circle(x + width * 0.8, y + height + wheel_radius * 0.3,
                     wheel_radius, fill=Color.BLACK, stroke=Color.GRAY, stroke_width=2)
        canvas.circle(x + width * 0.8, y + height + wheel_radius * 0.3,
                     wheel_radius * 0.5, fill=Color.SILVER)
        # Back wheels (dual)
        canvas.circle(x + width * 0.2, y + height + wheel_radius * 0.3,
                     wheel_radius, fill=Color.BLACK, stroke=Color.GRAY, stroke_width=2)
        canvas.circle(x + width * 0.2, y + height + wheel_radius * 0.3,
                     wheel_radius * 0.5, fill=Color.SILVER)
        canvas.circle(x + width * 0.3, y + height + wheel_radius * 0.3,
                     wheel_radius, fill=Color.BLACK, stroke=Color.GRAY, stroke_width=2)
        canvas.circle(x + width * 0.3, y + height + wheel_radius * 0.3,
                     wheel_radius * 0.5, fill=Color.SILVER)

        # Headlights
        canvas.circle(x + width * 0.95, y + height * 0.7,
                     radius=height * 0.08, fill=Color.WHITE)

        return canvas

    @staticmethod
    def wheel(canvas: 'Canvas', x: float, y: float, radius: float = 20,
              tire_color: str = Color.BLACK, rim_color: str = Color.SILVER) -> 'Canvas':
        """Draw a detailed wheel."""
        # Tire
        canvas.circle(x, y, radius, fill=tire_color)
        # Rim
        canvas.circle(x, y, radius * 0.6, fill=rim_color, stroke=Color.GRAY, stroke_width=2)
        # Hub
        canvas.circle(x, y, radius * 0.2, fill=Color.GRAY)
        return canvas

    @staticmethod
    def traffic_light(canvas: 'Canvas', x: float, y: float,
                      active: str = "red") -> 'Canvas':
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
    def road(canvas: 'Canvas', y: float, lane_width: float = 60,
             num_lanes: int = 2) -> 'Canvas':
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
