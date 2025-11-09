from sketchpy.shapes import Canvas, OceanPalette, OceanShapes

def main():
    can = Canvas(800, 600)
    ocean = OceanShapes(can)

    # YOUR TURN! Create lists for a varied scene
    jellyfish_sizes = [60, 80, 70, 90, 75]

    # Draw jellyfish using your list
    for i, size in enumerate(jellyfish_sizes):
        x = 80 + i * 140
        ocean.jellyfish(x, 200, size=size)

    # CHALLENGE: Add a list of seaweed heights!
    # seaweed_heights = [120, 150, 140, 160, 130]

    return can

if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-07.svg')
