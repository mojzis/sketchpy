from sketchpy import Canvas, Color, CreativeGardenPalette, CalmOasisPalette


def main():
    # Lesson 14: Lists + Functions + Gradients - Building Elegant Scenes
    # Learn to combine lists and functions for data-driven drawing

    can = Canvas(800, 600)

    # Optional: Show grid for coordinate reference
    # can.grid(spacing=50, show_coords=True)

    # Create gradient sky
    can.linear_gradient("sky", start=(0, 0), end=(0, 100),
                        colors=[CalmOasisPalette.POWDER_BLUE, CalmOasisPalette.SKY_BLUE])
    can.rect(0, 0, 800, 300, fill="gradient:sky")

    # Background: Road
    can.rect(0, 300, 800, 300, fill=CalmOasisPalette.MIST_GRAY)

    # Road markings (dashed line)
    for i in range(10):
        can.rect(i * 80 + 10, 395, 40, 10, fill=CreativeGardenPalette.BUTTER_YELLOW)

    # Create elegant car gradients
    can.linear_gradient("car_red", start=(0, 0), end=(100, 100),
                        colors=[CreativeGardenPalette.CORAL_BLUSH, CreativeGardenPalette.ROSE_QUARTZ])
    can.linear_gradient("car_blue", start=(0, 0), end=(100, 100),
                        colors=[CalmOasisPalette.POWDER_BLUE, CalmOasisPalette.PERIWINKLE])
    can.linear_gradient("car_yellow", start=(0, 0), end=(100, 100),
                        colors=[CreativeGardenPalette.BUTTER_YELLOW, CreativeGardenPalette.LEMON_CHIFFON])
    can.linear_gradient("car_green", start=(0, 0), end=(100, 100),
                        colors=[CalmOasisPalette.MINT_FRESH, CalmOasisPalette.SAGE_GREEN])


    def draw_car(canvas, car_data):
        """Draw a car from a dictionary of properties with elegant gradients.

        This function separates the drawing logic from the data,
        making it easy to draw many cars with different properties.
        """
        # Car body with gradient
        canvas.rect(
            car_data['x'],
            car_data['y'],
            car_data['width'],
            car_data['height'],
            fill=car_data['gradient']
        )

        # Wheels
        wheel_y = car_data['y'] + car_data['height'] + 15
        wheel_radius = 20
        canvas.circle(car_data['x'] + 30, wheel_y, wheel_radius, fill=Color.BLACK)
        canvas.circle(car_data['x'] + car_data['width'] - 30, wheel_y, wheel_radius, fill=Color.BLACK)

        # Wheel rims (inner circles with elegant gray)
        canvas.circle(car_data['x'] + 30, wheel_y, 10, fill=CalmOasisPalette.MIST_GRAY)
        canvas.circle(car_data['x'] + car_data['width'] - 30, wheel_y, 10, fill=CalmOasisPalette.MIST_GRAY)


    # Data-driven drawing: Separate data from display logic
    # Each dictionary contains all the information needed to draw one car
    cars_in_scene = [
        {'x': 50, 'y': 300, 'width': 150, 'height': 80, 'gradient': 'gradient:car_red'},
        {'x': 250, 'y': 320, 'width': 180, 'height': 90, 'gradient': 'gradient:car_blue'},
        {'x': 480, 'y': 290, 'width': 140, 'height': 75, 'gradient': 'gradient:car_green'},
    ]

    # Draw all cars from data using a loop
    # Notice how we don't repeat the drawing code - we just call the function!
    for car in cars_in_scene:
        draw_car(can, car)

    # Challenge: Add more cars to the list!
    # Try adding a car with different x, y, width, height, and gradient values
    # Create your own gradient and use it in the cars list!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-14.svg')
