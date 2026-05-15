from sketchpy import Canvas, Color
from sketchpy.helpers.cars import CarShapes


def main():
    can = Canvas(800, 600)
    cars = CarShapes(can)

    # Here's an example function. Try modifying it!
    def draw_street_scene(x, y, color):
        """Draw a car on a street"""
        can.rect(x, y, 200, 100, fill="#555555")
        cars.rounded_car(x + 50, y + 30, color=color)

    # Call the function with different positions and colors
    draw_street_scene(100, 200, Color.BLUE)
    draw_street_scene(400, 200, Color.RED)

    # YOUR TURN: define your own function below and call it!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-07.svg')
