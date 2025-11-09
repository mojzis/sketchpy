from sketchpy.shapes import Canvas, OceanPalette, OceanShapes

def main():
    can = Canvas(800, 600)
    ocean = OceanShapes(can)

    # YOUR TURN! Build your ocean ecosystem
    my_ocean = [
        {"type": "seaweed", "x": 100, "y": 600, "height": 150},
        {"type": "octopus", "x": 200, "y": 300, "size": 100},
        {"type": "jellyfish", "x": 400, "y": 200, "size": 80},
        # Add more creatures here!
    ]

    # Draw your ecosystem
    for creature in my_ocean:
        if creature["type"] == "octopus":
            ocean.octopus(creature["x"], creature["y"], size=creature["size"])
        elif creature["type"] == "jellyfish":
            ocean.jellyfish(creature["x"], creature["y"], size=creature["size"])
        elif creature["type"] == "seaweed":
            ocean.seaweed(creature["x"], creature["y"], height=creature["height"])

    return can

if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-09.svg')
