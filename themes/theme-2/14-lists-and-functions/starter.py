from sketchpy.shapes import Canvas, CreativeGardenPalette


def main():
    # Data-driven programming: define the garden as data!

    can = Canvas(800, 600)

    def draw_flower_from_data(can, flower_data):
        """Draw a flower based on dictionary data

        The dictionary contains all the information needed to draw the flower.
        This separates data from code - we can change the garden by changing
        the data without touching the drawing code!
        """
        # Extract all the flower properties from the dictionary
        x = flower_data["x"]
        y = flower_data["y"]
        size = flower_data["size"]
        petal_color = flower_data["petal_color"]
        center_color = flower_data["center_color"]

        # Calculate dimensions
        center_size = int(size * 0.7)
        petal_distance = int(size * 1.4)

        # Create radial gradients for depth
        can.radial_gradient("petal_grad", center=(50, 50), radius=60,
                            colors=['#FFFFFF', petal_color])
        can.radial_gradient("center_grad", center=(50, 50), radius=60,
                            colors=[center_color, '#F4E08A'])

        # Draw 4 petals with symmetric layering
        can.circle(x, y - petal_distance, size, fill='gradient:petal_grad',
                   stroke='#000', stroke_width=1.5)
        can.circle(x, y + petal_distance, size, fill='gradient:petal_grad',
                   stroke='#000', stroke_width=1.5)

        can.circle(x + petal_distance, y, size, fill='gradient:petal_grad',
                   stroke='#000', stroke_width=1.5)
        can.circle(x - petal_distance, y, size, fill='gradient:petal_grad',
                   stroke='#000', stroke_width=1.5)

        # Draw the flower center (LAST - top layer)
        can.circle(x, y, center_size, fill='gradient:center_grad',
                   stroke='#000', stroke_width=2)

        # Draw label if the flower has a name
        if "name" in flower_data:
            can.text(x, y + petal_distance + 25,
                     flower_data["name"],
                     16,
                     fill='#000')

    # Draw a coordinate grid to help with positioning
    can.grid(spacing=50, show_coords=True)

    # Define our entire garden as a list of flower dictionaries
    # Each dictionary describes one flower
    garden = [
        {
            "name": "Rose",
            "x": 150,
            "y": 350,
            "size": 20,
            "petal_color": CreativeGardenPalette.ROSE_QUARTZ,
            "center_color": CreativeGardenPalette.BUTTER_YELLOW
        },
        {
            "name": "Tulip",
            "x": 300,
            "y": 350,
            "size": 24,
            "petal_color": CreativeGardenPalette.LILAC_DREAM,
            "center_color": CreativeGardenPalette.LEMON_CHIFFON
        },
        {
            "name": "Daisy",
            "x": 450,
            "y": 350,
            "size": 18,
            "petal_color": CreativeGardenPalette.PEACH_WHISPER,
            "center_color": CreativeGardenPalette.CORAL_BLUSH
        },
        {
            "name": "Lily",
            "x": 600,
            "y": 350,
            "size": 22,
            "petal_color": CreativeGardenPalette.MISTY_MAUVE,
            "center_color": CreativeGardenPalette.BUTTER_YELLOW
        }
    ]

    # Draw all flowers from the data
    # To add more flowers, just add more dictionaries to the list!
    for flower_data in garden:
        draw_flower_from_data(can, flower_data)

    # Your turn! Try adding more flowers or other objects using dictionaries!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-14.svg')
