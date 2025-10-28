from sketchpy.shapes import Canvas, CreativeGardenPalette, CalmOasisPalette


def main():
    # Create a colorful garden with gradients!

    can = Canvas(800, 600)

    # Create a beautiful gradient sky
    can.linear_gradient("sky", start=(0, 0), end=(0, 100),
                        colors=[CalmOasisPalette.POWDER_BLUE, CalmOasisPalette.SKY_BLUE])
    can.rect(0, 0, 800, 300, fill="gradient:sky")

    # Background: Grass (bottom half)
    can.rect(0, 300, 800, 300, fill=CreativeGardenPalette.MINT_CREAM)

    # Draw multiple flowers using a loop
    # TODO: Use a for loop to draw 5 flowers

    # Example: Draw ONE flower first, then put it in a loop
    # This flower uses a radial gradient for depth
    cx, cy = 150, 250

    # Create gradient for the flower petals
    can.radial_gradient("petal", center=(50, 50), radius=50,
                        colors=[CreativeGardenPalette.ROSE_QUARTZ, CreativeGardenPalette.CORAL_BLUSH])

    can.circle(cx, cy, 30, fill="gradient:petal")
    can.circle(cx, cy, 15, fill=CreativeGardenPalette.BUTTER_YELLOW)

    # Your turn! Add more flowers with a loop
    # for i in range(5):
    #     x = 150 + i * 150
    #     y = 250
    #     # Draw flower at (x, y) - try using the gradient!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-02.svg')
