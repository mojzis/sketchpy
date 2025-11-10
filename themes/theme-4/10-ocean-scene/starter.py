from sketchpy import Canvas, OceanPalette, OceanShapes

def main():
    can = Canvas(800, 600)
    ocean = OceanShapes(can)

    # YOUR FINAL PROJECT! Create a complete ocean scene
    # Use all your skills: variables, loops, lists, dictionaries

    # Ocean floor: seaweed forest
    for i in range(8):
        x = 50 + i * 100
        height = 120 + (i % 3) * 30  # Varying heights
        ocean.seaweed(x, 600, height=height)

    # Background jellyfish (small, high up - look far away)
    background_jellyfish = [
        {"x": 100, "y": 100, "size": 50},
        {"x": 300, "y": 80, "size": 45},
        {"x": 500, "y": 120, "size": 55},
    ]
    for jelly in background_jellyfish:
        ocean.jellyfish(jelly["x"], jelly["y"], size=jelly["size"])

    # Foreground creatures (larger, closer)
    # Add your own octopuses and jellyfish here!
    ocean.octopus(200, 350, size=120, body_color=OceanPalette.CORAL)
    ocean.octopus(550, 380, size=140, body_color=OceanPalette.PURPLE_CORAL)

    # YOUR TURN: Add more creatures to make it amazing!

    return can

if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-10.svg')
