import math
from sketchpy import Canvas, MathDoodlingPalette


def main():
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    # Define drawing function
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

    # Data-driven art: Each mandala defined as a dictionary!
    mandalas = [
        {
            'x': 200,
            'y': 200,
            'num_circles': 12,
            'orbit_radius': 80,
            'circle_size': 50,
            'color': MathDoodlingPalette.MIST_BLUE,
            'opacity': 0.2
        },
        {
            'x': 600,
            'y': 200,
            'num_circles': 6,
            'orbit_radius': 100,
            'circle_size': 70,
            'color': MathDoodlingPalette.MIST_ROSE,
            'opacity': 0.3
        },
        {
            'x': 400,
            'y': 450,
            'num_circles': 16,
            'orbit_radius': 120,
            'circle_size': 40,
            'color': MathDoodlingPalette.MIST_MINT,
            'opacity': 0.25
        }
    ]

    # Draw all mandalas from the data!
    for config in mandalas:
        draw_mandala(
            can,
            config['x'],
            config['y'],
            num_circles=config['num_circles'],
            orbit_radius=config['orbit_radius'],
            circle_size=config['circle_size'],
            color=config['color'],
            opacity=config['opacity']
        )

    # Want to add another? Just add a dictionary to the list!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-14.svg')
