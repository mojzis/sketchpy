"""
Math Doodling Demo - Example patterns using the new MathDoodlingPalette

Run with: uv run python examples/math_doodling_demo.py
"""

import math
from sketchpy import Canvas, MathDoodlingPalette

# Example 1: Simple Overlap (Lesson 1 style)
def simple_overlap():
    """Two overlapping circles showing color mixing."""
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    # First circle
    can.circle(350, 300, 100,
               fill=MathDoodlingPalette.MIST_BLUE,
               opacity=0.3,
               stroke='none')

    # Second circle overlaps
    can.circle(450, 300, 100,
               fill=MathDoodlingPalette.MIST_ROSE,
               opacity=0.3,
               stroke='none')

    return can


# Example 2: Triadic Triangle
def triadic_triangle():
    """Three circles creating a central blend."""
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    # Top circle (blue)
    can.circle(400, 250, 120,
               fill=MathDoodlingPalette.MIST_BLUE,
               opacity=0.25,
               stroke='none')

    # Bottom left (rose)
    can.circle(320, 380, 120,
               fill=MathDoodlingPalette.MIST_ROSE,
               opacity=0.25,
               stroke='none')

    # Bottom right (mint)
    can.circle(480, 380, 120,
               fill=MathDoodlingPalette.MIST_MINT,
               opacity=0.25,
               stroke='none')

    return can


# Example 3: Simple Spirograph
def simple_spirograph():
    """8 circles arranged around a center point."""
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    center_x, center_y = 400, 300
    num_circles = 8
    orbit_radius = 140
    circle_size = 90

    for i in range(num_circles):
        angle = (i / num_circles) * 2 * math.pi
        x = center_x + orbit_radius * math.cos(angle)
        y = center_y + orbit_radius * math.sin(angle)

        can.circle(x, y, circle_size,
                   fill=MathDoodlingPalette.MIST_BLUE,
                   opacity=0.25,
                   stroke='none')

    return can


# Example 4: Concentric Drift
def concentric_drift():
    """Nested circles with gradual offset."""
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    num_rings = 12
    start_radius = 260

    for i in range(num_rings):
        # Drift offset increases with each ring
        offset_x = i * 7
        offset_y = i * 5

        radius = start_radius - (i * 20)

        can.circle(400 + offset_x, 300 + offset_y, radius,
                   fill=MathDoodlingPalette.MIST_ROSE,
                   opacity=0.2,
                   stroke='none')

    return can


# Example 5: Multi-Color Mandala
def multi_color_mandala():
    """Spirograph with alternating colors."""
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    center_x, center_y = 400, 300
    num_circles = 12
    orbit_radius = 150
    circle_size = 80

    colors = [
        MathDoodlingPalette.MIST_BLUE,
        MathDoodlingPalette.MIST_ROSE,
        MathDoodlingPalette.MIST_MINT
    ]

    for i in range(num_circles):
        angle = (i / num_circles) * 2 * math.pi
        x = center_x + orbit_radius * math.cos(angle)
        y = center_y + orbit_radius * math.sin(angle)

        # Cycle through colors
        color = colors[i % 3]

        can.circle(x, y, circle_size,
                   fill=color,
                   opacity=0.25,
                   stroke='none')

    return can


# Example 6: Vesica Piscis Grid
def vesica_grid():
    """Grid of overlapping pairs."""
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    for row in range(3):
        for col in range(4):
            x = 120 + col * 160
            y = 130 + row * 160

            # Left circle
            can.circle(x, y, 70,
                       fill=MathDoodlingPalette.MIST_BLUE,
                       opacity=0.3,
                       stroke='none')

            # Right circle (overlaps by half)
            can.circle(x + 70, y, 70,
                       fill=MathDoodlingPalette.MIST_MINT,
                       opacity=0.3,
                       stroke='none')

    return can


if __name__ == "__main__":
    # Generate and save all examples
    examples = {
        "01_simple_overlap": simple_overlap(),
        "02_triadic_triangle": triadic_triangle(),
        "03_simple_spirograph": simple_spirograph(),
        "04_concentric_drift": concentric_drift(),
        "05_multi_color_mandala": multi_color_mandala(),
        "06_vesica_grid": vesica_grid()
    }

    for name, canvas in examples.items():
        filename = f"debug_out/math_doodling_{name}.svg"
        canvas.save(filename)
        print(f"✓ Created {filename}")

    print(f"\n✓ Generated {len(examples)} Math Doodling examples!")
