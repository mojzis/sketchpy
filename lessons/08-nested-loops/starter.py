# Create a multi-story parking garage!

can = Canvas(800, 600)

# Show grid for alignment
can.grid(spacing=50, show_coords=True)

# Nested loops create a grid of cars (3 rows × 4 columns)
for row in range(3):
    for col in range(4):
        # Calculate position for this car
        x = 50 + col * 180
        y = 100 + row * 180

        # Alternating colors based on position
        if (row + col) % 2 == 0:
            car_color = Color.RED
        else:
            car_color = Color.BLUE

        # Draw car body
        can.rect(x, y, 150, 100, fill=car_color)

        # Draw wheels
        can.circle(x + 40, y + 110, 20, fill=Color.BLACK)
        can.circle(x + 110, y + 110, 20, fill=Color.BLACK)

# Your turn! Try changing:
# - Number of rows and columns
# - Spacing between cars
# - Color pattern (try using row or col alone)
# - Add windows or other details to the cars

can
