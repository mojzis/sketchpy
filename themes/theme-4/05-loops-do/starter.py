from sketchpy import Canvas, OceanPalette, OceanShapes

def main():
    can = Canvas(800, 600)
    ocean = OceanShapes(can)

    # YOUR TURN! Create a swarm of jellyfish using a loop
    # TODO: Fill in the blanks below

    for i in range(6):  # Try changing the number!
        x = 50 + i * 120  # Calculate position for each jellyfish
        y = 250            # All at same height (try changing this!)

        # Draw the jellyfish
        ocean.jellyfish(x, y, size=70)

    # CHALLENGE: Make jellyfish grow in size
    # Hint: size = 50 + i * 10

    return can

if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-05.svg')
