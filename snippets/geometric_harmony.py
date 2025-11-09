# Geometric Harmony - Balanced pattern design
from sketchpy import Canvas, CreativeGardenPalette, CalmOasisPalette

can = Canvas(400, 400)

# Background
can.rect(0, 0, 400, 400, fill=CalmOasisPalette.CREAM, stroke="none")

# Create concentric squares with alternating palettes
square_sets = [
    (200, 200, 180, CreativeGardenPalette.LILAC_DREAM),
    (200, 200, 160, CalmOasisPalette.MINT_FRESH),
    (200, 200, 140, CreativeGardenPalette.PEACH_WHISPER),
    (200, 200, 120, CalmOasisPalette.LAVENDER_MIST),
    (200, 200, 100, CreativeGardenPalette.SKY_BREEZE),
    (200, 200, 80, CalmOasisPalette.SEAFOAM),
    (200, 200, 60, CreativeGardenPalette.ROSE_QUARTZ),
    (200, 200, 40, CalmOasisPalette.PALE_LILAC),
]

for cx, cy, size, color in square_sets:
    x = cx - size // 2
    y = cy - size // 2
    can.rect(x, y, size, size, fill=color, stroke="none")

# Add corner accent circles
corner_color = CreativeGardenPalette.BUTTER_YELLOW
accent_positions = [
    (50, 50), (350, 50), (50, 350), (350, 350)
]

for x, y in accent_positions:
    can.circle(x, y, 30, fill=corner_color, stroke="none")
    can.circle(x, y, 20, fill=CalmOasisPalette.PERIWINKLE, stroke="none")
    can.circle(x, y, 10, fill=corner_color, stroke="none")

# Add small decorative elements between corners
can.circle(200, 50, 15, fill=CreativeGardenPalette.CORAL_BLUSH, stroke="none")
can.circle(50, 200, 15, fill=CalmOasisPalette.SAGE_GREEN, stroke="none")
can.circle(350, 200, 15, fill=CreativeGardenPalette.MISTY_MAUVE, stroke="none")
can.circle(200, 350, 15, fill=CalmOasisPalette.SOFT_AQUA, stroke="none")

can
