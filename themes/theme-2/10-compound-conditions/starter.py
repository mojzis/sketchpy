from sketchpy.shapes import Canvas, CreativeGardenPalette


def main():
    # Create a smart garden that changes based on multiple conditions

    can = Canvas(800, 600)

    # Draw a coordinate grid to help with positioning
    can.grid(spacing=50, show_coords=True)

    # Garden environment conditions - try changing these!
    is_spring = True
    has_water = True
    is_sunny = True
    temperature = 75  # Degrees

    # Draw background
    can.rect(0, 0, 800, 350, fill=CreativeGardenPalette.SKY_BREEZE)
    can.rect(0, 350, 800, 250, fill=CreativeGardenPalette.MINT_CREAM)

    # Draw sun if it's sunny
    if is_sunny:
        can.circle(700, 100, 50,
                   fill=CreativeGardenPalette.BUTTER_YELLOW,
                   stroke=CreativeGardenPalette.LEMON_CHIFFON,
                   stroke_width=3)

    # Draw flowers - appearance depends on conditions
    for i in range(6):
        x = 100 + i * 120
        y = 450

        # Flowers bloom well only if it's spring AND there's water
        if is_spring and has_water:
            # Healthy blooming flowers
            petal_color = CreativeGardenPalette.ROSE_QUARTZ
            center_color = CreativeGardenPalette.BUTTER_YELLOW
        else:
            # Wilted or dormant flowers
            petal_color = '#D2B48C'  # Brown
            center_color = '#8B7355'  # Dark brown

        # Draw flower center
        can.circle(x, y, 20, fill=center_color,
                   stroke='#000', stroke_width=2)

        # Draw 4 petals
        can.circle(x, y - 28, 22, fill=petal_color,
                   stroke='#000', stroke_width=1.5)
        can.circle(x + 28, y, 22, fill=petal_color,
                   stroke='#000', stroke_width=1.5)
        can.circle(x, y + 28, 22, fill=petal_color,
                   stroke='#000', stroke_width=1.5)
        can.circle(x - 28, y, 22, fill=petal_color,
                   stroke='#000', stroke_width=1.5)

    # Butterflies appear when it's sunny AND warm (temperature > 70)
    if is_sunny and temperature > 70:
        # Draw a couple of butterflies
        for i in range(2):
            bx = 250 + i * 250
            by = 200

            # Butterfly body
            can.ellipse(bx, by, 12, 40, fill=CreativeGardenPalette.LILAC_DREAM,
                        stroke='#000', stroke_width=2)

            # Wings
            can.circle(bx - 20, by - 10, 18, fill=CreativeGardenPalette.PEACH_WHISPER,
                       stroke='#000', stroke_width=1.5)
            can.circle(bx + 20, by - 10, 18, fill=CreativeGardenPalette.PEACH_WHISPER,
                       stroke='#000', stroke_width=1.5)

    # Your turn! Try changing the conditions or adding more conditional elements!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-10.svg')
