"""
Car-themed shape helpers for drawing vehicles and traffic scenes.
"""

# Imports will be available when combined for browser
from ..canvas import Canvas
from ..palettes import Color


class CarShapes:
    """Pre-made car-themed shapes for easy drawing."""

    @staticmethod
    def simple_car(canvas: 'Canvas', x: float, y: float,
                   width: float = 120, height: float = 50,
                   color: str = Color.RED) -> 'Canvas':
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
