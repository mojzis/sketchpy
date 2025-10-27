# Create a multi-colored car fleet using lists!

# Lists store multiple values in order
colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE]
sizes = [100, 120, 90, 110, 95]

can = Canvas(800, 600)

# Optional: Show grid to see positions
# can.grid(spacing=50, show_coords=True)

# Background: Sky
can.rect(0, 0, 800, 300, fill=CalmOasisPalette.SKY_BLUE)

# Background: Ground
can.rect(0, 300, 800, 300, fill=Color.GRAY)

# Loop through the lists with enumerate to get both index and value
for i, color in enumerate(colors):
    # Calculate position based on index
    x = 50 + i * 140
    y = 350

    # Get size from sizes list using index
    car_width = sizes[i]
    car_height = 50

    # Draw car body with color from list
    can.rect(x, y, car_width, car_height, fill=color)

    # Draw wheels (always black)
    wheel_y = y + car_height
    can.circle(x + 25, wheel_y, 15, fill=Color.BLACK)
    can.circle(x + car_width - 25, wheel_y, 15, fill=Color.BLACK)

# Try this: Add more colors to the colors list
# Try this: Add more sizes to make cars different heights too
# Challenge: Create a list of car heights and use sizes[i] for width AND height

can
