from sketchpy import Canvas, CreativeGardenPalette


def main():
    # Create a field of flowers using nested loops

    can = Canvas(800, 600)

    # Draw a coordinate grid to help with positioning
    can.grid(spacing=50, show_coords=True)

    # Draw a 3×4 grid of flowers (3 rows, 4 columns)
    # The outer loop handles rows (vertical positioning)
    # The inner loop handles columns (horizontal positioning)
    for row in range(3):
        for col in range(4):
            # Calculate position based on row and column
            x = 120 + col * 180  # Column controls horizontal position
            y = 120 + row * 180  # Row controls vertical position

            # Draw 4 petals with symmetric layering (FIRST - middle layer)
            can.circle(x, y - 30, 25, fill=CreativeGardenPalette.PEACH_WHISPER,
                       stroke='#000', stroke_width=1.5)  # Top
            can.circle(x, y + 30, 25, fill=CreativeGardenPalette.PEACH_WHISPER,
                       stroke='#000', stroke_width=1.5)  # Bottom

            can.circle(x + 30, y, 25, fill=CreativeGardenPalette.PEACH_WHISPER,
                       stroke='#000', stroke_width=1.5)  # Right
            can.circle(x - 30, y, 25, fill=CreativeGardenPalette.PEACH_WHISPER,
                       stroke='#000', stroke_width=1.5)  # Left

            # Draw flower center (LAST - top layer)
            can.circle(x, y, 14, fill=CreativeGardenPalette.LEMON_CHIFFON,
                       stroke='#000', stroke_width=2)

    # Your turn! Try changing the grid size or adding alternating colors!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-03.svg')
