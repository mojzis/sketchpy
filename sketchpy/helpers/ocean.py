"""
Ocean-themed shape helpers for drawing sea creatures.
"""

import math
import random

# Imports will be available when combined for browser
try:
    from ..canvas import Canvas
    from ..palettes import Color, OceanPalette
except ImportError:
    # For standalone browser bundle, these will be defined in same scope
    pass


class OceanShapes:
    """Pre-built ocean creature helpers for educational use."""

    def __init__(self, canvas: 'Canvas'):
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
