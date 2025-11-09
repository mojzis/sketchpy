from sketchpy.shapes import Canvas, OceanPalette, OceanShapes

def main():
    can = Canvas(800, 600)
    ocean = OceanShapes(can)

    # YOUR TURN! Create variables for three jellyfish
    # Jellyfish 1: somewhere on the left side
    x1 = 150
    y1 = 200
    size1 = 80

    # Jellyfish 2: in the middle
    x2 = 400  # Try changing this!
    y2 = 150  # And this!
    size2 = 100

    # Jellyfish 3: on the right side
    # Create your own variables here!
    x3 = 650
    y3 = 250
    size3 = 90

    # Draw the jellyfish using your variables
    ocean.jellyfish(x1, y1, size=size1)
    ocean.jellyfish(x2, y2, size=size2, body_color=OceanPalette.SHALLOW_WATER)
    ocean.jellyfish(x3, y3, size=size3)

    # CHALLENGE: Add seaweed at the bottom!
    # ocean.seaweed(x, y, height=150, color=OceanPalette.KELP_GREEN)

    return can

if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-03.svg')
