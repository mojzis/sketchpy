from sketchpy import Canvas, OceanPalette, OceanShapes

def main():
    can = Canvas(800, 600)
    ocean = OceanShapes(can)

    # Dictionaries: group related data together!
    creatures = [
        {"type": "octopus", "x": 150, "y": 250, "size": 100},
        {"type": "jellyfish", "x": 350, "y": 200, "size": 80},
        {"type": "octopus", "x": 550, "y": 300, "size": 120},
        {"type": "jellyfish", "x": 650, "y": 150, "size": 70}
    ]

    # Loop through and draw based on type
    for creature in creatures:
        if creature["type"] == "octopus":
            ocean.octopus(creature["x"], creature["y"], size=creature["size"])
        elif creature["type"] == "jellyfish":
            ocean.jellyfish(creature["x"], creature["y"], size=creature["size"])

    return can

if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-08.svg')
