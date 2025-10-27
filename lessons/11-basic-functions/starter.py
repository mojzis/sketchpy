# Vehicle Factory - Learn Basic Functions!
# Concepts: def, function names, calling functions, code reuse

from sketchpy.shapes import Canvas, Color

can = Canvas(800, 600)

# Optional grid for learning coordinates
can.grid(spacing=50, show_coords=True)

# Define a function - recipe for drawing a simple car
def draw_simple_car(canvas):
    """Draw a simple car at a fixed position"""
    # Car body
    canvas.rect(200, 300, 200, 80, fill=Color.RED, stroke=Color.BLACK, stroke_width=2)
    # Car roof
    canvas.rect(240, 260, 120, 40, fill=Color.RED, stroke=Color.BLACK, stroke_width=2)
    # Wheels
    canvas.circle(250, 390, 25, fill=Color.BLACK)
    canvas.circle(350, 390, 25, fill=Color.BLACK)
    # Hubcaps
    canvas.circle(250, 390, 12, fill=Color.GRAY)
    canvas.circle(350, 390, 12, fill=Color.GRAY)
    # Windows
    canvas.rect(250, 270, 35, 25, fill="#87CEEB", stroke=Color.BLACK)  # Sky blue
    canvas.rect(310, 270, 35, 25, fill="#87CEEB", stroke=Color.BLACK)

def draw_truck(canvas):
    """Draw a truck at a fixed position"""
    # Truck cargo bed
    canvas.rect(450, 280, 250, 120, fill=Color.BLUE, stroke=Color.BLACK, stroke_width=2)
    # Truck cab
    canvas.rect(650, 250, 80, 150, fill=Color.BLUE, stroke=Color.BLACK, stroke_width=2)
    # Wheels
    canvas.circle(500, 410, 30, fill=Color.BLACK)
    canvas.circle(630, 410, 30, fill=Color.BLACK)
    canvas.circle(680, 410, 30, fill=Color.BLACK)
    # Hubcaps
    canvas.circle(500, 410, 15, fill=Color.GRAY)
    canvas.circle(630, 410, 15, fill=Color.GRAY)
    canvas.circle(680, 410, 15, fill=Color.GRAY)
    # Cab window
    canvas.rect(660, 260, 60, 40, fill="#87CEEB", stroke=Color.BLACK)  # Sky blue

# Add labels
can.text(300, 240, "Simple Car", size=18, fill=Color.RED)
can.text(600, 220, "Truck", size=18, fill=Color.BLUE)

# Call functions to use them - this executes the code inside!
draw_simple_car(can)  # Draw the car
draw_truck(can)       # Draw the truck

# Try this:
# 1. Add a draw_sports_car() function
# 2. Call your new function below
# 3. Functions let you reuse code without copying it!

can
