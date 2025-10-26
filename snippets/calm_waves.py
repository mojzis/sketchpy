# Calm Waves - Soothing ocean pattern
from sketchpy.shapes import Canvas, CalmOasisPalette
import math

can = Canvas(400, 400)

# Background - gradient sky
can.rect(0, 0, 400, 400, fill=CalmOasisPalette.CLOUD_WHITE, stroke="none")

# Create wave layers with overlapping circles
wave_colors = [
    CalmOasisPalette.POWDER_BLUE,
    CalmOasisPalette.SOFT_AQUA,
    CalmOasisPalette.SKY_BLUE,
    CalmOasisPalette.SEAFOAM,
    CalmOasisPalette.MINT_FRESH
]

for layer, color in enumerate(wave_colors):
    y_base = 80 + layer * 50
    amplitude = 15
    frequency = 0.05

    # Create wave with overlapping circles
    for x in range(0, 400, 10):
        y = y_base + amplitude * math.sin(frequency * x + layer * 0.5)
        can.circle(x, y, 18, fill=color, stroke="none")

# Add some decorative circles (bubbles/sea foam)
bubble_positions = [
    (80, 120), (320, 160), (150, 200), (280, 240),
    (100, 280), (350, 300), (200, 340)
]

for x, y in bubble_positions:
    can.circle(x, y, 12, fill=CalmOasisPalette.PERIWINKLE, stroke="none")
    can.circle(x, y, 8, fill=CalmOasisPalette.CREAM, stroke="none")

can
