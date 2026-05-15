from sketchpy import Canvas, Color
from sketchpy.helpers.cars import CarShapes


def main():
    # Create a canvas (800 pixels wide, 600 pixels tall)
    can = Canvas(800, 600)

    # Create car drawing helper
    cars = CarShapes(can)

    # Draw a road
    cars.road(y=400, lane_width=80)

    # Draw a modern curvy car
    cars.rounded_car(x=200, y=350, width=140, height=50, color=Color.BLUE)

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-01.svg')
