from sketchpy import Canvas, Color, CreativeGardenPalette, CalmOasisPalette


def main():
    # Create a multi-colored car fleet using lists!

    can = Canvas(800, 600)

    # Optional: Show grid to see positions
    # can.grid(spacing=50, show_coords=True)

    # Create gradient sky
    can.linear_gradient("sky", start=(0, 0), end=(0, 100),
                        colors=[CalmOasisPalette.POWDER_BLUE, CalmOasisPalette.SKY_BLUE])
    can.rect(0, 0, 800, 300, fill="gradient:sky")

    # Background: Ground
    can.rect(0, 300, 800, 300, fill=CalmOasisPalette.MIST_GRAY)

    # Create elegant car gradients
    can.linear_gradient("car1", start=(0, 0), end=(100, 100),
                        colors=[CreativeGardenPalette.CORAL_BLUSH, CreativeGardenPalette.ROSE_QUARTZ])
    can.linear_gradient("car2", start=(0, 0), end=(100, 100),
                        colors=[CalmOasisPalette.POWDER_BLUE, CalmOasisPalette.PERIWINKLE])
    can.linear_gradient("car3", start=(0, 0), end=(100, 100),
                        colors=[CalmOasisPalette.MINT_FRESH, CalmOasisPalette.SAGE_GREEN])
    can.linear_gradient("car4", start=(0, 0), end=(100, 100),
                        colors=[CreativeGardenPalette.BUTTER_YELLOW, CreativeGardenPalette.LEMON_CHIFFON])
    can.linear_gradient("car5", start=(0, 0), end=(100, 100),
                        colors=[CreativeGardenPalette.LILAC_DREAM, CreativeGardenPalette.MISTY_MAUVE])

    # Lists store multiple values in order
    colors = ["gradient:car1", "gradient:car2", "gradient:car3", "gradient:car4", "gradient:car5"]
    sizes = [100, 120, 90, 110, 95]

    # Loop through the lists with enumerate to get both index and value
    for i, color in enumerate(colors):
        # Calculate position based on index
        x = 50 + i * 140
        y = 350

        # Get size from sizes list using index
        car_width = sizes[i]
        car_height = 50

        # Draw car body with gradient from list
        can.rect(x, y, car_width, car_height, fill=color)

        # Draw wheels (always black with gray rims)
        wheel_y = y + car_height
        can.circle(x + 25, wheel_y, 15, fill=Color.BLACK)
        can.circle(x + car_width - 25, wheel_y, 15, fill=Color.BLACK)
        can.circle(x + 25, wheel_y, 8, fill=CalmOasisPalette.MIST_GRAY)
        can.circle(x + car_width - 25, wheel_y, 8, fill=CalmOasisPalette.MIST_GRAY)

    # Try this: Add more gradients and colors to the colors list
    # Try this: Add more sizes to make cars different heights too
    # Challenge: Create a list of car heights and use sizes[i] for width AND height

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-07.svg')
