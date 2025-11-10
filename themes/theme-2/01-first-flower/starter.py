from sketchpy import Canvas, CreativeGardenPalette


def main():
    # Let's draw our first flower!

    can = Canvas(800, 600)

    # Draw a coordinate grid to help with positioning
    can.grid(spacing=50, show_coords=True)

    # Draw a stem from the bottom of the flower downward (FIRST - bottom layer)
    can.line(400, 330, 400, 500, stroke=CreativeGardenPalette.MINT_CREAM,
             stroke_width=8)

    # Draw 6 petals around the center (SECOND - middle layer)
    can.circle(400, 240, 40, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=2)  # Top petal
    can.circle(400, 360, 40, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=2)  # Bottom petal

    can.circle(450, 265, 40, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=2)  # Top-right petal
    can.circle(350, 265, 40, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=2)  # Top-left petal

    can.circle(450, 335, 40, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=2)  # Bottom-right petal
    can.circle(350, 335, 40, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=2)  # Bottom-left petal

    # Draw the flower center - a yellow circle in the middle (LAST - front/top layer)
    can.circle(400, 300, 30, fill=CreativeGardenPalette.BUTTER_YELLOW,
               stroke='#000', stroke_width=2)

    # Your turn! Try changing the colors, positions, or add leaves!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-01.svg')
