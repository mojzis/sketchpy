from sketchpy import Canvas, MathDoodlingPalette


def main():
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    # Draw 6 circles with fading opacity
    for i in range(6):
        # Calculate x position
        x = 150 + i * 110
        y = 300

        # Calculate opacity - gets smaller as i increases
        opacity = 0.5 - (i * 0.08)

        can.circle(x, y, 70,
                   fill=MathDoodlingPalette.MIST_ROSE,
                   opacity=opacity,
                   stroke='none')

    # Watch the circles fade from left to right!
    # Can you make them fade in the opposite direction?

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-04.svg')
