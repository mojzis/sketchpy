from sketchpy import Canvas, CreativeGardenPalette, CalmOasisPalette


def main():
    # Create geometric patterns with gradients!

    can = Canvas(800, 600)

    # Show grid for alignment
    can.grid(spacing=50, show_coords=True)

    # Create elegant gradients for our pattern
    can.radial_gradient("circle1", center=(50, 50), radius=60,
                        colors=[CalmOasisPalette.POWDER_BLUE, CalmOasisPalette.PERIWINKLE])
    can.radial_gradient("circle2", center=(50, 50), radius=60,
                        colors=[CreativeGardenPalette.LILAC_DREAM, CreativeGardenPalette.MISTY_MAUVE])

    # Example: Elegant grid of circles with gradients
    spacing = 80
    for row in range(6):
        for col in range(8):
            x = 50 + col * spacing
            y = 50 + row * spacing
            # Alternate gradient fills for a sophisticated look
            if (row + col) % 2 == 0:
                fill = "gradient:circle1"
            else:
                fill = "gradient:circle2"
            can.circle(x, y, 20, fill=fill)

    # Your turn! Create your own pattern below
    # Try creating more gradients with different color combinations!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-03.svg')
