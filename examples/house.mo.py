import marimo

__generated_with = "0.17.2"
app = marimo.App(width="medium")


@app.cell
def _():
    from sketchpy import Canvas, CreativeGardenPalette, CalmOasisPalette

    can = Canvas(800, 600)

    # Sky background (gradient effect with two rectangles)
    can.rect(0, 0, 800, 300, fill=CalmOasisPalette.SKY_BLUE)
    can.rect(0, 300, 800, 100, fill='#B8D8E8')  # lighter transition

    # Ground
    can.rect(0, 400, 800, 200, fill='#9DC183')

    # House body
    house_x, house_y = 250, 250
    house_width, house_height = 300, 200

    can.rect(house_x, house_y, house_width, house_height, 
             fill='#FFF8DC', stroke='#8B7355', stroke_width=3)

    # Roof (triangle using polygon)
    roof_peak_x = house_x + house_width // 2
    roof_peak_y = 150

    can.polygon([
        (house_x - 20, house_y),           # left edge
        (roof_peak_x, roof_peak_y),         # peak
        (house_x + house_width + 20, house_y)  # right edge
    ], fill='#FF9E80', stroke='#8B4513', stroke_width=3)

    # Door
    door_x = house_x + house_width // 2 - 40
    can.rounded_rect(door_x, 350, 80, 100, rx=8,
                     fill='#8B4513', stroke='#000', stroke_width=2)

    # Door knob
    can.circle(door_x + 65, 400, 5, fill='#FFD700', stroke='#000', stroke_width=1)

    # Windows (two squares)
    window_y = 290
    can.rect(290, window_y, 60, 60, 
             fill=CalmOasisPalette.CLOUD_WHITE, stroke='#000', stroke_width=2)
    can.rect(450, window_y, 60, 60, 
             fill=CalmOasisPalette.CLOUD_WHITE, stroke='#000', stroke_width=2)

    # Window panes (cross pattern)
    can.line(320, window_y, 320, window_y + 60, stroke='#000', stroke_width=2)
    can.line(290, window_y + 30, 350, window_y + 30, stroke='#000', stroke_width=2)
    can.line(480, window_y, 480, window_y + 60, stroke='#000', stroke_width=2)
    can.line(450, window_y + 30, 510, window_y + 30, stroke='#000', stroke_width=2)

    # Garden path (small rectangles)
    path_x = door_x + 40
    for i in range(4):
        path_y = 450 + i * 35
        can.rect(path_x - 15, path_y, 30, 25, 
                 fill='#D3C5B0', stroke='#A89C86', stroke_width=1.5)

    # Garden flowers (in front of house)
    flower_positions = [
        {'x': 270, 'y': 475, 'color': CreativeGardenPalette.ROSE_QUARTZ},
        {'x': 320, 'y': 490, 'color': CreativeGardenPalette.BUTTER_YELLOW},
        {'x': 365, 'y': 480, 'color': CreativeGardenPalette.LILAC_DREAM},
        {'x': 435, 'y': 485, 'color': CreativeGardenPalette.PEACH_WHISPER},
        {'x': 480, 'y': 475, 'color': CreativeGardenPalette.ROSE_QUARTZ},
        {'x': 530, 'y': 490, 'color': CreativeGardenPalette.BUTTER_YELLOW},
    ]

    for flower in flower_positions:
        # Stem
        can.line(flower['x'], flower['y'] - 5, flower['x'], flower['y'] + 35, 
                 stroke='#6B8E23', stroke_width=3)
        # Flower head
        can.circle(flower['x'], flower['y'], 12, 
                   fill=flower['color'], stroke='#000', stroke_width=1.5)

    # Sun in corner (simple circle with rays)
    sun_x, sun_y = 680, 120
    can.circle(sun_x, sun_y, 35, fill='#FFE66D', stroke='#FFD700', stroke_width=2)

    # Sun rays (short lines radiating out)
    for angle in range(0, 360, 45):
        import math
        rad = math.radians(angle)
        x1 = sun_x + math.cos(rad) * 45
        y1 = sun_y + math.sin(rad) * 45
        x2 = sun_x + math.cos(rad) * 60
        y2 = sun_y + math.sin(rad) * 60
        can.line(x1, y1, x2, y2, stroke='#FFD700', stroke_width=3)

    can
    return (can,)


@app.cell
def _(can):
    dir(can)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
