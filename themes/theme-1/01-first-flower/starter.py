from sketchpy.shapes import Canvas, Color, CreativeGardenPalette


def main():
    # Draw your flower here!

    can = Canvas(800, 600)

    # Draw a coordinate grid to help with positioning
    can.grid(spacing=50, show_coords=True)

    # Flower center position
    cx, cy = 400, 250

    # Stem
    can.rect(cx - 5, cy + 35, 10, 200, fill=CreativeGardenPalette.MINT_CREAM)

    # Draw 5 petals around the center (like a simple flower)
    petal_radius = 50
    can.circle(cx, cy - 50, petal_radius, fill=CreativeGardenPalette.ROSE_QUARTZ)  # Top
    can.circle(cx, cy + 50, petal_radius, fill=CreativeGardenPalette.ROSE_QUARTZ)  # Bottom
    can.circle(cx + 50, cy - 30, petal_radius, fill=CreativeGardenPalette.CORAL_BLUSH)  # Top right
    can.circle(cx + 50, cy + 30, petal_radius, fill=CreativeGardenPalette.LILAC_DREAM)  # Bottom right
    can.circle(cx - 50, cy + 30, petal_radius, fill=CreativeGardenPalette.SKY_BREEZE)  # Bottom left
    can.circle(cx - 50, cy - 30, petal_radius, fill=CreativeGardenPalette.PEACH_WHISPER)  # Top left

    # Flower center
    can.circle(cx, cy, 35, fill=CreativeGardenPalette.BUTTER_YELLOW)


    # Left leaf (ellipse)
    can.ellipse(cx - 35, cy + 140, 30, 15, fill=CreativeGardenPalette.HONEYDEW)

    # Right leaf (ellipse)
    can.ellipse(cx + 35, cy + 190, 30, 15, fill=CreativeGardenPalette.MINT_CREAM)

    # Your turn! Add more petals, change colors, or create your own garden!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-01.svg')
