"""
Demonstration of organic curve primitives: wave, blob, and tentacle.
Shows how each primitive works with different parameters.
"""

from sketchpy import Canvas, Color, OceanPalette

# Create canvas
can = Canvas(800, 600, background=OceanPalette.SHALLOW_WATER)

# Title
can.text(300, 30, "Ocean Curve Primitives", size=24, fill=OceanPalette.DEEP_OCEAN)

# === WAVE EXAMPLES ===
can.text(50, 80, "wave() - Wavy lines", size=16, fill=Color.BLACK)

# Gentle wave
can.wave(50, 100, 350, 100, height=15, waves=2,
         stroke=OceanPalette.OCEAN_BLUE, stroke_width=3)
can.text(360, 105, "height=15, waves=2", size=10, fill=Color.GRAY)

# Choppy water
can.wave(50, 150, 350, 150, height=8, waves=6,
         stroke=OceanPalette.SEAFOAM, stroke_width=2)
can.text(360, 155, "height=8, waves=6", size=10, fill=Color.GRAY)

# Diagonal wave
can.wave(50, 180, 300, 220, height=20, waves=3,
         stroke=OceanPalette.SEA_GREEN, stroke_width=3)
can.text(310, 210, "diagonal", size=10, fill=Color.GRAY)

# === BLOB EXAMPLES ===
can.text(50, 280, "blob() - Organic shapes", size=16, fill=Color.BLACK)

# Smooth blob
can.blob(100, 340, radius=40, wobble=0.1, points=12,
         fill=OceanPalette.CORAL, stroke=OceanPalette.CORAL)
can.text(70, 400, "wobble=0.1", size=10, fill=Color.GRAY)

# Medium bumpy
can.blob(200, 340, radius=40, wobble=0.3, points=8,
         fill=OceanPalette.PURPLE_CORAL, stroke=OceanPalette.PURPLE_CORAL)
can.text(170, 400, "wobble=0.3", size=10, fill=Color.GRAY)

# Very bumpy
can.blob(300, 340, radius=40, wobble=0.5, points=6,
         fill=OceanPalette.STARFISH_ORANGE, stroke=OceanPalette.STARFISH_ORANGE)
can.text(270, 400, "wobble=0.5", size=10, fill=Color.GRAY)

# === TENTACLE EXAMPLES ===
can.text(450, 80, "tentacle() - Tapered curves", size=16, fill=Color.BLACK)

# Straight tentacle
can.tentacle(480, 120, 480, 220, curl=0, thickness=20, taper=0.3,
            fill=OceanPalette.PURPLE_CORAL, stroke=OceanPalette.PURPLE_CORAL)
can.text(450, 235, "curl=0", size=10, fill=Color.GRAY)

# Right curl
can.tentacle(560, 120, 560, 220, curl=0.5, thickness=20, taper=0.3,
            fill=OceanPalette.CORAL, stroke=OceanPalette.CORAL)
can.text(535, 235, "curl=0.5", size=10, fill=Color.GRAY)

# Left curl
can.tentacle(640, 120, 640, 220, curl=-0.5, thickness=20, taper=0.3,
            fill=OceanPalette.STARFISH_ORANGE, stroke=OceanPalette.STARFISH_ORANGE)
can.text(610, 235, "curl=-0.5", size=10, fill=Color.GRAY)

# Strong taper vs. no taper
can.tentacle(520, 280, 520, 380, curl=0.3, thickness=25, taper=0.1,
            fill=OceanPalette.SEA_GREEN, stroke=OceanPalette.SEA_GREEN)
can.text(480, 395, "taper=0.1 (pointy)", size=10, fill=Color.GRAY)

can.tentacle(650, 280, 650, 380, curl=0.3, thickness=25, taper=0.8,
            fill=OceanPalette.KELP_GREEN, stroke=OceanPalette.KELP_GREEN)
can.text(610, 395, "taper=0.8 (thick)", size=10, fill=Color.GRAY)

# Bottom note
can.text(200, 580, "These primitives power the OceanShapes helpers!",
         size=14, fill=OceanPalette.DEEP_OCEAN)

# Save output
can.save("debug_out/ocean_primitives_output.svg")
