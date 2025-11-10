from sketchpy import Canvas, CreativeGardenPalette


def main():
    # Draw a garden with multiple flowers using a for loop

    can = Canvas(800, 600)

    # Draw a coordinate grid to help with positioning
    can.grid(spacing=50, show_coords=True)

    # Draw 5 flowers in a row using a loop
    # The loop variable 'i' will be 0, 1, 2, 3, 4
    for i in range(5):
        x = 100 + i * 150  # Calculate position: each flower is 150 pixels apart
        y = 300            # All flowers at the same height

        # Draw a stem down to the bottom (FIRST - bottom layer)
        can.line(x, y + 25, x, 500, stroke=CreativeGardenPalette.MINT_CREAM,
                 stroke_width=6)

        # Draw 4 petals with symmetric layering (SECOND - middle layer)
        can.circle(x, y - 35, 30, fill=CreativeGardenPalette.ROSE_QUARTZ,
                   stroke='#000', stroke_width=2)  # Top petal
        can.circle(x, y + 35, 30, fill=CreativeGardenPalette.ROSE_QUARTZ,
                   stroke='#000', stroke_width=2)  # Bottom petal

        can.circle(x + 35, y, 30, fill=CreativeGardenPalette.ROSE_QUARTZ,
                   stroke='#000', stroke_width=2)  # Right petal
        can.circle(x - 35, y, 30, fill=CreativeGardenPalette.ROSE_QUARTZ,
                   stroke='#000', stroke_width=2)  # Left petal

        # Draw the flower center (yellow circle) (LAST - top layer)
        can.circle(x, y, 18, fill=CreativeGardenPalette.BUTTER_YELLOW,
                   stroke='#000', stroke_width=2)

    # Your turn! Try changing the number of flowers, spacing, or colors!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-02.svg')
