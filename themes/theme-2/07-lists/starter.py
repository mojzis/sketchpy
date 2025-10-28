from sketchpy.shapes import Canvas, CreativeGardenPalette


def main():
    # Create a diverse flower garden using lists

    can = Canvas(800, 600)

    # Draw a coordinate grid to help with positioning
    can.grid(spacing=50, show_coords=True)

    # Lists to store different properties for each flower
    flower_names = ["Rose", "Tulip", "Daisy", "Lily", "Violet"]

    petal_colors = [
        CreativeGardenPalette.ROSE_QUARTZ,
        CreativeGardenPalette.LILAC_DREAM,
        CreativeGardenPalette.PEACH_WHISPER,
        CreativeGardenPalette.CORAL_BLUSH,
        CreativeGardenPalette.MISTY_MAUVE
    ]

    # Draw flowers using data from the lists
    # len() returns the number of items in the list
    for i in range(len(flower_names)):
        x = 100 + i * 140
        y = 350

        # Get the color and name for this flower from the lists
        petal_color = petal_colors[i]
        name = flower_names[i]

        # Draw flower center
        can.circle(x, y, 20, fill=CreativeGardenPalette.BUTTER_YELLOW,
                   stroke='#000', stroke_width=2)

        # Draw 4 petals with the color from our list
        can.circle(x, y - 28, 22, fill=petal_color,
                   stroke='#000', stroke_width=1.5)
        can.circle(x + 28, y, 22, fill=petal_color,
                   stroke='#000', stroke_width=1.5)
        can.circle(x, y + 28, 22, fill=petal_color,
                   stroke='#000', stroke_width=1.5)
        can.circle(x - 28, y, 22, fill=petal_color,
                   stroke='#000', stroke_width=1.5)

        # Label with the flower name from our list
        can.text(x, y + 60, name, 18, fill='#000')

    # Your turn! Try adding more flowers to the lists, or create a sizes list!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-07.svg')
