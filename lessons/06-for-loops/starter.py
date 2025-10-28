from sketchpy.shapes import Canvas, Color, CreativeGardenPalette, CalmOasisPalette


def main():
    # Create a parking lot with multiple cars using loops and groups!

    can = Canvas(800, 600)

    # Optional: Show grid to see positions
    # can.grid(spacing=50, show_coords=True)

    # Create gradient sky
    can.linear_gradient("sky", start=(0, 0), end=(0, 100),
                        colors=[CalmOasisPalette.POWDER_BLUE, CalmOasisPalette.SKY_BLUE])
    can.rect(0, 0, 800, 300, fill="gradient:sky")

    # Background: Ground
    can.rect(0, 300, 800, 300, fill=CalmOasisPalette.MIST_GRAY)

    # Create gradients for different colored cars
    can.linear_gradient("car_red", start=(0, 0), end=(100, 100),
                        colors=[CreativeGardenPalette.CORAL_BLUSH, CreativeGardenPalette.ROSE_QUARTZ])
    can.linear_gradient("car_blue", start=(0, 0), end=(100, 100),
                        colors=[CalmOasisPalette.POWDER_BLUE, CalmOasisPalette.SKY_BLUE])
    can.linear_gradient("car_green", start=(0, 0), end=(100, 100),
                        colors=[CalmOasisPalette.MINT_FRESH, CalmOasisPalette.SAGE_GREEN])

    # Draw 5 cars in a row using a for loop
    # This shows the power of loops - no code repetition!
    car_colors = ["gradient:car_red", "gradient:car_blue", "gradient:car_green",
                  CreativeGardenPalette.LILAC_DREAM, CreativeGardenPalette.PEACH_WHISPER]

    for i in range(5):
        # Calculate position based on loop variable i
        x_position = 50 + i * 150  # Each car is 150 pixels apart
        y_position = 350

        # Use groups to organize each car as a unit
        with can.group(f"car_{i}"):
            # Draw car body with gradient
            can.rect(x_position, y_position, 120, 60, fill=car_colors[i])

            # Draw two wheels
            can.circle(x_position + 30, y_position + 60, 20, fill=Color.BLACK)
            can.circle(x_position + 90, y_position + 60, 20, fill=Color.BLACK)

            # Wheel rims
            can.circle(x_position + 30, y_position + 60, 10, fill=CalmOasisPalette.MIST_GRAY)
            can.circle(x_position + 90, y_position + 60, 10, fill=CalmOasisPalette.MIST_GRAY)

    # Try this: Change range(5) to range(3) or range(7)
    # Try this: Change the spacing (150) to make cars closer or further apart
    # Challenge: Add windows to each car (use another rect inside the loop and group)

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-06.svg')
