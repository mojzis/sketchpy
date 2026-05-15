from sketchpy import Canvas, Color
from sketchpy.helpers.cars import CarShapes


def main():
    can = Canvas(800, 600)
    cars = CarShapes(can)

    # Draw road
    cars.road(y=400, lane_width=80)

    # Alternating car types and colors
    for i in range(6):
        x = 50 + i * 120

        if i % 2 == 0:  # Even positions
            cars.rounded_car(x, 350, color=Color.BLUE)
        else:  # Odd positions
            cars.sports_car(x, 355, color=Color.RED)

    # Traffic lights with different states
    cars.traffic_light(100, 100, active="red")
    cars.traffic_light(400, 100, active="yellow")
    cars.traffic_light(700, 100, active="green")

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-08.svg')
