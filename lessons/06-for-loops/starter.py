# Create a parking lot with multiple cars using loops!

can = Canvas(800, 600)

# Optional: Show grid to see positions
# can.grid(spacing=50, show_coords=True)

# Background: Sky
can.rect(0, 0, 800, 300, fill=CalmOasisPalette.SKY_BLUE)

# Background: Ground
can.rect(0, 300, 800, 300, fill=Color.GRAY)

# Draw 5 cars in a row using a for loop
# This shows the power of loops - no code repetition!
for i in range(5):
    # Calculate position based on loop variable i
    x_position = 50 + i * 150  # Each car is 150 pixels apart
    y_position = 350

    # Draw car body (rectangle)
    can.rect(x_position, y_position, 120, 60, fill=Color.RED)

    # Draw two wheels (circles)
    can.circle(x_position + 30, y_position + 60, 20, fill=Color.BLACK)
    can.circle(x_position + 90, y_position + 60, 20, fill=Color.BLACK)

# Try this: Change range(5) to range(3) or range(7)
# Try this: Change the spacing (150) to make cars closer or further apart
# Challenge: Add windows to each car (use another rect inside the loop)

can
