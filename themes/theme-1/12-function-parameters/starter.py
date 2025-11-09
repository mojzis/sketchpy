from sketchpy import Canvas, Color, CreativeGardenPalette, CalmOasisPalette


def main():
    # Learn about functions with parameters and gradients!

    can = Canvas(800, 600)

    # Draw a coordinate grid to help with positioning (optional)
    # can.grid(spacing=50, show_coords=True)

    # Create elegant gradients for different car styles
    can.linear_gradient("sporty", start=(0, 0), end=(100, 100),
                        colors=[CreativeGardenPalette.CORAL_BLUSH, CreativeGardenPalette.ROSE_QUARTZ])
    can.linear_gradient("elegant", start=(0, 0), end=(100, 100),
                        colors=[CalmOasisPalette.POWDER_BLUE, CalmOasisPalette.PERIWINKLE])
    can.linear_gradient("natural", start=(0, 0), end=(100, 100),
                        colors=[CalmOasisPalette.MINT_FRESH, CalmOasisPalette.SAGE_GREEN])

    def draw_car(canvas, x, y, width, gradient_name):
        """Draw a car at position (x, y) with given width and gradient.

        This function takes PARAMETERS that let us customize each car:
        - x, y: where to draw the car
        - width: how wide the car should be
        - gradient_name: which gradient to use for the car body
        """
        # Calculate height proportional to width
        height = width * 0.5

        # Draw car body with gradient
        canvas.rect(x, y, width, height, fill=f"gradient:{gradient_name}", stroke=Color.BLACK, stroke_width=2)

        # Calculate wheel size and positions based on car size
        wheel_radius = height * 0.3
        wheel_y = y + height + wheel_radius
        front_wheel_x = x + width * 0.25
        rear_wheel_x = x + width * 0.75

        # Draw wheels with elegant rims
        canvas.circle(front_wheel_x, wheel_y, wheel_radius, fill=Color.BLACK)
        canvas.circle(rear_wheel_x, wheel_y, wheel_radius, fill=Color.BLACK)
        canvas.circle(front_wheel_x, wheel_y, wheel_radius * 0.5, fill=CalmOasisPalette.MIST_GRAY)
        canvas.circle(rear_wheel_x, wheel_y, wheel_radius * 0.5, fill=CalmOasisPalette.MIST_GRAY)

    # Now we can draw many different cars by passing different ARGUMENTS!
    # Each function call uses different values for the parameters

    # Small sporty car
    draw_car(can, 50, 200, 150, "sporty")

    # Medium elegant car
    draw_car(can, 250, 250, 200, "elegant")

    # Large natural car
    draw_car(can, 500, 180, 100, "natural")

    # Your turn! Try calling draw_car() with different arguments
    # Can you make a tiny car? A huge car? Try different gradients!
    # Create your own gradient and use it!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-12.svg')
