from sketchpy.shapes import Canvas, OceanPalette, OceanShapes

def main():
    # Create an ocean canvas
    can = Canvas(800, 600)

    # Create ocean helper (gives us octopus, jellyfish, seaweed!)
    ocean = OceanShapes(can)

    # Draw an octopus! Try changing these numbers:
    ocean.octopus(400, 300, size=120)

    return can

if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-01.svg')
