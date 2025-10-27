# Learn about functions with parameters!

can = Canvas(800, 600)

# Draw a coordinate grid to help with positioning (optional)
# can.grid(spacing=50, show_coords=True)

def draw_car(canvas, x, y, width, color):
    """Draw a car at position (x, y) with given width and color.

    This function takes PARAMETERS that let us customize each car:
    - x, y: where to draw the car
    - width: how wide the car should be
    - color: what color to make the car
    """
    # Calculate height proportional to width
    height = width * 0.5

    # Draw car body
    canvas.rect(x, y, width, height, fill=color, stroke=Color.BLACK, stroke_width=2)

    # Calculate wheel size and positions based on car size
    wheel_radius = height * 0.3
    wheel_y = y + height + wheel_radius
    front_wheel_x = x + width * 0.25
    rear_wheel_x = x + width * 0.75

    # Draw wheels
    canvas.circle(front_wheel_x, wheel_y, wheel_radius, fill=Color.BLACK)
    canvas.circle(rear_wheel_x, wheel_y, wheel_radius, fill=Color.BLACK)

# Now we can draw many different cars by passing different ARGUMENTS!
# Each function call uses different values for the parameters

# Small red car
draw_car(can, 50, 200, 150, Color.RED)

# Medium blue car
draw_car(can, 250, 250, 200, Color.BLUE)

# Large green car
draw_car(can, 500, 180, 100, Color.GREEN)

# Your turn! Try calling draw_car() with different arguments
# Can you make a tiny car? A huge car? Try different colors!

can
