"""
Complete underwater ocean scene using OceanShapes helpers.
Demonstrates how easy it is to create complex scenes with simple API calls.
"""

from sketchpy.shapes import Canvas, Color, OceanPalette, OceanShapes
import random

# Seed for reproducible randomness in shapes (changed to showcase S-curves)
random.seed(99)  # Different seed to show variety in twist values

# Create canvas with ocean gradient background
can = Canvas(800, 600, background=OceanPalette.SHALLOW_WATER)

# Create gradient from light to dark (top to bottom)
can.linear_gradient("ocean_depth",
                    start=(0, 0), end=(0, 100),
                    colors=[
                        (OceanPalette.SHALLOW_WATER, 0),
                        (OceanPalette.OCEAN_BLUE, 0.5),
                        (OceanPalette.DEEP_OCEAN, 1.0)
                    ])

# Background gradient rectangle
can.rect(0, 0, 800, 600, fill="gradient:ocean_depth", stroke="none")

# Initialize OceanShapes helper
ocean = OceanShapes(can)

# === OCEAN FLOOR (seaweed) ===
# Draw several seaweed plants across the bottom
seaweed_positions = [80, 150, 220, 580, 650, 720]
for x_pos in seaweed_positions:
    height = random.randint(120, 180)
    ocean.seaweed(x_pos, 600, height=height, sway=0.4, color=OceanPalette.KELP_GREEN)

# === JELLYFISH ===
# Float a few jellyfish in the upper water
ocean.jellyfish(150, 100, size=60, body_color=OceanPalette.TRANSLUCENT_BLUE, tentacle_count=8)
ocean.jellyfish(600, 150, size=80, body_color=OceanPalette.TRANSLUCENT_BLUE, tentacle_count=6)
ocean.jellyfish(700, 80, size=50, body_color=OceanPalette.TRANSLUCENT_BLUE, tentacle_count=7)

# === MAIN OCTOPUS (the star of the show!) ===
ocean.octopus(400, 300, size=150, body_color=OceanPalette.PURPLE_CORAL, eye_color=Color.WHITE)

# === SMALLER OCTOPUS FRIENDS ===
ocean.octopus(200, 450, size=80, body_color=OceanPalette.CORAL, eye_color=Color.WHITE)
ocean.octopus(620, 400, size=70, body_color=OceanPalette.STARFISH_ORANGE, eye_color=Color.WHITE)

# === BUBBLES (using circles) ===
bubble_positions = [
    (100, 500), (350, 450), (250, 380), (500, 520),
    (150, 300), (650, 480), (700, 350), (450, 200)
]

for bx, by in bubble_positions:
    bubble_size = random.randint(3, 8)
    can.circle(bx, by, bubble_size, fill=OceanPalette.SEAFOAM,
               stroke=Color.WHITE, stroke_width=1, opacity=0.6)

# === OCEAN WAVES ON SURFACE ===
# Draw wavy water surface at top
can.wave(0, 20, 800, 20, height=10, waves=8,
         stroke=OceanPalette.SEAFOAM, stroke_width=2)
can.wave(0, 35, 800, 35, height=8, waves=6,
         stroke=OceanPalette.SEAFOAM, stroke_width=1)

# === SANDY FLOOR ===
# Add sand at bottom using blobs
for i in range(48):
    sand_x = i * 20 + random.randint(-3, 3)
    can.blob(sand_x, 590, radius=12, wobble=0.3, points=8,
            fill=OceanPalette.SAND, stroke=OceanPalette.SAND)

# Title
# can.text(250, 580, "Underwater Friends", size=20, fill=OceanPalette.SHELL_WHITE)

# Save output
can.save("debug_out/ocean_scene_output.svg")
