from sketchpy import Canvas, OceanPalette, OceanShapes

def main():
    can = Canvas(800, 600)
    ocean = OceanShapes(can)

    # Lists: multiple values in one container!
    sizes = [80, 120, 100, 140]
    colors = [
        OceanPalette.CORAL,
        OceanPalette.PURPLE_CORAL,
        OceanPalette.STARFISH_ORANGE,
        OceanPalette.TROPICAL_YELLOW
    ]

    # Loop through list with enumerate to get index and value
    for i, size in enumerate(sizes):
        x = 100 + i * 160
        ocean.octopus(x, 300, size=size, body_color=colors[i])

    return can

if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-06.svg')
