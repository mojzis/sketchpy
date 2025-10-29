import math
from sketchpy.shapes import Canvas, MathDoodlingPalette


def main():
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    # Define position calculator function
    def circle_position(center_x, center_y, radius, angle):
        """Calculate x, y position on a circle - returns position"""
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        return x, y

    # Define drawing function
    def draw_mandala(canvas, cx, cy, num_circles=6, orbit_radius=50,
                     circle_size=35, color=MathDoodlingPalette.MIST_BLUE,
                     opacity=0.25):
        """Draw a mandala at position (cx, cy)"""
        for i in range(num_circles):
            angle = (i / num_circles) * 2 * math.pi
            x = cx + orbit_radius * math.cos(angle)
            y = cy + orbit_radius * math.sin(angle)

            canvas.circle(x, y, circle_size,
                          fill=color,
                          opacity=opacity,
                          stroke='none')

    # Use circle_position to arrange mandalas in a circle!
    center_x, center_y = 400, 300
    layout_radius = 180
    num_mandalas = 6

    for i in range(num_mandalas):
        # Calculate where this mandala should go
        angle = (i / num_mandalas) * 2 * math.pi
        x, y = circle_position(center_x, center_y, layout_radius, angle)

        # Draw mandala at the calculated position
        draw_mandala(can, x, y,
                     num_circles=6,
                     orbit_radius=40,
                     circle_size=25,
                     color=MathDoodlingPalette.MIST_ROSE,
                     opacity=0.3)

    # A mandala made of mandalas!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-13.svg')
