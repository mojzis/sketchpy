# Create a traffic jam scene with groups and gradients!

can = Canvas(800, 600)

# Show grid for alignment
can.grid(spacing=50, show_coords=True)

# Create elegant gradient for cars
can.linear_gradient("traffic_car", start=(0, 0), end=(100, 100),
                    colors=[CreativeGardenPalette.CORAL_BLUSH, CreativeGardenPalette.ROSE_QUARTZ])

# Starting position for first car
x = 50
y = 300
car_counter = 0

# Draw cars until we run out of space (canvas width is 800)
while x < 750:
    # Use groups to organize each car
    with can.group(f"traffic_car_{car_counter}"):
        # Draw car body with gradient
        can.rect(x, y, 100, 60, fill="gradient:traffic_car")

        # Draw wheels with elegant rims
        can.circle(x + 25, y + 70, 15, fill=Color.BLACK)
        can.circle(x + 75, y + 70, 15, fill=Color.BLACK)
        can.circle(x + 25, y + 70, 8, fill=CalmOasisPalette.MIST_GRAY)
        can.circle(x + 75, y + 70, 8, fill=CalmOasisPalette.MIST_GRAY)

    # Move to next car position
    x = x + 120
    car_counter = car_counter + 1

    # Optional: vary the y position after crossing the middle
    if x > 400:
        y = y + 20

# Your turn! Try:
# - Change the spacing between cars (x = x + ?)
# - Add a counter to stop after exactly 6 cars
# - Make cars alternate colors (create different gradients!)
# - Create a two-lane traffic jam (add another while loop)

can
