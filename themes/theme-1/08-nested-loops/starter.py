from sketchpy.shapes import Canvas, Color, CreativeGardenPalette, CalmOasisPalette


def main():
    # Create a multi-story parking garage with elegant gradients!

    can = Canvas(800, 600)

    # Show grid for alignment
    can.grid(spacing=50, show_coords=True)

    # Create two elegant gradients for alternating pattern
    can.linear_gradient("car_warm", start=(0, 0), end=(100, 100),
                        colors=[CreativeGardenPalette.CORAL_BLUSH, CreativeGardenPalette.PEACH_WHISPER])
    can.linear_gradient("car_cool", start=(0, 0), end=(100, 100),
                        colors=[CalmOasisPalette.POWDER_BLUE, CalmOasisPalette.PERIWINKLE])

    # Nested loops create a grid of cars (3 rows × 4 columns)
    for row in range(3):
        for col in range(4):
            # Calculate position for this car
            x = 50 + col * 180
            y = 100 + row * 180

            # Alternating gradient fills based on position
            if (row + col) % 2 == 0:
                car_color = "gradient:car_warm"
            else:
                car_color = "gradient:car_cool"

            # Draw car body with gradient
            can.rect(x, y, 150, 100, fill=car_color)

            # Draw wheels with elegant rims
            can.circle(x + 40, y + 110, 20, fill=Color.BLACK)
            can.circle(x + 110, y + 110, 20, fill=Color.BLACK)
            can.circle(x + 40, y + 110, 10, fill=CalmOasisPalette.MIST_GRAY)
            can.circle(x + 110, y + 110, 10, fill=CalmOasisPalette.MIST_GRAY)

    # Your turn! Try changing:
    # - Number of rows and columns
    # - Spacing between cars
    # - Color pattern (try using row or col alone)
    # - Add windows or other details to the cars
    # - Create your own gradients!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-08.svg')
