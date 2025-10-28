from sketchpy.shapes import Canvas, CreativeGardenPalette


def draw_flower(can, x, y):
    """Draw a simple flower at the specified position"""
    # Draw flower center
    can.circle(x, y, 20, fill=CreativeGardenPalette.BUTTER_YELLOW,
               stroke='#000', stroke_width=2)

    # Draw 4 petals
    can.circle(x, y - 28, 22, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)
    can.circle(x + 28, y, 22, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)
    can.circle(x, y + 28, 22, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)
    can.circle(x - 28, y, 22, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)


def draw_stem(can, x, y, height):
    """Draw a stem from y down to y + height"""
    can.line(x, y, x, y + height,
             stroke=CreativeGardenPalette.MINT_CREAM,
             stroke_width=6)


def main():
    # Use functions to organize our flower drawing code

    can = Canvas(800, 600)

    # Draw a coordinate grid to help with positioning
    can.grid(spacing=50, show_coords=True)

    # Draw ground
    can.rect(0, 400, 800, 200, fill=CreativeGardenPalette.MINT_CREAM)

    # Draw flowers with stems using our reusable functions
    # Much cleaner than copying all the circle code 6 times!
    for i in range(6):
        x = 100 + i * 120
        y = 450

        # Call our functions to draw each part
        draw_stem(can, x, y, 80)   # Stem first (back layer)
        draw_flower(can, x, y)      # Flower on top

    # Your turn! Try creating a draw_butterfly() or draw_grass() function!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-11.svg')
