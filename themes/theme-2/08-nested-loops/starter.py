from sketchpy import Canvas, CreativeGardenPalette


def main():
    # Create a full flower field using nested loops

    can = Canvas(800, 600)

    # Draw a coordinate grid to help with positioning
    can.grid(spacing=50, show_coords=True)

    # Draw sky and ground background
    can.rect(0, 0, 800, 300, fill=CreativeGardenPalette.SKY_BREEZE)
    can.rect(0, 300, 800, 300, fill=CreativeGardenPalette.MINT_CREAM)

    # Draw a 4×5 grid of flowers (4 rows, 5 columns)
    # Outer loop controls rows (vertical position)
    # Inner loop controls columns (horizontal position)
    for row in range(4):
        for col in range(5):
            # Calculate position based on row and column
            x = 100 + col * 130  # Columns control x (horizontal)
            y = 350 + row * 80   # Rows control y (vertical)

            # Use checkerboard pattern for petal colors
            # (row + col) % 2 alternates between 0 and 1
            if (row + col) % 2 == 0:
                petal_color = CreativeGardenPalette.LILAC_DREAM
            else:
                petal_color = CreativeGardenPalette.PEACH_WHISPER

            # Draw 4 petals with symmetric layering and alternating colors
            can.circle(x, y - 25, 20, fill=petal_color,
                       stroke='#000', stroke_width=1.5)
            can.circle(x, y + 25, 20, fill=petal_color,
                       stroke='#000', stroke_width=1.5)

            can.circle(x + 25, y, 20, fill=petal_color,
                       stroke='#000', stroke_width=1.5)
            can.circle(x - 25, y, 20, fill=petal_color,
                       stroke='#000', stroke_width=1.5)

            # Draw flower center (LAST - top layer)
            can.circle(x, y, 18, fill=CreativeGardenPalette.LEMON_CHIFFON,
                       stroke='#000', stroke_width=2)

    # Your turn! Try changing the pattern using row % 2 or col % 2!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-08.svg')
