import math
from sketchpy.shapes import Canvas, MathDoodlingPalette


def main():
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    # Grid of 3 rows × 3 columns
    for row in range(3):
        for col in range(3):
            # Calculate center of this mandala
            center_x = 200 + col * 200
            center_y = 150 + row * 200

            # Draw a small mandala at this grid position
            num_circles = 6
            orbit_radius = 50
            circle_size = 30

            for i in range(num_circles):
                angle = (i / num_circles) * 2 * math.pi
                x = center_x + orbit_radius * math.cos(angle)
                y = center_y + orbit_radius * math.sin(angle)

                can.circle(x, y, circle_size,
                           fill=MathDoodlingPalette.MIST_BLUE,
                           opacity=0.25,
                           stroke='none')

    # 9 mandalas! That's the power of nested loops!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-08.svg')
