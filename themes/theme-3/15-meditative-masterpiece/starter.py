import math
from sketchpy import Canvas, MathDoodlingPalette


def main():
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    # Define helper functions
    def draw_mandala(canvas, cx, cy, num_circles=8, orbit_radius=100,
                     circle_size=60, color=MathDoodlingPalette.MIST_BLUE,
                     opacity=0.25):
        """Draw a customizable mandala"""
        for i in range(num_circles):
            angle = (i / num_circles) * 2 * math.pi
            x = cx + orbit_radius * math.cos(angle)
            y = cy + orbit_radius * math.sin(angle)
            canvas.circle(x, y, circle_size, fill=color,
                          opacity=opacity, stroke='none')

    def draw_concentric_rings(canvas, cx, cy, num_rings=10, start_radius=200,
                              color=MathDoodlingPalette.MIST_ROSE, opacity=0.15):
        """Draw concentric rings with drift"""
        for i in range(num_rings):
            offset_x = i * 4
            offset_y = i * 3
            radius = start_radius - (i * 18)
            canvas.circle(cx + offset_x, cy + offset_y, radius,
                          fill=color, opacity=opacity, stroke='none')

    def draw_spiral(canvas, cx, cy, max_radius=180,
                    color=MathDoodlingPalette.MIST_MINT, opacity=0.25):
        """Draw a growing spiral"""
        radius = 0
        angle = 0
        while radius < max_radius:
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            canvas.circle(x, y, 20, fill=color, opacity=opacity, stroke='none')
            radius += 10
            angle += 0.5

    # Example masterpiece - now create your own!

    # Layer 1: Background concentric rings
    draw_concentric_rings(can, 400, 300, num_rings=15,
                          start_radius=280,
                          color=MathDoodlingPalette.MIST_BLUE,
                          opacity=0.12)

    # Layer 2: Central mandala
    draw_mandala(can, 400, 300,
                 num_circles=16,
                 orbit_radius=150,
                 circle_size=80,
                 color=MathDoodlingPalette.MIST_ROSE,
                 opacity=0.2)

    # Layer 3: Smaller accent mandalas
    for i in range(6):
        angle = (i / 6) * 2 * math.pi
        x = 400 + 200 * math.cos(angle)
        y = 300 + 200 * math.sin(angle)
        draw_mandala(can, x, y,
                     num_circles=6,
                     orbit_radius=40,
                     circle_size=25,
                     color=MathDoodlingPalette.MIST_MINT,
                     opacity=0.3)

    # Now it's YOUR turn!
    # Delete this code and create something unique!
    # Combine patterns, experiment with colors, make it YOURS!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-15.svg')
