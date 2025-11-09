from sketchpy import Canvas, OceanPalette, OceanShapes

def main():
    can = Canvas(800, 600)
    ocean = OceanShapes(can)

    # Draw a row of seaweed using a loop!
    # This replaces 5 lines with just 3 lines
    for i in range(5):
        x = 100 + i * 100  # Calculate position: 100, 200, 300, 400, 500
        ocean.seaweed(x, 600, height=150, color=OceanPalette.KELP_GREEN)

    # The loop runs 5 times:
    # i=0: x = 100 + 0*100 = 100
    # i=1: x = 100 + 1*100 = 200
    # i=2: x = 100 + 2*100 = 300
    # i=3: x = 100 + 3*100 = 400
    # i=4: x = 100 + 4*100 = 500

    return can

if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-04.svg')
