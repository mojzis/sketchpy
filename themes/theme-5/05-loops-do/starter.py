from sketchpy import Canvas, Color
from sketchpy.helpers.cars import CarShapes


def main():
    can = Canvas(800, 600)
    cars = CarShapes(can)

    # Draw your road
    cars.road(y=400, lane_width=80)

    # Create your loop here
    # Example:
    # for i in range(???):
    #     x = ??? + i * ???
    #     cars.rounded_car(x, 350, color=Color.BLUE)

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-05.svg')
