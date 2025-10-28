# Final Project: Complete Garden Scene

## What You'll Learn
- **Integration:** Combine all concepts from previous lessons
- **Drawing:** Create a complete, layered garden scene with multiple elements

## Project Overview

This is your chance to bring together everything you've learned:
- Functions for organization
- Nested loops for patterns
- Conditionals for variation
- Lists and dictionaries for data
- Return values for calculations
- Parameters for flexibility

Let's build a complete garden scene!

## Planning Your Scene

Before coding, plan your layers (back to front):
1. **Background:** Sky and ground
2. **Background elements:** Sun/moon, clouds
3. **Mid-ground:** Flowers, grass
4. **Foreground:** Butterflies, labels

Drawing order matters - things drawn later appear on top!

## Instructions

### Step 1: Set Up the Scene Structure

```python
from sketchpy.shapes import Canvas, CreativeGardenPalette


def draw_sky(can, is_day=True):
    """Draw sky background"""
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


def main():
    can = Canvas(800, 600)
    can.grid(spacing=50, show_coords=True)

    # Layer 1: Background
    draw_sky(can, is_day=True)
    draw_ground(can)

    # Layer 2: Sun
    draw_sun(can, 700, 100)

    return can
```

**Try it:** Add a `draw_cloud()` function and place a few clouds in the sky.

### Step 2: Add Flower Functions

```python
def calculate_flower_parts(size):
    """Calculate flower dimensions"""
    center_size = int(size * 0.7)
    petal_size = size
    petal_distance = int(size * 1.4)
    return center_size, petal_size, petal_distance


def draw_flower(can, x, y, size, petal_color, center_color):
    """Draw a complete flower"""
    center_size, petal_size, petal_distance = calculate_flower_parts(size)

    # Center
    can.circle(x, y, center_size, fill=center_color,
               stroke='#000', stroke_width=2)

    # Petals
    can.circle(x, y - petal_distance, petal_size, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x + petal_distance, y, petal_size, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x, y + petal_distance, petal_size, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x - petal_distance, y, petal_size, fill=petal_color,
               stroke='#000', stroke_width=1.5)


def draw_stem(can, x, y, height):
    """Draw a flower stem"""
    can.line(x, y, x, y + height,
             stroke=CreativeGardenPalette.MINT_CREAM,
             stroke_width=6)
```

### Step 3: Create a Garden Using Data

```python
def create_garden_data():
    """Define garden as data structure"""
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
    """Draw all flowers from data"""
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


def main():
    can = Canvas(800, 600)
    can.grid(spacing=50, show_coords=True)

    # Layer 1: Background
    draw_sky(can, is_day=True)
    draw_ground(can)

    # Layer 2: Sun
    draw_sun(can, 700, 100)

    # Layer 3: Garden
    garden = create_garden_data()
    draw_garden(can, garden)

    return can
```

### Step 4: Add Butterflies

```python
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


def main():
    can = Canvas(800, 600)
    can.grid(spacing=50, show_coords=True)

    draw_sky(can, is_day=True)
    draw_ground(can)
    draw_sun(can, 700, 100)

    garden = create_garden_data()
    draw_garden(can, garden)

    # Layer 4: Butterflies (on top)
    draw_butterfly(can, 300, 200, CreativeGardenPalette.PEACH_WHISPER)
    draw_butterfly(can, 500, 250, CreativeGardenPalette.ROSE_QUARTZ)

    return can
```

**Challenge Ideas:**

1. **Add variety:** Create multiple flower types with different petal patterns
2. **Grass tufts:** Add small grass clumps using loops
3. **Clouds:** Draw puffy clouds using multiple circles
4. **Time of day:** Add parameter to change scene from day to night
5. **Garden path:** Draw a winding path through the garden
6. **Title:** Add a decorative title at the top
7. **Border:** Create a decorative border around the scene
8. **Interactive elements:** Add parameters to customize the entire scene

## Project Checklist

- [ ] Background (sky and ground)
- [ ] At least 5 flowers with variety in size/color
- [ ] At least one other element (butterfly, cloud, sun, etc.)
- [ ] Organized into functions
- [ ] Uses data structures (lists or dictionaries)
- [ ] Proper layering (back to front)
- [ ] Clean, readable code with comments

## Reflection

Congratulations on completing all 15 lessons! You've learned:
- Object creation and method calls
- Loops (for and while)
- Conditionals and boolean logic
- Functions with parameters and return values
- Data structures (lists and dictionaries)
- Code organization and reusability

You're now ready to create any visual program you can imagine!

## Next Steps

- Experiment with your own themes
- Combine multiple scenes
- Create animations by generating multiple frames
- Share your creations!
