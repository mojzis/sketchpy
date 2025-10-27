# Lesson 14: Lists + Functions - Building Scenes
# Learn to combine lists and functions for data-driven drawing

can = Canvas(800, 600)

# Optional: Show grid for coordinate reference
# can.grid(spacing=50, show_coords=True)

# Background: Sky
can.rect(0, 0, 800, 300, fill=CalmOasisPalette.SKY_BLUE)

# Background: Road
can.rect(0, 300, 800, 300, fill=Color.GRAY)

# Road markings (dashed line)
for i in range(10):
    can.rect(i * 80 + 10, 395, 40, 10, fill=Color.YELLOW)


def draw_car(canvas, car_data):
    """Draw a car from a dictionary of properties.

    This function separates the drawing logic from the data,
    making it easy to draw many cars with different properties.
    """
    # Car body
    canvas.rect(
        car_data['x'],
        car_data['y'],
        car_data['width'],
        car_data['height'],
        fill=car_data['color']
    )

    # Wheels
    wheel_y = car_data['y'] + car_data['height'] + 15
    wheel_radius = 20
    canvas.circle(car_data['x'] + 30, wheel_y, wheel_radius, fill=Color.BLACK)
    canvas.circle(car_data['x'] + car_data['width'] - 30, wheel_y, wheel_radius, fill=Color.BLACK)

    # Wheel rims (inner circles)
    canvas.circle(car_data['x'] + 30, wheel_y, 10, fill=Color.SILVER)
    canvas.circle(car_data['x'] + car_data['width'] - 30, wheel_y, 10, fill=Color.SILVER)


# Data-driven drawing: Separate data from display logic
# Each dictionary contains all the information needed to draw one car
cars_in_scene = [
    {'x': 50, 'y': 300, 'width': 150, 'height': 80, 'color': Color.RED},
    {'x': 250, 'y': 320, 'width': 180, 'height': 90, 'color': Color.BLUE},
    {'x': 480, 'y': 290, 'width': 140, 'height': 75, 'color': Color.GREEN},
]

# Draw all cars from data using a loop
# Notice how we don't repeat the drawing code - we just call the function!
for car in cars_in_scene:
    draw_car(can, car)

# Challenge: Add more cars to the list!
# Try adding a car with different x, y, width, height, and color values

can
