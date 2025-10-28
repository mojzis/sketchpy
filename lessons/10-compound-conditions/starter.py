from sketchpy.shapes import Canvas, Color, CreativeGardenPalette, CalmOasisPalette


def main():
    # Smart Traffic System - Learn Compound Conditions with Gradients!
    # Concepts: and, or, not operators for complex logic

    # Traffic system variables
    time_of_day = "morning"
    is_weekend = True
    traffic_level = 75

    can = Canvas(800, 600)

    # Optional grid for learning coordinates
    can.grid(spacing=50, show_coords=True)

    # Create elegant gradients for different conditions
    can.linear_gradient("leisure_sky", start=(0, 0), end=(0, 100),
                        colors=[CalmOasisPalette.POWDER_BLUE, CalmOasisPalette.SKY_BLUE])
    can.linear_gradient("rush_sky", start=(0, 0), end=(0, 100),
                        colors=[CreativeGardenPalette.CORAL_BLUSH, CreativeGardenPalette.PEACH_WHISPER])
    can.linear_gradient("normal_sky", start=(0, 0), end=(0, 100),
                        colors=[CalmOasisPalette.MINT_FRESH, CalmOasisPalette.SAGE_GREEN])

    # Complex conditions determine traffic message and car color
    if time_of_day == "morning" and is_weekend:
        # Both conditions must be true - Leisure mode
        can.rect(0, 0, 800, 600, fill="gradient:leisure_sky")
        can.text(400, 100, "Leisure Drive - Enjoy the ride!", size=24, fill=CalmOasisPalette.PERIWINKLE)
        car_gradient = "leisure_car"
        can.linear_gradient(car_gradient, start=(0, 0), end=(100, 100),
                            colors=[CalmOasisPalette.POWDER_BLUE, CalmOasisPalette.PERIWINKLE])
        message = "Light traffic"
    elif traffic_level > 70 or time_of_day == "evening":
        # Either condition being true triggers this - Rush hour
        can.rect(0, 0, 800, 600, fill="gradient:rush_sky")
        can.text(400, 100, "Rush Hour! Heavy traffic ahead", size=24, fill=CreativeGardenPalette.CORAL_BLUSH)
        car_gradient = "rush_car"
        can.linear_gradient(car_gradient, start=(0, 0), end=(100, 100),
                            colors=[CalmOasisPalette.MIST_GRAY, CalmOasisPalette.CLOUD_WHITE])
        message = "Heavy traffic"
    else:
        # Neither special condition applies - Normal traffic
        can.rect(0, 0, 800, 600, fill="gradient:normal_sky")
        can.text(400, 100, "Normal Traffic - Smooth sailing", size=24, fill=CalmOasisPalette.SAGE_GREEN)
        car_gradient = "normal_car"
        can.linear_gradient(car_gradient, start=(0, 0), end=(100, 100),
                            colors=[CalmOasisPalette.MINT_FRESH, CalmOasisPalette.SAGE_GREEN])
        message = "Normal traffic"

    # Display traffic info
    can.text(400, 150, f"Time: {time_of_day} | Weekend: {is_weekend} | Level: {traffic_level}%",
             size=16, fill=Color.BLACK)
    can.text(400, 180, f"Status: {message}", size=18, fill=Color.BLACK)

    # Draw car with determined gradient
    can.rect(300, 300, 200, 100, fill=f"gradient:{car_gradient}", stroke=Color.BLACK, stroke_width=2)
    can.rect(340, 260, 120, 40, fill=f"gradient:{car_gradient}", stroke=Color.BLACK, stroke_width=2)  # Roof

    # Draw wheels with elegant rims
    can.circle(340, 410, 30, fill=Color.BLACK)
    can.circle(460, 410, 30, fill=Color.BLACK)
    can.circle(340, 410, 15, fill=CalmOasisPalette.MIST_GRAY)  # Hubcaps
    can.circle(460, 410, 15, fill=CalmOasisPalette.MIST_GRAY)

    # Windows with subtle tint
    can.rect(350, 270, 40, 25, fill=CalmOasisPalette.POWDER_BLUE, stroke=Color.BLACK)
    can.rect(410, 270, 40, 25, fill=CalmOasisPalette.POWDER_BLUE, stroke=Color.BLACK)

    # Try changing the variables at the top to see different results!
    # - Change time_of_day to "evening" or "afternoon"
    # - Change is_weekend to False
    # - Change traffic_level to different numbers (0-100)
    # - Add your own conditions with 'not' operator!

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-10.svg')
