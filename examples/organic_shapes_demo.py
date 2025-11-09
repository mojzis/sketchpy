"""
Demonstration of enhanced organic shapes with smooth Bézier blobs and S-curve tentacles.
Shows the difference between simple curves and twisted S-curves.
"""

from sketchpy import Canvas, Color, OceanPalette
import random

# Seed for reproducibility
random.seed(123)

# Create canvas
can = Canvas(900, 700, background=OceanPalette.SHALLOW_WATER)

# Title
can.text(280, 30, "Enhanced Organic Shapes", size=24, fill=OceanPalette.DEEP_OCEAN)

# === SMOOTH BLOBS ===
can.text(50, 80, "Smooth Bézier Blobs", size=18, fill=Color.BLACK)

# Show progression of wobble
wobble_values = [0.1, 0.25, 0.4, 0.6]
for i, wobble in enumerate(wobble_values):
    x = 100 + i * 150
    can.blob(x, 150, radius=50, wobble=wobble, points=10,
             fill=OceanPalette.CORAL, stroke=OceanPalette.CORAL, stroke_width=2)
    can.text(x - 35, 220, f"wobble={wobble}", size=11, fill=Color.BLACK)

# === S-CURVE TENTACLES ===
can.text(50, 280, "S-Curve Tentacles (twist parameter)", size=18, fill=Color.BLACK)

# Row 1: No twist (simple curves)
can.text(50, 320, "twist=0 (simple)", size=12, fill=Color.GRAY)
can.tentacle(120, 340, 120, 480, curl=0.3, twist=0, thickness=25, taper=0.3,
            fill=OceanPalette.PURPLE_CORAL)
can.tentacle(220, 340, 220, 480, curl=0.5, twist=0, thickness=25, taper=0.3,
            fill=OceanPalette.PURPLE_CORAL)
can.tentacle(320, 340, 320, 480, curl=0.7, twist=0, thickness=25, taper=0.3,
            fill=OceanPalette.PURPLE_CORAL)

# Row 2: Light twist (gentle S)
can.text(430, 320, "twist=0.3 (gentle S)", size=12, fill=Color.GRAY)
can.tentacle(500, 340, 500, 480, curl=0.3, twist=0.3, thickness=25, taper=0.3,
            fill=OceanPalette.STARFISH_ORANGE)
can.tentacle(600, 340, 600, 480, curl=0.5, twist=0.3, thickness=25, taper=0.3,
            fill=OceanPalette.STARFISH_ORANGE)
can.tentacle(700, 340, 700, 480, curl=0.7, twist=0.3, thickness=25, taper=0.3,
            fill=OceanPalette.STARFISH_ORANGE)

# Row 3: Strong twist (pronounced S)
can.text(50, 510, "twist=0.7 (strong S)", size=12, fill=Color.GRAY)
can.tentacle(120, 530, 120, 670, curl=0.3, twist=0.7, thickness=25, taper=0.3,
            fill=OceanPalette.SEA_GREEN)
can.tentacle(220, 530, 220, 670, curl=0.5, twist=0.7, thickness=25, taper=0.3,
            fill=OceanPalette.SEA_GREEN)
can.tentacle(320, 530, 320, 670, curl=0.7, twist=0.7, thickness=25, taper=0.3,
            fill=OceanPalette.SEA_GREEN)

# Row 4: Maximum twist (very organic)
can.text(430, 510, "twist=1.0 (maximum)", size=12, fill=Color.GRAY)
can.tentacle(500, 530, 500, 670, curl=0.3, twist=1.0, thickness=25, taper=0.3,
            fill=OceanPalette.KELP_GREEN)
can.tentacle(600, 530, 600, 670, curl=0.5, twist=1.0, thickness=25, taper=0.3,
            fill=OceanPalette.KELP_GREEN)
can.tentacle(700, 530, 700, 670, curl=0.7, twist=1.0, thickness=25, taper=0.3,
            fill=OceanPalette.KELP_GREEN)

# Note at bottom
can.text(180, 690, "S-curves create natural, flowing tentacle shapes!",
         size=14, fill=OceanPalette.DEEP_OCEAN)

# Save output
can.save("debug_out/organic_shapes_demo.svg")
print("Saved organic_shapes_demo.svg")
print("\nDemonstrates:")
print("- Smooth Bézier blob curves (no sharp corners)")
print("- S-curve tentacles with twist parameter")
print("- Natural flowing shapes perfect for octopus arms!")
