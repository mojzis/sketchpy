"""
Demonstration of convex blob shapes.
All blobs stay pleasantly rounded without weird concave indentations.
"""

from sketchpy import Canvas, OceanPalette
import random

# Different seeds for variety
can = Canvas(900, 400, background="#F0F8FF")

can.text(250, 30, "Convex Blobs - Always Pleasantly Rounded",
         size=22, fill=OceanPalette.DEEP_OCEAN)

# Row 1: Low wobble (very round)
can.text(50, 80, "wobble=0.15 (gentle)", size=14, fill="#333")
random.seed(10)
for i in range(6):
    can.blob(100 + i * 130, 140, radius=50, wobble=0.15, points=8,
             fill=OceanPalette.CORAL, stroke=OceanPalette.CORAL, stroke_width=2)

# Row 2: Medium wobble (organic)
can.text(50, 240, "wobble=0.4 (organic)", size=14, fill="#333")
random.seed(20)
for i in range(6):
    can.blob(100 + i * 130, 300, radius=50, wobble=0.4, points=10,
             fill=OceanPalette.PURPLE_CORAL, stroke=OceanPalette.PURPLE_CORAL, stroke_width=2)

# Note
can.text(180, 380, "All shapes stay convex - no weird concave dents!",
         size=12, fill=OceanPalette.DEEP_OCEAN)

can.save("debug_out/convex_blobs_demo.svg")
print("Saved convex_blobs_demo.svg")
print("\nAll blobs are convex - pleasantly rounded organic shapes!")
print("No disturbing concave indentations.")
