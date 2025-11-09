"""
Simple Shapes Example - Perfect for beginners!

This example shows the basics of sketchpy:
- Creating a canvas
- Drawing basic shapes (circles, rectangles, lines, text)
- Using colors
- Saving to a file

Run with: python examples/simple_shapes.py
"""

from sketchpy import Canvas, Color

# Create a canvas (800 pixels wide, 600 pixels tall)
can = Canvas(800, 600, background=Color.WHITE)

# Draw some circles
can.circle(150, 150, 60, fill=Color.RED)
can.circle(400, 150, 60, fill=Color.BLUE)
can.circle(650, 150, 60, fill=Color.GREEN)

# Draw rectangles
can.rect(100, 300, 100, 80, fill=Color.ORANGE)
can.rounded_rect(350, 300, 100, 80, rx=10, fill=Color.PURPLE)

# Draw a line
can.line(100, 500, 700, 500, stroke=Color.BLACK, stroke_width=3)

# Draw some text
can.text(250, 50, "Welcome to sketchpy!", size=32, fill=Color.BLACK)
can.text(100, 450, "Basic shapes are easy!", size=20, fill=Color.GRAY)

# Optional: Show a coordinate grid to help visualize positions
# Uncomment the line below to see the grid
# can.grid(spacing=50, show_coords=True)

# Save to a file
can.save("debug_out/simple_shapes.svg")
print("✓ Created debug_out/simple_shapes.svg")
print("\nTip: Open the SVG file in a web browser to see your drawing!")
