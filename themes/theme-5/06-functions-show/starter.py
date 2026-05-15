from sketchpy import Canvas, Color
from sketchpy.helpers.cars import CarShapes


def main():
    can = Canvas(800, 600)
    cars = CarShapes(can)

    # Background
    can.rect(0, 0, 800, 600, fill="#87CEEB", stroke="none")  # Sky

    # Define a function - like creating a recipe
    def draw_intersection(x, y, car_color=Color.BLUE):
        """Draw a complete intersection with traffic light and car"""
        # Draw traffic light
        cars.traffic_light(x, y, active="red")

        # Draw waiting car
        cars.rounded_car(x + 100, y + 140, width=120, color=car_color)

        # Draw road crossing
        can.rect(x - 50, y + 150, 300, 80, fill="#555555")

    # Call the function - use the recipe!
    draw_intersection(100, 50, car_color=Color.BLUE)
    draw_intersection(500, 50, car_color=Color.RED)

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-06.svg')
