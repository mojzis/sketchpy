# Create a traffic jam scene!

can = Canvas(800, 600)

# Show grid for alignment
can.grid(spacing=50, show_coords=True)

# Starting position for first car
x = 50
y = 300

# Draw cars until we run out of space (canvas width is 800)
while x < 750:
    # Draw car body
    can.rect(x, y, 100, 60, fill=Color.RED)

    # Draw wheels
    can.circle(x + 25, y + 70, 15, fill=Color.BLACK)
    can.circle(x + 75, y + 70, 15, fill=Color.BLACK)

    # Move to next car position
    x = x + 120

    # Optional: vary the y position after crossing the middle
    if x > 400:
        y = y + 20

# Your turn! Try:
# - Change the spacing between cars (x = x + ?)
# - Add a counter to stop after exactly 6 cars
# - Make cars alternate colors
# - Create a two-lane traffic jam (add another while loop)

can
