from sketchpy import Canvas, MathDoodlingPalette


def main():
    # Create canvas with subtle paper-white background
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    # First circle (left side, blue)
    can.circle(350, 300, 100,
               fill=MathDoodlingPalette.MIST_BLUE,
               opacity=0.3,
               stroke='none')

    # Second circle (right side, rose) - overlaps the first!
    can.circle(450, 300, 100,
               fill=MathDoodlingPalette.MIST_ROSE,
               opacity=0.3,
               stroke='none')

    # Look at the middle - see the purple blend? That's the magic!
    # Try changing the opacity or adding a third circle!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-01.svg')
