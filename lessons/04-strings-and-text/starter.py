from sketchpy.shapes import Canvas, Color, CreativeGardenPalette, CalmOasisPalette


def main():
    # Label your car parts with text!

    can = Canvas(800, 600)

    # Optional: Show grid for positioning
    can.grid(spacing=50, show_coords=True)

    # String variables - text information about our car
    car_type = "Sports Car"
    car_year = 2024
    max_speed = 200

    # Create an elegant metallic gradient for the car body
    can.linear_gradient("car_body", start=(0, 0), end=(100, 100),
                        colors=[CreativeGardenPalette.CORAL_BLUSH,
                                CreativeGardenPalette.ROSE_QUARTZ,
                                CreativeGardenPalette.PEACH_WHISPER])

    # Draw the car body with gradient
    can.rect(200, 300, 300, 100, fill="gradient:car_body", stroke=Color.BLACK, stroke_width=2)

    # Draw the car roof
    can.rect(275, 240, 150, 60, fill="gradient:car_body", stroke=Color.BLACK, stroke_width=2)

    # Draw wheels
    can.circle(250, 420, 40, fill=Color.BLACK)
    can.circle(450, 420, 40, fill=Color.BLACK)

    # Draw wheel rims with elegant silver
    can.circle(250, 420, 20, fill=CalmOasisPalette.MIST_GRAY)
    can.circle(450, 420, 20, fill=CalmOasisPalette.MIST_GRAY)

    # Draw windows with subtle tint
    can.rect(285, 250, 60, 40, fill=CalmOasisPalette.POWDER_BLUE)
    can.rect(355, 250, 60, 40, fill=CalmOasisPalette.POWDER_BLUE)

    # Add text labels using f-strings to combine text and numbers
    # f-strings let you put variables inside curly braces {} in a string
    can.text(350, 220, f"{car_type} ({car_year})", size=20, fill=Color.BLACK)
    can.text(350, 480, f"Top Speed: {max_speed} km/h", size=16, fill=CalmOasisPalette.MIST_GRAY)

    # Label different car parts
    can.text(275, 280, "Windows", size=12, fill=Color.BLACK)
    can.text(350, 350, "Body", size=14, fill=Color.WHITE)
    can.text(250, 440, "Wheels", size=12, fill=Color.WHITE)

    # Your turn! Try these challenges:
    # 1. Add more car details (make, model, color name)
    # 2. Change the string variables and see the text update
    # 3. Add labels for more car parts (doors, headlights, etc.)
    # 4. Create a "specification sheet" below the car with 5+ details

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-04.svg')
