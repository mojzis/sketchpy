import math
from sketchpy.shapes import Canvas, MathDoodlingPalette


def main():
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    # Define our reusable function
    def draw_mandala(canvas, cx, cy):
        """Draw a mandala at position (cx, cy)"""
        num_circles = 8
        orbit_radius = 80
        circle_size = 50

        for i in range(num_circles):
            angle = (i / num_circles) * 2 * math.pi
            x = cx + orbit_radius * math.cos(angle)
            y = cy + orbit_radius * math.sin(angle)

            canvas.circle(x, y, circle_size,
                          fill=MathDoodlingPalette.MIST_BLUE,
                          opacity=0.25,
                          stroke='none')

    # Draw three mandalas using our function!
    draw_mandala(can, 200, 200)  # Top-left
    draw_mandala(can, 600, 200)  # Top-right
    draw_mandala(can, 400, 450)  # Bottom-center

    # That's way cleaner than writing the same code 3 times!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-11.svg')
