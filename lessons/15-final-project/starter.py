# Lesson 15: Final Project - Complete City Traffic Scene
# Integrate all concepts: functions, loops, conditionals, lists, dictionaries

can = Canvas(800, 600)

# Optional: Show grid for planning (comment out when done)
# can.grid(spacing=50, show_coords=True)


# ============ BACKGROUND FUNCTIONS ============

def draw_sky(canvas):
    """Draw a gradient-like sky using multiple rectangles."""
    # Top part (darker blue)
    canvas.rect(0, 0, 800, 100, fill=CalmOasisPalette.POWDER_BLUE)
    # Middle part (lighter blue)
    canvas.rect(0, 100, 800, 100, fill=CalmOasisPalette.SKY_BLUE)


def draw_buildings(canvas):
    """Draw a city skyline with multiple buildings."""
    # Building 1: Tall office building
    canvas.rect(50, 80, 120, 120, fill=Color.GRAY)
    # Windows (using nested loops for grid pattern)
    for row in range(4):
        for col in range(3):
            canvas.rect(70 + col * 30, 100 + row * 25, 15, 18, fill=Color.YELLOW)

    # Building 2: Medium building
    canvas.rect(200, 120, 90, 80, fill=Color.GRAY)
    for row in range(3):
        for col in range(2):
            canvas.rect(215 + col * 30, 135 + row * 20, 15, 15, fill=Color.YELLOW)

    # Building 3: Short wide building
    canvas.rect(320, 150, 140, 50, fill=Color.SILVER)
    for i in range(5):
        canvas.rect(335 + i * 25, 165, 15, 15, fill=Color.YELLOW)

    # Building 4: Another tall building
    canvas.rect(500, 100, 100, 100, fill=Color.GRAY)
    for row in range(4):
        for col in range(2):
            canvas.rect(520 + col * 30, 115 + row * 22, 15, 15, fill=Color.YELLOW)


def draw_road(canvas):
    """Draw a multi-lane road with markings."""
    # Road surface
    canvas.rect(0, 200, 800, 200, fill=Color.GRAY)

    # Yellow center line (dashed)
    for i in range(10):
        canvas.rect(i * 80 + 10, 295, 40, 10, fill=Color.YELLOW)

    # White lane dividers (dashed)
    for i in range(10):
        canvas.rect(i * 80 + 10, 245, 40, 5, fill=Color.WHITE)
        canvas.rect(i * 80 + 10, 345, 40, 5, fill=Color.WHITE)


def draw_grass(canvas):
    """Draw grass/ground area at the bottom."""
    canvas.rect(0, 400, 800, 200, fill=CreativeGardenPalette.MINT_CREAM)


# ============ CAR FUNCTIONS ============

def draw_sedan(canvas, x, y, color):
    """Draw a sedan-style car at the given position."""
    # Car body
    canvas.rect(x, y, 150, 70, fill=color)

    # Roof
    canvas.rect(x + 30, y - 30, 90, 30, fill=color)

    # Windows
    canvas.rect(x + 35, y - 25, 35, 20, fill=CalmOasisPalette.SKY_BLUE)
    canvas.rect(x + 80, y - 25, 35, 20, fill=CalmOasisPalette.SKY_BLUE)

    # Wheels
    canvas.circle(x + 30, y + 80, 15, fill=Color.BLACK)
    canvas.circle(x + 120, y + 80, 15, fill=Color.BLACK)


def draw_truck(canvas, x, y, color):
    """Draw a truck at the given position."""
    # Cargo area
    canvas.rect(x + 60, y - 20, 140, 90, fill=color)

    # Cab
    canvas.rect(x, y + 20, 70, 50, fill=color)

    # Cab window
    canvas.rect(x + 10, y + 25, 45, 30, fill=CalmOasisPalette.SKY_BLUE)

    # Wheels
    canvas.circle(x + 30, y + 80, 18, fill=Color.BLACK)
    canvas.circle(x + 110, y + 80, 18, fill=Color.BLACK)
    canvas.circle(x + 170, y + 80, 18, fill=Color.BLACK)


def draw_compact_car(canvas, x, y, color):
    """Draw a small compact car."""
    # Body
    canvas.rect(x, y, 100, 60, fill=color)

    # Roof
    canvas.rect(x + 20, y - 25, 60, 25, fill=color)

    # Windows
    canvas.rect(x + 25, y - 20, 22, 15, fill=CalmOasisPalette.SKY_BLUE)
    canvas.rect(x + 53, y - 20, 22, 15, fill=CalmOasisPalette.SKY_BLUE)

    # Wheels
    canvas.circle(x + 20, y + 68, 12, fill=Color.BLACK)
    canvas.circle(x + 80, y + 68, 12, fill=Color.BLACK)


def draw_traffic_light(canvas, x, y, active_light):
    """Draw a traffic light. active_light can be 'red', 'yellow', or 'green'."""
    # Pole
    canvas.rect(x - 5, y, 10, 100, fill=Color.GRAY)

    # Light housing
    canvas.rect(x - 20, y - 100, 40, 100, fill=Color.BLACK)

    # Lights (conditionally colored based on active state)
    if active_light == 'red':
        canvas.circle(x, y - 75, 12, fill=Color.RED)
    else:
        canvas.circle(x, y - 75, 12, fill=Color.GRAY)

    if active_light == 'yellow':
        canvas.circle(x, y - 50, 12, fill=Color.YELLOW)
    else:
        canvas.circle(x, y - 50, 12, fill=Color.GRAY)

    if active_light == 'green':
        canvas.circle(x, y - 25, 12, fill=Color.GREEN)
    else:
        canvas.circle(x, y - 25, 12, fill=Color.GRAY)


# ============ DRAW THE COMPLETE SCENE ============

# Draw background elements (order matters - back to front)
draw_sky(can)
draw_buildings(can)
draw_road(can)
draw_grass(can)

# Add traffic lights
draw_traffic_light(can, 100, 200, 'red')
draw_traffic_light(can, 700, 200, 'green')

# Define vehicles in scene using a list of dictionaries
# This data structure makes it easy to manage multiple objects
vehicles = [
    {'type': 'sedan', 'x': 50, 'y': 230, 'color': Color.RED},
    {'type': 'truck', 'x': 250, 'y': 280, 'color': Color.BLUE},
    {'type': 'compact', 'x': 520, 'y': 225, 'color': CreativeGardenPalette.BUTTER_YELLOW},
    {'type': 'sedan', 'x': 600, 'y': 330, 'color': Color.GREEN},
]

# Draw all vehicles using conditional logic
for vehicle in vehicles:
    if vehicle['type'] == 'sedan':
        draw_sedan(can, vehicle['x'], vehicle['y'], vehicle['color'])
    elif vehicle['type'] == 'truck':
        draw_truck(can, vehicle['x'], vehicle['y'], vehicle['color'])
    elif vehicle['type'] == 'compact':
        draw_compact_car(can, vehicle['x'], vehicle['y'], vehicle['color'])

# Add some trees in the grass area using a loop
for i in range(5):
    tree_x = 100 + i * 150
    # Tree trunk
    can.rect(tree_x - 10, 450, 20, 60, fill=Color.BROWN)
    # Tree foliage (simple circle)
    can.circle(tree_x, 440, 40, fill=CreativeGardenPalette.HONEYDEW)

# Challenge: Add more elements!
# - More vehicles with different positions
# - Clouds in the sky
# - People walking on the sidewalk
# - More detailed buildings
# - Street signs

can
