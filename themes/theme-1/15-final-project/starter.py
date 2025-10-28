from sketchpy.shapes import Canvas, Color, CreativeGardenPalette, CalmOasisPalette


def main():
    # Lesson 15: Final Project - Complete City Traffic Scene with Gradients & Groups
    # Integrate ALL concepts: functions, loops, conditionals, lists, dictionaries, gradients, groups

    can = Canvas(800, 600)

    # Optional: Show grid for planning (comment out when done)
    # can.grid(spacing=50, show_coords=True)

    # ============ CREATE ELEGANT GRADIENTS ============

    # Sky gradient
    can.linear_gradient("sky", start=(0, 0), end=(0, 100),
                        colors=[CalmOasisPalette.POWDER_BLUE, CalmOasisPalette.SKY_BLUE, CalmOasisPalette.SOFT_AQUA])

    # Building gradients
    can.linear_gradient("building", start=(0, 0), end=(100, 100),
                        colors=[CalmOasisPalette.MIST_GRAY, CalmOasisPalette.MIST_GRAY])

    # Window glow gradient
    can.radial_gradient("window", center=(50, 50), radius=60,
                        colors=[CreativeGardenPalette.BUTTER_YELLOW, CreativeGardenPalette.LEMON_CHIFFON])

    # Car gradients
    can.linear_gradient("sedan_red", start=(0, 0), end=(100, 100),
                        colors=[CreativeGardenPalette.CORAL_BLUSH, CreativeGardenPalette.ROSE_QUARTZ])
    can.linear_gradient("truck_blue", start=(0, 0), end=(100, 100),
                        colors=[CalmOasisPalette.POWDER_BLUE, CalmOasisPalette.PERIWINKLE])
    can.linear_gradient("compact_yellow", start=(0, 0), end=(100, 100),
                        colors=[CreativeGardenPalette.BUTTER_YELLOW, CreativeGardenPalette.LEMON_CHIFFON])
    can.linear_gradient("sedan_green", start=(0, 0), end=(100, 100),
                        colors=[CalmOasisPalette.MINT_FRESH, CalmOasisPalette.SAGE_GREEN])

    # Traffic light glow
    can.radial_gradient("light_glow", center=(50, 50), radius=80,
                        colors=[Color.YELLOW, CreativeGardenPalette.LEMON_CHIFFON])


    # ============ BACKGROUND FUNCTIONS ============

    def draw_sky(canvas):
        """Draw a beautiful gradient sky."""
        canvas.rect(0, 0, 800, 200, fill="gradient:sky")


    def draw_buildings(canvas):
        """Draw a city skyline with grouped buildings using gradients."""
        # Building 1: Tall office building (grouped)
        with canvas.group("building1"):
            canvas.rect(50, 80, 120, 120, fill="gradient:building")
            # Windows with glow gradient
            for row in range(4):
                for col in range(3):
                    canvas.rect(70 + col * 30, 100 + row * 25, 15, 18, fill="gradient:window")

        # Building 2: Medium building (grouped)
        with canvas.group("building2"):
            canvas.rect(200, 120, 90, 80, fill="gradient:building")
            for row in range(3):
                for col in range(2):
                    canvas.rect(215 + col * 30, 135 + row * 20, 15, 15, fill="gradient:window")

        # Building 3: Short wide building (grouped)
        with canvas.group("building3"):
            canvas.rect(320, 150, 140, 50, fill=CalmOasisPalette.MIST_GRAY)
            for i in range(5):
                canvas.rect(335 + i * 25, 165, 15, 15, fill="gradient:window")

        # Building 4: Another tall building (grouped)
        with canvas.group("building4"):
            canvas.rect(500, 100, 100, 100, fill="gradient:building")
            for row in range(4):
                for col in range(2):
                    canvas.rect(520 + col * 30, 115 + row * 22, 15, 15, fill="gradient:window")


    def draw_road(canvas):
        """Draw a multi-lane road with markings."""
        # Road surface
        canvas.rect(0, 200, 800, 200, fill=CalmOasisPalette.MIST_GRAY)

        # Yellow center line (dashed)
        for i in range(10):
            canvas.rect(i * 80 + 10, 295, 40, 10, fill=CreativeGardenPalette.BUTTER_YELLOW)

        # White lane dividers (dashed)
        for i in range(10):
            canvas.rect(i * 80 + 10, 245, 40, 5, fill=Color.WHITE)
            canvas.rect(i * 80 + 10, 345, 40, 5, fill=Color.WHITE)


    def draw_grass(canvas):
        """Draw grass/ground area at the bottom."""
        canvas.rect(0, 400, 800, 200, fill=CreativeGardenPalette.MINT_CREAM)


    # ============ CAR FUNCTIONS WITH GRADIENTS ============

    def draw_sedan(canvas, x, y, gradient):
        """Draw a sedan-style car with gradient fill."""
        # Car body
        canvas.rect(x, y, 150, 70, fill=gradient)

        # Roof
        canvas.rect(x + 30, y - 30, 90, 30, fill=gradient)

        # Windows
        canvas.rect(x + 35, y - 25, 35, 20, fill=CalmOasisPalette.POWDER_BLUE)
        canvas.rect(x + 80, y - 25, 35, 20, fill=CalmOasisPalette.POWDER_BLUE)

        # Wheels with elegant rims
        canvas.circle(x + 30, y + 80, 15, fill=Color.BLACK)
        canvas.circle(x + 120, y + 80, 15, fill=Color.BLACK)
        canvas.circle(x + 30, y + 80, 8, fill=CalmOasisPalette.MIST_GRAY)
        canvas.circle(x + 120, y + 80, 8, fill=CalmOasisPalette.MIST_GRAY)


    def draw_truck(canvas, x, y, gradient):
        """Draw a truck with gradient fill."""
        # Cargo area
        canvas.rect(x + 60, y - 20, 140, 90, fill=gradient)

        # Cab
        canvas.rect(x, y + 20, 70, 50, fill=gradient)

        # Cab window
        canvas.rect(x + 10, y + 25, 45, 30, fill=CalmOasisPalette.POWDER_BLUE)

        # Wheels with elegant rims
        canvas.circle(x + 30, y + 80, 18, fill=Color.BLACK)
        canvas.circle(x + 110, y + 80, 18, fill=Color.BLACK)
        canvas.circle(x + 170, y + 80, 18, fill=Color.BLACK)
        canvas.circle(x + 30, y + 80, 9, fill=CalmOasisPalette.MIST_GRAY)
        canvas.circle(x + 110, y + 80, 9, fill=CalmOasisPalette.MIST_GRAY)
        canvas.circle(x + 170, y + 80, 9, fill=CalmOasisPalette.MIST_GRAY)


    def draw_compact_car(canvas, x, y, gradient):
        """Draw a small compact car with gradient."""
        # Body
        canvas.rect(x, y, 100, 60, fill=gradient)

        # Roof
        canvas.rect(x + 20, y - 25, 60, 25, fill=gradient)

        # Windows
        canvas.rect(x + 25, y - 20, 22, 15, fill=CalmOasisPalette.POWDER_BLUE)
        canvas.rect(x + 53, y - 20, 22, 15, fill=CalmOasisPalette.POWDER_BLUE)

        # Wheels with elegant rims
        canvas.circle(x + 20, y + 68, 12, fill=Color.BLACK)
        canvas.circle(x + 80, y + 68, 12, fill=Color.BLACK)
        canvas.circle(x + 20, y + 68, 6, fill=CalmOasisPalette.MIST_GRAY)
        canvas.circle(x + 80, y + 68, 6, fill=CalmOasisPalette.MIST_GRAY)


    def draw_traffic_light(canvas, x, y, active_light):
        """Draw a traffic light with glowing active light."""
        # Pole
        canvas.rect(x - 5, y, 10, 100, fill=CalmOasisPalette.MIST_GRAY)

        # Light housing
        canvas.rect(x - 20, y - 100, 40, 100, fill=Color.BLACK)

        # Lights (conditionally colored with glow effect on active state)
        if active_light == 'red':
            canvas.circle(x, y - 75, 12, fill=CreativeGardenPalette.CORAL_BLUSH)
        else:
            canvas.circle(x, y - 75, 12, fill=CalmOasisPalette.MIST_GRAY)

        if active_light == 'yellow':
            canvas.circle(x, y - 50, 12, fill="gradient:light_glow")
        else:
            canvas.circle(x, y - 50, 12, fill=CalmOasisPalette.MIST_GRAY)

        if active_light == 'green':
            canvas.circle(x, y - 25, 12, fill=CalmOasisPalette.MINT_FRESH)
        else:
            canvas.circle(x, y - 25, 12, fill=CalmOasisPalette.MIST_GRAY)


    # ============ DRAW THE COMPLETE SCENE ============

    # Draw background elements (order matters - back to front)
    draw_sky(can)
    draw_buildings(can)
    draw_road(can)
    draw_grass(can)

    # Add traffic lights
    draw_traffic_light(can, 100, 200, 'red')
    draw_traffic_light(can, 700, 200, 'green')

    # Define vehicles in scene using a list of dictionaries with gradients
    # This data structure makes it easy to manage multiple objects
    vehicles = [
        {'type': 'sedan', 'x': 50, 'y': 230, 'gradient': 'gradient:sedan_red'},
        {'type': 'truck', 'x': 250, 'y': 280, 'gradient': 'gradient:truck_blue'},
        {'type': 'compact', 'x': 520, 'y': 225, 'gradient': 'gradient:compact_yellow'},
        {'type': 'sedan', 'x': 600, 'y': 330, 'gradient': 'gradient:sedan_green'},
    ]

    # Draw all vehicles using conditional logic with groups for organization
    for i, vehicle in enumerate(vehicles):
        with can.group(f"vehicle_{i}"):
            if vehicle['type'] == 'sedan':
                draw_sedan(can, vehicle['x'], vehicle['y'], vehicle['gradient'])
            elif vehicle['type'] == 'truck':
                draw_truck(can, vehicle['x'], vehicle['y'], vehicle['gradient'])
            elif vehicle['type'] == 'compact':
                draw_compact_car(can, vehicle['x'], vehicle['y'], vehicle['gradient'])

    # Create tree gradients
    can.radial_gradient("tree_leaves", center=(50, 50), radius=60,
                        colors=[CreativeGardenPalette.HONEYDEW, CalmOasisPalette.MINT_FRESH])

    # Add some trees in the grass area using a loop with groups
    for i in range(5):
        tree_x = 100 + i * 150
        with can.group(f"tree_{i}"):
            # Tree trunk
            can.rect(tree_x - 10, 450, 20, 60, fill=Color.BROWN)
            # Tree foliage with gradient
            can.circle(tree_x, 440, 40, fill="gradient:tree_leaves")

    # Challenge: Add more elements!
    # - More vehicles with different positions and custom gradients
    # - Clouds in the sky with gradient effects
    # - People walking on the sidewalk
    # - More detailed buildings with grouped elements
    # - Street signs
    # - Try experimenting with radial gradients for sun/moon effects!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-15.svg')
