from sketchpy import Canvas, CreativeGardenPalette


def main():
    # Grow a garden using while loops - add flowers until canvas is full

    can = Canvas(800, 600)

    # Draw a coordinate grid to help with positioning
    can.grid(spacing=50, show_coords=True)

    # Draw ground
    can.rect(0, 400, 800, 200, fill=CreativeGardenPalette.MINT_CREAM)

    # Draw flowers from left to right until we run out of room
    x = 80  # Initialize: starting position
    flower_spacing = 120

    # Keep adding flowers while there's room (leave 50px margin on right)
    while x < 750:  # Check: is there still room?
        y = 450

        # Draw 4 petals with symmetric layering
        can.circle(x, y - 28, 22, fill=CreativeGardenPalette.ROSE_QUARTZ,
                   stroke='#000', stroke_width=1.5)
        can.circle(x, y + 28, 22, fill=CreativeGardenPalette.ROSE_QUARTZ,
                   stroke='#000', stroke_width=1.5)

        can.circle(x + 28, y, 22, fill=CreativeGardenPalette.ROSE_QUARTZ,
                   stroke='#000', stroke_width=1.5)
        can.circle(x - 28, y, 22, fill=CreativeGardenPalette.ROSE_QUARTZ,
                   stroke='#000', stroke_width=1.5)

        # Draw flower center (LAST - top layer)
        can.circle(x, y, 14, fill=CreativeGardenPalette.BUTTER_YELLOW,
                   stroke='#000', stroke_width=2)

        # Update: move to next position (CRITICAL - prevents infinite loop!)
        x = x + flower_spacing

    # Your turn! Try changing flower_spacing or adding a row limit!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-09.svg')
