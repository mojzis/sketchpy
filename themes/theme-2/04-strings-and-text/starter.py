from sketchpy.shapes import Canvas, CreativeGardenPalette


def main():
    # Create a labeled flower garden using strings and text

    can = Canvas(800, 600)

    # Draw a coordinate grid to help with positioning
    can.grid(spacing=50, show_coords=True)

    # Add a title to our garden
    can.text(400, 50, "My Flower Garden", 32, fill='#333')

    # List of flower names to label each flower
    flower_names = ["Rose", "Tulip", "Daisy", "Lily", "Violet"]

    # Draw and label 5 flowers in a row
    for i in range(5):
        x = 100 + i * 140
        y = 300

        # Draw 4 petals with symmetric layering (FIRST - middle layer)
        can.circle(x, y - 28, 22, fill=CreativeGardenPalette.LILAC_DREAM,
                   stroke='#000', stroke_width=1.5)
        can.circle(x, y + 28, 22, fill=CreativeGardenPalette.LILAC_DREAM,
                   stroke='#000', stroke_width=1.5)

        can.circle(x + 28, y, 22, fill=CreativeGardenPalette.LILAC_DREAM,
                   stroke='#000', stroke_width=1.5)
        can.circle(x - 28, y, 22, fill=CreativeGardenPalette.LILAC_DREAM,
                   stroke='#000', stroke_width=1.5)

        # Draw flower center (LAST - top layer)
        can.circle(x, y, 14, fill=CreativeGardenPalette.LEMON_CHIFFON,
                   stroke='#000', stroke_width=2)

        # Use an f-string to create a numbered label
        # i+1 because humans count from 1, not 0
        label = f"{i+1}. {flower_names[i]}"
        can.text(x, y + 60, label, 18, fill='#000')

    # Your turn! Try changing the flower names or adding more information!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-04.svg')
