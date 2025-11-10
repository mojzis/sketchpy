from sketchpy import Canvas, MathDoodlingPalette


def main():
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    # Draw 5 circles in a row using a loop
    for i in range(5):
        # Calculate x position - each circle is 100 pixels apart
        x = 200 + i * 100
        y = 300  # Keep y constant for a horizontal row

        can.circle(x, y, 60,
                   fill=MathDoodlingPalette.MIST_BLUE,
                   opacity=0.25,
                   stroke='none')

    # See how the overlaps create darker blue regions?
    # Try changing range(5) to range(10) for more circles!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-03.svg')
