from sketchpy import Canvas, CreativeGardenPalette


def main():
    # Create a perfectly spaced flower garden using for loops

    can = Canvas(800, 600)

    # Draw a coordinate grid to help with positioning
    can.grid(spacing=50, show_coords=True)

    # Draw the ground
    can.rect(0, 400, 800, 200, fill=CreativeGardenPalette.MINT_CREAM)

    # Draw 6 flowers in a row with perfect spacing
    for i in range(6):
        # Position formula: start + index * spacing
        x = 80 + i * 120  # Start at 80, each flower 120 pixels apart
        y = 450           # Ground level for all flowers

        # Draw stem from ground up to flower (FIRST - bottom layer)
        can.line(x, y, x, y - 80, stroke=CreativeGardenPalette.MINT_CREAM,
                 stroke_width=6)

        # Draw 4 petals with symmetric layering (SECOND - middle layer)
        can.circle(x, y - 110, 25, fill=CreativeGardenPalette.ROSE_QUARTZ,
                   stroke='#000', stroke_width=2)  # Top
        can.circle(x, y - 50, 25, fill=CreativeGardenPalette.ROSE_QUARTZ,
                   stroke='#000', stroke_width=2)  # Bottom

        can.circle(x + 30, y - 80, 25, fill=CreativeGardenPalette.ROSE_QUARTZ,
                   stroke='#000', stroke_width=2)  # Right
        can.circle(x - 30, y - 80, 25, fill=CreativeGardenPalette.ROSE_QUARTZ,
                   stroke='#000', stroke_width=2)  # Left

        # Draw flower center (LAST - top layer)
        can.circle(x, y - 80, 22, fill=CreativeGardenPalette.BUTTER_YELLOW,
                   stroke='#000', stroke_width=2)

    # Your turn! Try changing the spacing, number of flowers, or add more rows!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-06.svg')
