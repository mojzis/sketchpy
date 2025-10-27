# Draw a day/night car scene with conditionals!

can = Canvas(800, 600)

# Boolean variables - these are True or False values
is_night = True
speed = 150

# Conditional drawing - different results based on conditions
# The if/else statement makes decisions in your code
if is_night:
    # Night time scene
    can.rect(0, 0, 800, 600, fill="#001122")  # Dark blue sky
    can.circle(700, 100, 40, fill=Color.YELLOW)  # Moon
    can.text(400, 50, "Night Drive", size=24, fill=Color.WHITE)

    # Stars in the night sky
    can.circle(100, 80, 3, fill=Color.WHITE)
    can.circle(200, 120, 3, fill=Color.WHITE)
    can.circle(150, 60, 3, fill=Color.WHITE)
    can.circle(300, 90, 3, fill=Color.WHITE)
else:
    # Day time scene
    can.rect(0, 0, 800, 600, fill="#87CEEB")  # Light blue sky
    can.circle(700, 100, 40, fill=Color.YELLOW)  # Sun
    can.text(400, 50, "Day Drive", size=24, fill=Color.BLACK)

# Draw the road (same for both day and night)
can.rect(0, 450, 800, 150, fill="#444444")  # Dark gray road

# Draw lane markings
for i in range(5):
    x = 50 + i * 180
    can.rect(x, 520, 80, 10, fill=Color.WHITE)

# Draw the car (same for both day and night)
can.rect(200, 400, 300, 100, fill=Color.RED, stroke=Color.BLACK, stroke_width=2)
can.rect(275, 340, 150, 60, fill=Color.RED, stroke=Color.BLACK, stroke_width=2)

# Wheels
can.circle(250, 520, 40, fill=Color.BLACK)
can.circle(450, 520, 40, fill=Color.BLACK)
can.circle(250, 520, 20, fill=Color.GRAY)
can.circle(450, 520, 20, fill=Color.GRAY)

# Headlights (bigger at night to show they're on)
if is_night:
    can.circle(190, 450, 12, fill=Color.YELLOW)
else:
    can.circle(190, 450, 6, fill=Color.YELLOW)

# Show different speed message based on comparison
# Comparison operators: > (greater than), < (less than), == (equal to)
if speed > 120:
    can.text(350, 580, "SPEEDING! Slow down!", size=24, fill=Color.RED)
else:
    can.text(350, 580, "Safe speed", size=24, fill=Color.GREEN)

# Your turn! Try these challenges:
# 1. Change is_night to False and see the scene change
# 2. Change the speed value and see the message change
# 3. Add more conditional elements (traffic lights, weather)
# 4. Try adding elif for a third condition (morning/afternoon/night)

can
