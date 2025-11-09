from sketchpy.shapes import Canvas, OceanPalette, OceanShapes

def main():
    can = Canvas(800, 600)
    ocean = OceanShapes(can)

    # Variables: storage boxes for values!
    # Try changing these numbers:
    x1 = 200
    y1 = 300
    small_size = 80

    x2 = 400
    y2 = 250
    medium_size = 120

    x3 = 600
    y3 = 350
    big_size = 150

    # Now use the variables to draw three octopuses
    ocean.octopus(x1, y1, size=small_size, body_color=OceanPalette.CORAL)
    ocean.octopus(x2, y2, size=medium_size, body_color=OceanPalette.PURPLE_CORAL)
    ocean.octopus(x3, y3, size=big_size, body_color=OceanPalette.STARFISH_ORANGE)

    return can

if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-02.svg')
