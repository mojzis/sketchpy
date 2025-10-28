# Draw a day/night car scene with conditionals and gradients!

can = Canvas(800, 600)

# Boolean variables - these are True or False values
is_night = True
speed = 150

# Conditional drawing - different results based on conditions
# The if/else statement makes decisions in your code
if is_night:
    # Night time scene with dramatic gradient
    can.linear_gradient("night_sky", start=(0, 0), end=(0, 100),
                        colors=["#001a33", "#003366", "#004d80"])
    can.rect(0, 0, 800, 600, fill="gradient:night_sky")

    # Moon with gentle glow
    can.radial_gradient("moon_glow", center=(50, 50), radius=50,
                        colors=[CreativeGardenPalette.LEMON_CHIFFON, CreativeGardenPalette.BUTTER_YELLOW])
    can.circle(700, 100, 40, fill="gradient:moon_glow")
    can.text(400, 50, "Night Drive", size=24, fill=CalmOasisPalette.CREAM)

    # Stars in the night sky
    can.circle(100, 80, 3, fill=Color.WHITE)
    can.circle(200, 120, 3, fill=Color.WHITE)
    can.circle(150, 60, 3, fill=Color.WHITE)
    can.circle(300, 90, 3, fill=Color.WHITE)
    can.circle(500, 70, 3, fill=Color.WHITE)
    can.circle(600, 150, 3, fill=Color.WHITE)
else:
    # Day time scene with beautiful gradient
    can.linear_gradient("day_sky", start=(0, 0), end=(0, 100),
                        colors=[CalmOasisPalette.POWDER_BLUE, CalmOasisPalette.SKY_BLUE, CalmOasisPalette.SOFT_AQUA])
    can.rect(0, 0, 800, 600, fill="gradient:day_sky")

    # Bright sun
    can.radial_gradient("sun_glow", center=(50, 50), radius=50,
                        colors=[Color.YELLOW, CreativeGardenPalette.BUTTER_YELLOW])
    can.circle(700, 100, 40, fill="gradient:sun_glow")
    can.text(400, 50, "Day Drive", size=24, fill=Color.BLACK)

# Draw the road (same for both day and night)
can.rect(0, 450, 800, 150, fill=CalmOasisPalette.MIST_GRAY)

# Draw lane markings
for i in range(5):
    x = 50 + i * 180
    can.rect(x, 520, 80, 10, fill=Color.WHITE)

# Create elegant car gradient
can.linear_gradient("car_paint", start=(0, 0), end=(100, 100),
                    colors=[CreativeGardenPalette.CORAL_BLUSH, CreativeGardenPalette.ROSE_QUARTZ])

# Draw the car (same for both day and night)
can.rect(200, 400, 300, 100, fill="gradient:car_paint", stroke=Color.BLACK, stroke_width=2)
can.rect(275, 340, 150, 60, fill="gradient:car_paint", stroke=Color.BLACK, stroke_width=2)

# Wheels
can.circle(250, 520, 40, fill=Color.BLACK)
can.circle(450, 520, 40, fill=Color.BLACK)
can.circle(250, 520, 20, fill=CalmOasisPalette.MIST_GRAY)
can.circle(450, 520, 20, fill=CalmOasisPalette.MIST_GRAY)

# Headlights (bigger at night to show they're on with glowing effect)
if is_night:
    # Bright headlights with glow effect at night
    can.radial_gradient("headlight_glow", center=(50, 50), radius=70,
                        colors=[Color.YELLOW, CreativeGardenPalette.BUTTER_YELLOW])
    can.circle(190, 450, 12, fill="gradient:headlight_glow")
else:
    can.circle(190, 450, 6, fill=CreativeGardenPalette.BUTTER_YELLOW)

# Show different speed message based on comparison
# Comparison operators: > (greater than), < (less than), == (equal to)
if speed > 120:
    can.text(350, 580, "SPEEDING! Slow down!", size=24, fill=CreativeGardenPalette.CORAL_BLUSH)
else:
    can.text(350, 580, "Safe speed", size=24, fill=CreativeGardenPalette.MINT_CREAM)

# Your turn! Try these challenges:
# 1. Change is_night to False and see the scene change
# 2. Change the speed value and see the message change
# 3. Add more conditional elements (traffic lights, weather)
# 4. Try adding elif for a third condition (morning/afternoon/night)

can
