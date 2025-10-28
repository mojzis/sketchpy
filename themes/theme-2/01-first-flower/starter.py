from sketchpy.shapes import Canvas, CreativeGardenPalette


def main():
    # Let's draw our first flower!

    can = Canvas(800, 600)

    # Draw a coordinate grid to help with positioning
    can.grid(spacing=50, show_coords=True)

    # Draw the flower center - a yellow circle in the middle
    can.circle(400, 300, 30, fill=CreativeGardenPalette.BUTTER_YELLOW,
               stroke='#000', stroke_width=2)

    # Draw 6 petals arranged around the center
    # Each petal is a circle positioned to surround the center
    petal_positions = [
        (400, 230),  # Top
        (450, 265),  # Top-right
        (450, 335),  # Bottom-right
        (400, 370),  # Bottom
        (350, 335),  # Bottom-left
        (350, 265)   # Top-left
    ]

    for x, y in petal_positions:
        can.circle(x, y, 40, fill=CreativeGardenPalette.ROSE_QUARTZ,
                   stroke='#000', stroke_width=2)

    # Draw a stem from the bottom of the flower downward
    can.line(400, 330, 400, 500, stroke=CreativeGardenPalette.MINT_CREAM,
             stroke_width=8)

    # Your turn! Try changing the colors, positions, or add leaves!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-01.svg')
