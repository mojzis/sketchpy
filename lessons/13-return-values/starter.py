# Learn about return values from functions!

can = Canvas(800, 600)

# Draw a coordinate grid to help with positioning (optional)
# can.grid(spacing=50, show_coords=True)

def calculate_wheel_positions(car_x, car_y, car_width):
    """Calculate where wheels should be placed.

    This function RETURNS a list of (x, y) tuples.
    Instead of drawing, it just calculates and gives back the positions.
    """
    wheel_y = car_y + 80
    front_wheel_x = car_x + car_width * 0.25
    rear_wheel_x = car_x + car_width * 0.75

    # The RETURN statement sends back a value
    return [(front_wheel_x, wheel_y), (rear_wheel_x, wheel_y)]

def get_car_color(speed):
    """Return appropriate color based on speed.

    Fast cars (>150) get RED
    Medium cars (>100) get ORANGE
    Slow cars get BLUE
    """
    if speed > 150:
        return Color.RED
    elif speed > 100:
        return Color.ORANGE
    else:
        return Color.BLUE

# Use returned values to draw a car

# Set car speed
speed = 180

# Call function and capture the RETURNED color
car_color = get_car_color(speed)

# Car position and size
car_x = 200
car_width = 250

# Draw the car body using the returned color
can.rect(car_x, 300, car_width, 80, fill=car_color, stroke=Color.BLACK, stroke_width=2)

# Call function and capture the RETURNED wheel positions
wheel_positions = calculate_wheel_positions(car_x, 300, car_width)

# Use the returned positions to draw wheels
for x, y in wheel_positions:
    can.circle(x, y, 25, fill=Color.BLACK)

# Your turn! Try different speeds to see different colors
# Can you add a function that returns the car's height based on width?

can
