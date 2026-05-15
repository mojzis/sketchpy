from sketchpy import Canvas, Color
from sketchpy.helpers.cars import CarShapes


def main():
    can = Canvas(800, 600)
    cars = CarShapes(can)

    # Draw parking lot lines
    can.rect(0, 200, 800, 300, fill="#808080", stroke=Color.BLACK, stroke_width=2)

    # First row - rounded cars
    for i in range(5):
        x = 50 + i * 150
        cars.rounded_car(x, 250, width=120, height=45, color=Color.BLUE)

    # Second row - simple cars
    for i in range(5):
        x = 50 + i * 150
        cars.simple_car(x, 400, width=110, height=45, color=Color.RED)

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-04.svg')
