from sketchpy import Canvas, Color
from sketchpy.helpers.cars import CarShapes


def main():
    can = Canvas(800, 600)
    cars = CarShapes(can)

    # Draw road
    cars.road(y=450, lane_width=80)

    # Variables for sedan (rounded car)
    sedan_x = 100
    sedan_y = 400
    sedan_color = Color.BLUE

    # Variables for sports car
    sports_x = 350
    sports_y = 250
    sports_color = Color.RED

    # Variables for bus
    bus_x = 550
    bus_y = 380
    bus_width = 200
    bus_color = Color.YELLOW

    # Draw vehicles using variables
    cars.rounded_car(sedan_x, sedan_y, color=sedan_color)
    cars.sports_car(sports_x, sports_y, color=sports_color)
    cars.bus(bus_x, bus_y, width=bus_width, color=bus_color)

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-02.svg')
