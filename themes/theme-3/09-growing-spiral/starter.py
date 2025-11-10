import math
from sketchpy import Canvas, MathDoodlingPalette


def main():
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    center_x, center_y = 400, 300

    # Starting values
    radius = 0
    angle = 0

    # Keep spiraling until we get too far from center
    while radius < 250:
        # Calculate position
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)

        can.circle(x, y, 25,
                   fill=MathDoodlingPalette.MIST_MINT,
                   opacity=0.3,
                   stroke='none')

        # Grow outward and rotate
        radius = radius + 12
        angle = angle + 0.6

    # A beautiful spiral! Try changing the growth rate!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-09.svg')
