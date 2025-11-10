from sketchpy import Canvas, CreativeGardenPalette


def main():
    # Create a diverse garden using parameters to customize each flower

    can = Canvas(800, 600)

    def draw_flower(can, x, y, size, petal_color, center_color):
        """Draw a customizable flower

        Parameters control size and colors, making each flower unique!
        """
        # Calculate proportional sizes based on the size parameter
        center_size = int(size * 0.7)  # Center is 70% of petal size
        petal_size = size
        petal_distance = int(size * 1.4)  # Petals positioned 1.4x size away

        # Create radial gradients for depth
        can.radial_gradient("petal_grad", center=(50, 50), radius=60,
                            colors=['#FFFFFF', petal_color])
        can.radial_gradient("center_grad", center=(50, 50), radius=60,
                            colors=[center_color, '#F4E08A'])

        # Draw 4 petals with symmetric layering and custom color
        can.circle(x, y - petal_distance, petal_size, fill='gradient:petal_grad',
                   stroke='#000', stroke_width=1.5)
        can.circle(x, y + petal_distance, petal_size, fill='gradient:petal_grad',
                   stroke='#000', stroke_width=1.5)

        can.circle(x + petal_distance, y, petal_size, fill='gradient:petal_grad',
                   stroke='#000', stroke_width=1.5)
        can.circle(x - petal_distance, y, petal_size, fill='gradient:petal_grad',
                   stroke='#000', stroke_width=1.5)

        # Draw flower center with custom color (LAST - top layer)
        can.circle(x, y, center_size, fill='gradient:center_grad',
                   stroke='#000', stroke_width=2)

    # Draw a coordinate grid to help with positioning
    can.grid(spacing=50, show_coords=True)

    # Draw flowers with different sizes and colors
    # Each one is unique thanks to parameters!
    draw_flower(can, 150, 300, 20,
                CreativeGardenPalette.ROSE_QUARTZ,
                CreativeGardenPalette.BUTTER_YELLOW)

    draw_flower(can, 350, 300, 25,
                CreativeGardenPalette.LILAC_DREAM,
                CreativeGardenPalette.LEMON_CHIFFON)

    draw_flower(can, 550, 300, 18,
                CreativeGardenPalette.PEACH_WHISPER,
                CreativeGardenPalette.CORAL_BLUSH)

    # Use a loop to create a gradient of sizes
    for i in range(5):
        x = 80 + i * 140
        y = 480
        size = 15 + i * 2  # Sizes: 15, 17, 19, 21, 23

        draw_flower(can, x, y, size,
                    CreativeGardenPalette.MISTY_MAUVE,
                    CreativeGardenPalette.BUTTER_YELLOW)

    # Your turn! Try creating flowers with different parameter combinations!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-12.svg')
