import math
from sketchpy.shapes import Canvas, MathDoodlingPalette


def main():
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    # List of colors to cycle through
    colors = [
        MathDoodlingPalette.MIST_BLUE,
        MathDoodlingPalette.MIST_ROSE,
        MathDoodlingPalette.MIST_MINT
    ]

    center_x, center_y = 400, 300
    num_circles = 12
    orbit_radius = 150
    circle_size = 80

    for i in range(num_circles):
        angle = (i / num_circles) * 2 * math.pi
        x = center_x + orbit_radius * math.cos(angle)
        y = center_y + orbit_radius * math.sin(angle)

        # Pick color using modulo - cycles through the list!
        color = colors[i % 3]

        can.circle(x, y, circle_size,
                   fill=color,
                   opacity=0.25,
                   stroke='none')

    # A rainbow mandala! See the repeating pattern?

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-07.svg')
