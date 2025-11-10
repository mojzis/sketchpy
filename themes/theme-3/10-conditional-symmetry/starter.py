import math
from sketchpy import Canvas, MathDoodlingPalette


def main():
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    center_x, center_y = 400, 300
    num_circles = 12
    orbit_radius = 150

    for i in range(num_circles):
        angle = (i / num_circles) * 2 * math.pi
        x = center_x + orbit_radius * math.cos(angle)
        y = center_y + orbit_radius * math.sin(angle)

        # Use conditional logic to vary the pattern
        if i % 2 == 0:  # Even positions
            color = MathDoodlingPalette.MIST_BLUE
            size = 80
        else:  # Odd positions
            color = MathDoodlingPalette.MIST_ROSE
            size = 70

        can.circle(x, y, size,
                   fill=color,
                   opacity=0.25,
                   stroke='none')

    # See the alternating pattern? Try adding more conditions!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-10.svg')
