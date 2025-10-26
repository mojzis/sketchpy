# Sunset Garden - Peaceful layered landscape
from sketchpy.shapes import Canvas, CreativeGardenPalette
import random

can = Canvas(400, 400)

# Sky gradient effect with stacked rectangles
sky_colors = [
    CreativeGardenPalette.SKY_BREEZE,
    CreativeGardenPalette.PEACH_WHISPER,
    CreativeGardenPalette.LEMON_CHIFFON,
    CreativeGardenPalette.BUTTER_YELLOW
]
for i, color in enumerate(sky_colors):
    y = i * 100
    can.rect(0, y, 400, 100, fill=color, stroke="none")

# Sun
can.circle(300, 100, 40, fill=CreativeGardenPalette.BUTTER_YELLOW, stroke="none")
can.circle(300, 100, 30, fill=CreativeGardenPalette.LEMON_CHIFFON, stroke="none")

# Rolling hills
can.ellipse(200, 250, 300, 80, fill=CreativeGardenPalette.MINT_CREAM, stroke="none")
can.ellipse(100, 300, 250, 70, fill=CreativeGardenPalette.HONEYDEW, stroke="none")
can.ellipse(300, 320, 200, 60, fill=CreativeGardenPalette.MINT_CREAM, stroke="none")

# Garden flowers - scattered pattern
random.seed(42)
flower_colors = [
    CreativeGardenPalette.ROSE_QUARTZ,
    CreativeGardenPalette.LILAC_DREAM,
    CreativeGardenPalette.PEACH_WHISPER,
    CreativeGardenPalette.CORAL_BLUSH
]

for i in range(15):
    x = random.randint(50, 350)
    y = random.randint(260, 350)
    color = random.choice(flower_colors)
    can.circle(x, y, 8, fill=color, stroke="none")
    can.circle(x, y, 4, fill=CreativeGardenPalette.BUTTER_YELLOW, stroke="none")

can
