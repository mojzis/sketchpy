from sketchpy.shapes import Canvas, MathDoodlingPalette


def main():
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    # Top circle (blue)
    can.circle(400, 250, 120,
               fill=MathDoodlingPalette.MIST_BLUE,
               opacity=0.25,
               stroke='none')

    # Bottom-left circle (rose)
    can.circle(320, 380, 120,
               fill=MathDoodlingPalette.MIST_ROSE,
               opacity=0.25,
               stroke='none')

    # Bottom-right circle (mint)
    can.circle(480, 380, 120,
               fill=MathDoodlingPalette.MIST_MINT,
               opacity=0.25,
               stroke='none')

    # Count the different colors - how many can you find?
    # Try adjusting the positions or sizes!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-02.svg')
