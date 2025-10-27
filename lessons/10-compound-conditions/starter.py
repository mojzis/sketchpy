# Smart Traffic System - Learn Compound Conditions!
# Concepts: and, or, not operators for complex logic

# Traffic system variables
time_of_day = "morning"
is_weekend = True
traffic_level = 75

can = Canvas(800, 600)

# Optional grid for learning coordinates
can.grid(spacing=50, show_coords=True)

# Complex conditions determine traffic message and car color
if time_of_day == "morning" and is_weekend:
    # Both conditions must be true
    can.text(400, 100, "Leisure Drive - Enjoy the ride!", size=24, fill=Color.BLUE)
    car_color = Color.BLUE
    message = "Light traffic"
elif traffic_level > 70 or time_of_day == "evening":
    # Either condition being true triggers this
    can.text(400, 100, "Rush Hour! Heavy traffic ahead", size=24, fill=Color.RED)
    car_color = Color.GRAY
    message = "Heavy traffic"
else:
    # Neither special condition applies
    can.text(400, 100, "Normal Traffic - Smooth sailing", size=24, fill=Color.GREEN)
    car_color = Color.GREEN
    message = "Normal traffic"

# Display traffic info
can.text(400, 150, f"Time: {time_of_day} | Weekend: {is_weekend} | Level: {traffic_level}%",
         size=16, fill=Color.BLACK)
can.text(400, 180, f"Status: {message}", size=18, fill=car_color)

# Draw car with determined color
can.rect(300, 300, 200, 100, fill=car_color, stroke=Color.BLACK, stroke_width=2)
can.rect(340, 260, 120, 40, fill=car_color, stroke=Color.BLACK, stroke_width=2)  # Roof

# Draw wheels
can.circle(340, 410, 30, fill=Color.BLACK)
can.circle(460, 410, 30, fill=Color.BLACK)
can.circle(340, 410, 15, fill=Color.GRAY)  # Hubcaps
can.circle(460, 410, 15, fill=Color.GRAY)

# Windows
can.rect(350, 270, 40, 25, fill="#87CEEB", stroke=Color.BLACK)  # Sky blue
can.rect(410, 270, 40, 25, fill="#87CEEB", stroke=Color.BLACK)

# Try changing the variables at the top to see different results!
# - Change time_of_day to "evening" or "afternoon"
# - Change is_weekend to False
# - Change traffic_level to different numbers (0-100)
# - Add your own conditions with 'not' operator!

can
