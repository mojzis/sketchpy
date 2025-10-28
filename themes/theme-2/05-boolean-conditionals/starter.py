from sketchpy.shapes import Canvas, CreativeGardenPalette


def main():
    # Create a garden scene that changes from day to night

    can = Canvas(800, 600)

    # Draw a coordinate grid to help with positioning
    can.grid(spacing=50, show_coords=True)

    # Try changing this to False to see the night scene!
    is_daytime = True

    # Choose different colors based on whether it's day or night
    if is_daytime:
        sky_color = CreativeGardenPalette.SKY_BREEZE
        ground_color = CreativeGardenPalette.MINT_CREAM
    else:
        sky_color = '#2C3E50'  # Dark blue for night
        ground_color = '#34495E'  # Dark grey-blue for night

    # Draw the sky and ground
    can.rect(0, 0, 800, 350, fill=sky_color)
    can.rect(0, 350, 800, 250, fill=ground_color)

    # Draw sun during day, moon at night
    if is_daytime:
        can.circle(650, 100, 50,
                   fill=CreativeGardenPalette.BUTTER_YELLOW,
                   stroke=CreativeGardenPalette.LEMON_CHIFFON,
                   stroke_width=3)
    else:
        can.circle(650, 100, 45,
                   fill='#F4F4F4',
                   stroke='#E0E0E0',
                   stroke_width=2)

    # Draw flowers that look different during day vs night
    for i in range(5):
        x = 120 + i * 140
        y = 450

        # Different flower colors for day and night
        if is_daytime:
            petal_color = CreativeGardenPalette.ROSE_QUARTZ
            center_color = CreativeGardenPalette.BUTTER_YELLOW
        else:
            petal_color = CreativeGardenPalette.MISTY_MAUVE
            center_color = CreativeGardenPalette.LILAC_DREAM

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

    # Your turn! Try changing is_daytime to False, or add more conditional elements!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-05.svg')
