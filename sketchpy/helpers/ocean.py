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
                eye_color: str = Color.WHITE,
                style: str = "classic") -> 'OceanShapes':
        """
        Draw a cute octopus with improved anatomy.

        Args:
            x, y: Top center of head
            size: Approximate size
            body_color: Main body color
            eye_color: Eye color
            style: "classic", "realistic", or "cartoon"

        Returns:
            self (for method chaining)

        Example:
            ocean = OceanShapes(can)
            ocean.octopus(400, 200, size=120, body_color=OceanPalette.PURPLE_CORAL)
            ocean.octopus(400, 400, size=120, style="realistic")
        """
        if style == "realistic":
            return self.octopus_realistic(x, y, size, body_color, eye_color)
        elif style == "cartoon":
            return self.octopus_cartoon(x, y, size, body_color, eye_color)

        # Classic style with pear-shaped head
        head_width = size * 0.8
        head_height = size * 0.75
        tentacle_length = size * 1.2

        # Draw tentacles FIRST (so they appear behind the head)
        num_tentacles = 8
        # Attach tentacles closer to head (at 85% of head height)
        base_y = y + head_height * 0.85

        # At 85% height, pear width is approximately head_width * 0.59
        # Reduce further to account for tentacle thickness at angles
        attachment_width = head_width * 0.35

        for i in range(num_tentacles):
            # Spread tentacles in an arc below the octopus
            angle = math.pi * 0.15 + (i / (num_tentacles - 1)) * math.pi * 0.7

            # Calculate tentacle endpoint
            end_x = x + math.cos(angle) * tentacle_length
            end_y = base_y + math.sin(angle) * tentacle_length

            # Add some curl and twist variation for natural S-curves
            curl = random.uniform(-0.5, 0.5)
            twist = random.uniform(0.6, 0.9)

            # Vary thickness slightly
            thickness = size * 0.12 * random.uniform(0.8, 1.0)

            # Calculate attachment point within body outline
            # Account for tentacle thickness by keeping them more centered
            attach_offset = (i - (num_tentacles - 1) / 2) * (attachment_width / (num_tentacles - 1))
            attach_x = x + attach_offset

            self.canvas.tentacle(attach_x, base_y, end_x, end_y,
                               curl=curl, twist=twist, thickness=thickness, taper=0.2,
                               fill=body_color, stroke=body_color, stroke_width=1)

        # Draw pear-shaped head AFTER tentacles (appears in front)
        self.canvas.pear(x, y, width=head_width, height=head_height,
                        fill=body_color, stroke=body_color, stroke_width=2)

        # Draw eyes (smaller)
        eye_size = size * 0.06
        eye_offset_x = size * 0.15
        eye_offset_y = size * 0.22

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

    def octopus_realistic(self, x: float, y: float, size: float = 100,
                         body_color: str = OceanPalette.CORAL,
                         eye_color: str = Color.WHITE) -> 'OceanShapes':
        """
        Draw a realistic octopus with grouped tentacles (4 per side).

        Args:
            x, y: Top center of head
            size: Approximate size
            body_color: Main body color
            eye_color: Eye color

        Returns:
            self (for method chaining)
        """
        head_width = size * 0.85
        head_height = size * 0.8
        tentacle_length = size * 1.3

        # Draw tentacles FIRST in two groups (left and right)
        num_tentacles = 8
        # Attach closer to head
        base_y = y + head_height * 0.85

        # At 85% height, pear width is approximately head_width * 0.59
        # Reduce to account for tentacle thickness at angles
        group_width = head_width * 0.18

        for i in range(num_tentacles):
            # Group tentacles: 4 on left, 4 on right with gaps in middle
            if i < 4:
                # Left group - spread from center-left to outer-left edge
                angle = math.pi * 0.42 + (i / 3) * math.pi * 0.16
                # Attach points spread within left side of body
                attach_x = x - (group_width * (1 - i / 3))
            else:
                # Right group - spread from center-right to outer-right edge
                angle = math.pi * 0.58 + ((i - 4) / 3) * math.pi * 0.16
                # Attach points spread within right side of body
                attach_x = x + (group_width * (1 - (i - 4) / 3))

            # Calculate tentacle endpoint
            end_x = attach_x + math.cos(angle) * tentacle_length
            end_y = base_y + math.sin(angle) * tentacle_length

            # More natural curl variation
            curl = random.uniform(-0.4, 0.4)
            twist = random.uniform(0.5, 0.8)

            thickness = size * 0.13 * random.uniform(0.85, 1.0)

            self.canvas.tentacle(attach_x, base_y, end_x, end_y,
                               curl=curl, twist=twist, thickness=thickness, taper=0.15,
                               fill=body_color, stroke=body_color, stroke_width=1)

        # Draw pear-shaped head
        self.canvas.pear(x, y, width=head_width, height=head_height,
                        fill=body_color, stroke=body_color, stroke_width=2)

        # Draw eyes (smaller)
        eye_size = size * 0.07
        eye_offset_x = size * 0.18
        eye_offset_y = size * 0.25

        # Left eye
        self.canvas.circle(x - eye_offset_x, y + eye_offset_y, eye_size,
                          fill=eye_color, stroke=Color.BLACK, stroke_width=2)
        self.canvas.circle(x - eye_offset_x + eye_size * 0.25, y + eye_offset_y,
                          eye_size * 0.45, fill=Color.BLACK, stroke=Color.BLACK)

        # Right eye
        self.canvas.circle(x + eye_offset_x, y + eye_offset_y, eye_size,
                          fill=eye_color, stroke=Color.BLACK, stroke_width=2)
        self.canvas.circle(x + eye_offset_x + eye_size * 0.25, y + eye_offset_y,
                          eye_size * 0.45, fill=Color.BLACK, stroke=Color.BLACK)

        return self

    def octopus_cartoon(self, x: float, y: float, size: float = 100,
                       body_color: str = OceanPalette.CORAL,
                       eye_color: str = Color.WHITE) -> 'OceanShapes':
        """
        Draw a cartoon octopus with exaggerated features and curly tentacles.

        Args:
            x, y: Top center of head
            size: Approximate size
            body_color: Main body color
            eye_color: Eye color

        Returns:
            self (for method chaining)
        """
        head_width = size * 0.9
        head_height = size * 0.7
        tentacle_length = size * 1.4

        # Draw very curly tentacles FIRST
        num_tentacles = 8
        # Attach closer to head
        base_y = y + head_height * 0.85

        # At 85% height, pear width is approximately head_width * 0.59
        # Account for thicker tentacles in cartoon style
        attachment_width = head_width * 0.4

        for i in range(num_tentacles):
            # Wide spread for cartoon effect
            angle = math.pi * 0.12 + (i / (num_tentacles - 1)) * math.pi * 0.76

            # Calculate tentacle endpoint
            end_x = x + math.cos(angle) * tentacle_length
            end_y = base_y + math.sin(angle) * tentacle_length

            # Exaggerated curl and twist
            curl = random.uniform(-0.7, 0.7)
            twist = random.uniform(0.7, 1.0)  # More S-curves

            thickness = size * 0.14 * random.uniform(0.9, 1.1)

            # Calculate attachment point within body outline
            attach_offset = (i - (num_tentacles - 1) / 2) * (attachment_width / (num_tentacles - 1))
            attach_x = x + attach_offset

            self.canvas.tentacle(attach_x, base_y, end_x, end_y,
                               curl=curl, twist=twist, thickness=thickness, taper=0.25,
                               fill=body_color, stroke=body_color, stroke_width=1)

        # Draw exaggerated pear head (shorter and wider)
        self.canvas.pear(x, y, width=head_width, height=head_height,
                        fill=body_color, stroke=body_color, stroke_width=2)

        # Draw cartoon eyes (big but not huge)
        eye_size = size * 0.09
        eye_offset_x = size * 0.2
        eye_offset_y = size * 0.2

        # Left eye (larger whites)
        self.canvas.circle(x - eye_offset_x, y + eye_offset_y, eye_size,
                          fill=eye_color, stroke=Color.BLACK, stroke_width=2)
        self.canvas.circle(x - eye_offset_x + eye_size * 0.3, y + eye_offset_y - eye_size * 0.1,
                          eye_size * 0.5, fill=Color.BLACK, stroke=Color.BLACK)

        # Right eye
        self.canvas.circle(x + eye_offset_x, y + eye_offset_y, eye_size,
                          fill=eye_color, stroke=Color.BLACK, stroke_width=2)
        self.canvas.circle(x + eye_offset_x + eye_size * 0.3, y + eye_offset_y - eye_size * 0.1,
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
