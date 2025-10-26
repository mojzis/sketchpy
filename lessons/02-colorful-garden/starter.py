# Create a colorful garden!

can = Canvas(800, 600)

# Background: Sky (top half)
can.rect(0, 0, 800, 300, fill=CalmOasisPalette.SKY_BLUE)

# Background: Grass (bottom half)
can.rect(0, 300, 800, 300, fill=CreativeGardenPalette.MINT_CREAM)

# Draw multiple flowers using a loop
# TODO: Use a for loop to draw 5 flowers

# Example: Draw ONE flower first, then put it in a loop
cx, cy = 150, 250
can.circle(cx, cy, 30, fill=CreativeGardenPalette.ROSE_QUARTZ)
can.circle(cx, cy, 15, fill=CreativeGardenPalette.BUTTER_YELLOW)

# Your turn! Add more flowers with a loop
# for i in range(5):
#     x = 150 + i * 150
#     y = 250
#     # Draw flower at (x, y)

can
