# Create geometric patterns!

can = Canvas(800, 600)

# Show grid for alignment
can.grid(spacing=50, show_coords=True)

# Example: Simple grid of circles
spacing = 80
for row in range(6):
    for col in range(8):
        x = 50 + col * spacing
        y = 50 + row * spacing
        # Alternate colors
        if (row + col) % 2 == 0:
            fill = CalmOasisPalette.POWDER_BLUE
        else:
            fill = CreativeGardenPalette.LILAC_DREAM
        can.circle(x, y, 20, fill=fill)

# Your turn! Create your own pattern below

can
