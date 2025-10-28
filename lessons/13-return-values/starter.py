from sketchpy.shapes import Canvas, Color, CreativeGardenPalette, CalmOasisPalette


def main():
    # Learn about return values from functions with elegant palettes!

    can = Canvas(800, 600)

    # Draw a coordinate grid to help with positioning (optional)
    # can.grid(spacing=50, show_coords=True)

    # Create elegant gradients
    can.linear_gradient("fast", start=(0, 0), end=(100, 100),
                        colors=[CreativeGardenPalette.CORAL_BLUSH, CreativeGardenPalette.ROSE_QUARTZ])
    can.linear_gradient("medium", start=(0, 0), end=(100, 100),
                        colors=[CreativeGardenPalette.BUTTER_YELLOW, CreativeGardenPalette.PEACH_WHISPER])
    can.linear_gradient("slow", start=(0, 0), end=(100, 100),
                        colors=[CalmOasisPalette.POWDER_BLUE, CalmOasisPalette.PERIWINKLE])

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

    def get_car_gradient(speed):
        """Return appropriate gradient name based on speed.

        Fast cars (>150) get sporty gradient
        Medium cars (>100) get warm gradient
        Slow cars get cool gradient
        """
        if speed > 150:
            return "fast"
        elif speed > 100:
            return "medium"
        else:
            return "slow"

    # Use returned values to draw a car

    # Set car speed
    speed = 180

    # Call function and capture the RETURNED gradient name
    car_gradient = get_car_gradient(speed)

    # Car position and size
    car_x = 200
    car_width = 250

    # Draw the car body using the returned gradient
    can.rect(car_x, 300, car_width, 80, fill=f"gradient:{car_gradient}", stroke=Color.BLACK, stroke_width=2)

    # Call function and capture the RETURNED wheel positions
    wheel_positions = calculate_wheel_positions(car_x, 300, car_width)

    # Use the returned positions to draw wheels with elegant rims
    for x, y in wheel_positions:
        can.circle(x, y, 25, fill=Color.BLACK)
        can.circle(x, y, 12, fill=CalmOasisPalette.MIST_GRAY)

    # Your turn! Try different speeds to see different gradients
    # Can you add a function that returns the car's height based on width?
    # Can you create a function that returns a gradient name based on other criteria?

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-13.svg')
