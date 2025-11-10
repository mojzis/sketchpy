from sketchpy import Canvas, MathDoodlingPalette


def main():
    can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

    num_rings = 12
    start_radius = 260

    for i in range(num_rings):
        # Drift offset increases with each ring
        offset_x = i * 7
        offset_y = i * 5

        # Radius decreases with each ring
        radius = start_radius - (i * 20)

        can.circle(400 + offset_x, 300 + offset_y, radius,
                   fill=MathDoodlingPalette.MIST_ROSE,
                   opacity=0.2,
                   stroke='none')

    # See the rippling effect? Like dropping a stone in water!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-06.svg')
