from sketchpy import Canvas, CreativeGardenPalette


def main():
    # Final project: Complete garden scene using all concepts!

    can = Canvas(800, 600)

    def draw_sky(can, is_day=True):
        """Draw sky background - different colors for day vs night"""
        if is_day:
            can.rect(0, 0, 800, 350, fill=CreativeGardenPalette.SKY_BREEZE)
        else:
            can.rect(0, 0, 800, 350, fill='#2C3E50')

    def draw_ground(can):
        """Draw ground"""
        can.rect(0, 350, 800, 250, fill=CreativeGardenPalette.MINT_CREAM)

    def draw_sun(can, x, y):
        """Draw a sun"""
        can.circle(x, y, 50,
                   fill=CreativeGardenPalette.BUTTER_YELLOW,
                   stroke=CreativeGardenPalette.LEMON_CHIFFON,
                   stroke_width=3)

    def calculate_flower_parts(size):
        """Calculate proportional flower dimensions from size"""
        center_size = int(size * 0.7)
        petal_size = size
        petal_distance = int(size * 1.4)
        return center_size, petal_size, petal_distance

    def draw_flower(can, x, y, size, petal_color, center_color):
        """Draw a complete flower with specified properties"""
        center_size, petal_size, petal_distance = calculate_flower_parts(size)

        # Create radial gradients for depth
        can.radial_gradient("petal_grad", center=(50, 50), radius=60,
                            colors=['#FFFFFF', petal_color])
        can.radial_gradient("center_grad", center=(50, 50), radius=60,
                            colors=[center_color, '#F4E08A'])

        # Draw 4 petals with symmetric layering (FIRST - middle layer)
        can.circle(x, y - petal_distance, petal_size, fill='gradient:petal_grad',
                   stroke='#000', stroke_width=1.5)
        can.circle(x, y + petal_distance, petal_size, fill='gradient:petal_grad',
                   stroke='#000', stroke_width=1.5)

        can.circle(x + petal_distance, y, petal_size, fill='gradient:petal_grad',
                   stroke='#000', stroke_width=1.5)
        can.circle(x - petal_distance, y, petal_size, fill='gradient:petal_grad',
                   stroke='#000', stroke_width=1.5)

        # Draw flower center (LAST - top layer)
        can.circle(x, y, center_size, fill='gradient:center_grad',
                   stroke='#000', stroke_width=2)

    def draw_stem(can, x, y, height):
        """Draw a flower stem"""
        can.line(x, y, x, y + height,
                 stroke=CreativeGardenPalette.MINT_CREAM,
                 stroke_width=6)

    def draw_butterfly(can, x, y, wing_color):
        """Draw a butterfly"""
        # Body
        can.ellipse(x, y, 12, 40,
                    fill=CreativeGardenPalette.LILAC_DREAM,
                    stroke='#000', stroke_width=2)

        # Wings
        can.circle(x - 20, y - 10, 18, fill=wing_color,
                   stroke='#000', stroke_width=1.5)
        can.circle(x + 20, y - 10, 18, fill=wing_color,
                   stroke='#000', stroke_width=1.5)
        can.circle(x - 18, y + 10, 15, fill=wing_color,
                   stroke='#000', stroke_width=1.5)
        can.circle(x + 18, y + 10, 15, fill=wing_color,
                   stroke='#000', stroke_width=1.5)

    def create_garden_data():
        """Define garden as a data structure

        Each flower is a dictionary with all its properties.
        This separates the garden design from the drawing code!
        """
        return [
            {
                "x": 120,
                "y": 450,
                "size": 20,
                "petal_color": CreativeGardenPalette.ROSE_QUARTZ,
                "center_color": CreativeGardenPalette.BUTTER_YELLOW
            },
            {
                "x": 250,
                "y": 450,
                "size": 24,
                "petal_color": CreativeGardenPalette.LILAC_DREAM,
                "center_color": CreativeGardenPalette.LEMON_CHIFFON
            },
            {
                "x": 380,
                "y": 450,
                "size": 18,
                "petal_color": CreativeGardenPalette.PEACH_WHISPER,
                "center_color": CreativeGardenPalette.CORAL_BLUSH
            },
            {
                "x": 510,
                "y": 450,
                "size": 22,
                "petal_color": CreativeGardenPalette.MISTY_MAUVE,
                "center_color": CreativeGardenPalette.BUTTER_YELLOW
            },
            {
                "x": 640,
                "y": 450,
                "size": 20,
                "petal_color": CreativeGardenPalette.CORAL_BLUSH,
                "center_color": CreativeGardenPalette.LEMON_CHIFFON
            }
        ]

    def draw_garden(can, garden_data):
        """Draw all flowers from data structure"""
        for flower in garden_data:
            # Draw stem first (back layer)
            draw_stem(can, flower["x"], flower["y"], 80)

            # Draw flower on top
            draw_flower(can,
                        flower["x"],
                        flower["y"],
                        flower["size"],
                        flower["petal_color"],
                        flower["center_color"])

    # Draw a coordinate grid to help with positioning
    can.grid(spacing=50, show_coords=True)

    # Layer 1: Background (sky and ground)
    draw_sky(can, is_day=True)
    draw_ground(can)

    # Layer 2: Sun
    draw_sun(can, 700, 100)

    # Layer 3: Garden (flowers with stems)
    garden = create_garden_data()
    draw_garden(can, garden)

    # Layer 4: Butterflies (foreground)
    draw_butterfly(can, 300, 200, CreativeGardenPalette.PEACH_WHISPER)
    draw_butterfly(can, 500, 250, CreativeGardenPalette.ROSE_QUARTZ)

    # Add title
    can.text(400, 50, "My Garden", 36, fill='#333')

    # Your turn! Add more elements, create your own unique garden!
    # Ideas: clouds, grass tufts, a path, more butterflies, different times of day

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-15.svg')
