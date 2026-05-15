from sketchpy import Canvas, Color
from sketchpy.helpers.cars import CarShapes


def main():
    # Create your canvas
    can = Canvas(800, 600)
    cars = CarShapes(can)

    # YOUR CITY SCENE HERE!
    # Use variables, loops, functions, and conditionals
    # to create something amazing!

    # Example starter:
    # Sky background
    can.rect(0, 0, 800, 300, fill="#87CEEB")

    # Ground
    can.rect(0, 300, 800, 300, fill="#90EE90")

    # Now build your city!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-10.svg')
