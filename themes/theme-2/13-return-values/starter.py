from sketchpy import Canvas, CreativeGardenPalette


def main():
    # Use functions that return values to organize our code

    can = Canvas(800, 600)

    def calculate_flower_dimensions(base_size):
        """Calculate all flower dimensions from a base size

        Returns: (center_size, petal_size, petal_distance)
        """
        center_size = int(base_size * 0.7)
        petal_size = base_size
        petal_distance = int(base_size * 1.4)

        # Return multiple values as a tuple
        return center_size, petal_size, petal_distance

    def get_flower_color(position_index):
        """Return flower color based on position

        Different positions get different colors for variety.
        """
        colors = [
            CreativeGardenPalette.ROSE_QUARTZ,
            CreativeGardenPalette.LILAC_DREAM,
            CreativeGardenPalette.PEACH_WHISPER,
            CreativeGardenPalette.CORAL_BLUSH
        ]

        # Use modulo to cycle through colors
        color_index = position_index % len(colors)
        return colors[color_index]

    def draw_flower(can, x, y, base_size, petal_color):
        """Draw a flower using calculated dimensions"""
        # Call function and capture its return values
        center_size, petal_size, petal_distance = calculate_flower_dimensions(base_size)

        # Create radial gradients for depth
        can.radial_gradient("petal_grad", center=(50, 50), radius=60,
                            colors=['#FFFFFF', petal_color])
        can.radial_gradient("center_grad", center=(50, 50), radius=60,
                            colors=[CreativeGardenPalette.BUTTER_YELLOW, '#F4E08A'])

        # Draw 4 petals with symmetric layering using calculated distance
        can.circle(x, y - petal_distance, petal_size, fill='gradient:petal_grad',
                   stroke='#000', stroke_width=1.5)
        can.circle(x, y + petal_distance, petal_size, fill='gradient:petal_grad',
                   stroke='#000', stroke_width=1.5)

        can.circle(x + petal_distance, y, petal_size, fill='gradient:petal_grad',
                   stroke='#000', stroke_width=1.5)
        can.circle(x - petal_distance, y, petal_size, fill='gradient:petal_grad',
                   stroke='#000', stroke_width=1.5)

        # Draw center (LAST - top layer)
        can.circle(x, y, center_size,
                   fill='gradient:center_grad',
                   stroke='#000', stroke_width=2)

    # Draw a coordinate grid to help with positioning
    can.grid(spacing=50, show_coords=True)

    # Draw flowers using return values
    for i in range(5):
        x = 100 + i * 140
        y = 350
        size = 18 + i * 2  # Gradually increasing size

        # Get color for this position using return value
        color = get_flower_color(i)

        # Draw flower with calculated color and dimensions
        draw_flower(can, x, y, size, color)

    # Your turn! Try creating more functions that return calculated values!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-13.svg')
