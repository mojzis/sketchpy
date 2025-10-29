import math
from sketchpy.shapes import Canvas, MathDoodlingPalette


def main():
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    # Center of our mandala
    center_x, center_y = 400, 300

    # How many circles?
    num_circles = 8

    # Distance from center (orbit radius)
    orbit_radius = 140

    # Size of each circle
    circle_size = 90

    # Draw circles arranged in a circle!
    for i in range(num_circles):
        # Calculate angle for this circle
        angle = (i / num_circles) * 2 * math.pi

        # Use trigonometry to find position
        x = center_x + orbit_radius * math.cos(angle)
        y = center_y + orbit_radius * math.sin(angle)

        can.circle(x, y, circle_size,
                   fill=MathDoodlingPalette.MIST_BLUE,
                   opacity=0.25,
                   stroke='none')

    # You've created a mandala! Try changing num_circles to 6 or 12!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-05.svg')
