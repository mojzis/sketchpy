import math
from sketchpy.shapes import Canvas, MathDoodlingPalette


def main():
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    # Define our fully customizable function
    def draw_mandala(canvas, cx, cy, num_circles=8, orbit_radius=100,
                     circle_size=60, color=MathDoodlingPalette.MIST_BLUE,
                     opacity=0.25):
        """Draw a fully customizable mandala"""
        for i in range(num_circles):
            angle = (i / num_circles) * 2 * math.pi
            x = cx + orbit_radius * math.cos(angle)
            y = cy + orbit_radius * math.sin(angle)

            canvas.circle(x, y, circle_size,
                          fill=color,
                          opacity=opacity,
                          stroke='none')

    # Large blue mandala with many circles
    draw_mandala(can, 250, 250,
                 num_circles=12,
                 orbit_radius=120,
                 circle_size=70,
                 color=MathDoodlingPalette.MIST_BLUE,
                 opacity=0.2)

    # Small dense rose mandala
    draw_mandala(can, 550, 250,
                 num_circles=16,
                 orbit_radius=80,
                 circle_size=40,
                 color=MathDoodlingPalette.MIST_ROSE,
                 opacity=0.3)

    # Medium mint mandala
    draw_mandala(can, 400, 450,
                 num_circles=6,
                 orbit_radius=100,
                 circle_size=80,
                 color=MathDoodlingPalette.MIST_MINT,
                 opacity=0.25)

    # Three totally different mandalas from one function!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-12.svg')
