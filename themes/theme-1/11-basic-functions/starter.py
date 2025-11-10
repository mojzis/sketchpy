from sketchpy import Canvas, Color, CreativeGardenPalette, CalmOasisPalette


def main():
    # Vehicle Factory - Learn Basic Functions with Groups!
    # Concepts: def, function names, calling functions, code reuse, groups

    can = Canvas(800, 600)

    # Optional grid for learning coordinates
    can.grid(spacing=50, show_coords=True)

    # Create elegant gradients for vehicles
    can.linear_gradient("car_red", start=(0, 0), end=(100, 100),
                        colors=[CreativeGardenPalette.CORAL_BLUSH, CreativeGardenPalette.ROSE_QUARTZ])
    can.linear_gradient("truck_blue", start=(0, 0), end=(100, 100),
                        colors=[CalmOasisPalette.POWDER_BLUE, CalmOasisPalette.PERIWINKLE])

    # Define a function - recipe for drawing a simple car
    def draw_simple_car(canvas):
        """Draw a simple car at a fixed position using groups"""
        with canvas.group("simple_car"):
            # Car body
            canvas.rect(200, 300, 200, 80, fill="gradient:car_red", stroke=Color.BLACK, stroke_width=2)
            # Car roof
            canvas.rect(240, 260, 120, 40, fill="gradient:car_red", stroke=Color.BLACK, stroke_width=2)
            # Wheels
            canvas.circle(250, 390, 25, fill=Color.BLACK)
            canvas.circle(350, 390, 25, fill=Color.BLACK)
            # Hubcaps
            canvas.circle(250, 390, 12, fill=CalmOasisPalette.MIST_GRAY)
            canvas.circle(350, 390, 12, fill=CalmOasisPalette.MIST_GRAY)
            # Windows
            canvas.rect(250, 270, 35, 25, fill=CalmOasisPalette.POWDER_BLUE, stroke=Color.BLACK)
            canvas.rect(310, 270, 35, 25, fill=CalmOasisPalette.POWDER_BLUE, stroke=Color.BLACK)

    def draw_truck(canvas):
        """Draw a truck at a fixed position using groups"""
        with canvas.group("truck"):
            # Truck cargo bed
            canvas.rect(450, 280, 250, 120, fill="gradient:truck_blue", stroke=Color.BLACK, stroke_width=2)
            # Truck cab
            canvas.rect(650, 250, 80, 150, fill="gradient:truck_blue", stroke=Color.BLACK, stroke_width=2)
            # Wheels
            canvas.circle(500, 410, 30, fill=Color.BLACK)
            canvas.circle(630, 410, 30, fill=Color.BLACK)
            canvas.circle(680, 410, 30, fill=Color.BLACK)
            # Hubcaps
            canvas.circle(500, 410, 15, fill=CalmOasisPalette.MIST_GRAY)
            canvas.circle(630, 410, 15, fill=CalmOasisPalette.MIST_GRAY)
            canvas.circle(680, 410, 15, fill=CalmOasisPalette.MIST_GRAY)
            # Cab window
            canvas.rect(660, 260, 60, 40, fill=CalmOasisPalette.POWDER_BLUE, stroke=Color.BLACK)

    # Add labels
    can.text(300, 240, "Simple Car", size=18, fill=CreativeGardenPalette.ROSE_QUARTZ)
    can.text(600, 220, "Truck", size=18, fill=CalmOasisPalette.PERIWINKLE)

    # Call functions to use them - this executes the code inside!
    draw_simple_car(can)  # Draw the car
    draw_truck(can)       # Draw the truck

    # Try this:
    # 1. Add a draw_sports_car() function
    # 2. Call your new function below
    # 3. Functions let you reuse code without copying it!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-11.svg')
