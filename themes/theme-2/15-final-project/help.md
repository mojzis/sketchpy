# Help: Final Project

## Project Planning

### 1. Sketch Your Scene
Draw it on paper first:
- What's in the background?
- What's in the foreground?
- Where are the main elements?

### 2. List Your Layers (Back to Front)
```
Layer 1: Sky and ground
Layer 2: Sun/moon, clouds
Layer 3: Flowers, stems, grass
Layer 4: Butterflies, foreground elements
Layer 5: Labels, title
```

### 3. Identify Functions Needed
```python
# Background
draw_sky()
draw_ground()

# Elements
draw_sun()
draw_cloud()
draw_flower()
draw_butterfly()

# Helpers
calculate_positions()
get_color_scheme()
```

### 4. Define Your Data
```python
# What properties does each object need?
flower = {
    "x": ...,
    "y": ...,
    "size": ...,
    "colors": ...
}
```

## Code Organization Template

```python
from sketchpy.shapes import Canvas, CreativeGardenPalette


# ===== CALCULATION FUNCTIONS =====

def calculate_something(input):
    """Calculate and return a value"""
    result = input * 2
    return result


# ===== DRAWING FUNCTIONS =====

def draw_background(can):
    """Draw sky and ground"""
    pass


def draw_element(can, x, y, size):
    """Draw a specific element"""
    pass


# ===== DATA FUNCTIONS =====

def create_scene_data():
    """Define scene as data structure"""
    return [
        {"x": 100, "y": 200, "size": 20},
        {"x": 200, "y": 200, "size": 25}
    ]


# ===== MAIN FUNCTION =====

def main():
    """Assemble the complete scene"""
    can = Canvas(800, 600)

    # Layer by layer
    draw_background(can)

    # Use data
    scene_data = create_scene_data()
    for item in scene_data:
        draw_element(can, item["x"], item["y"], item["size"])

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-15.svg')
```

## Common Patterns

### Pattern 1: Layered Drawing
```python
def main():
    can = Canvas(800, 600)

    # Draw back to front
    draw_sky(can)
    draw_ground(can)
    draw_background_elements(can)
    draw_main_elements(can)
    draw_foreground(can)

    return can
```

### Pattern 2: Data-Driven Scene
```python
def create_all_objects():
    """Return all scene objects as data"""
    return {
        "flowers": [...],
        "butterflies": [...],
        "clouds": [...]
    }


def draw_scene(can, scene_data):
    """Draw everything from data"""
    for flower in scene_data["flowers"]:
        draw_flower(can, flower)

    for butterfly in scene_data["butterflies"]:
        draw_butterfly(can, butterfly)
```

### Pattern 3: Configurable Scene
```python
def main():
    can = Canvas(800, 600)

    # Configuration
    is_day = True
    season = "spring"
    weather = "sunny"

    # Use config to control drawing
    draw_sky(can, is_day)

    if weather == "sunny":
        draw_sun(can, 700, 100)

    if season == "spring":
        draw_flowers(can, num_flowers=10)

    return can
```

## Debugging Large Projects

### 1. Build Incrementally
```python
# Start simple
def main():
    can = Canvas(800, 600)
    draw_sky(can)  # Test just this
    return can

# Add one element at a time
def main():
    can = Canvas(800, 600)
    draw_sky(can)
    draw_ground(can)  # Add this, test
    return can
```

### 2. Test Functions Separately
```python
# Test one function in isolation
def main():
    can = Canvas(800, 600)
    can.grid(spacing=50, show_coords=True)

    # Just test the flower function
    draw_flower(can, 400, 300, 20,
                CreativeGardenPalette.ROSE_QUARTZ,
                CreativeGardenPalette.BUTTER_YELLOW)

    return can
```

### 3. Use Print Statements
```python
def draw_garden(can, garden_data):
    print(f"Drawing {len(garden_data)} flowers")

    for i, flower in enumerate(garden_data):
        print(f"  Flower {i}: at ({flower['x']}, {flower['y']})")
        draw_flower(can, flower)
```

### 4. Comment Out Sections
```python
def main():
    can = Canvas(800, 600)

    draw_sky(can)
    draw_ground(can)
    # draw_garden(can, garden_data)  # Temporarily disabled
    draw_butterflies(can)

    return can
```

## Project Extension Ideas

### Easy Extensions
- Add more flowers with different colors
- Add clouds in the sky
- Add grass tufts on the ground
- Change time of day (day/night)

### Medium Extensions
- Create multiple flower types with different petal patterns
- Add a winding path through the garden
- Add a decorative border
- Create a weather system (rain, snow)

### Advanced Extensions
- Add depth/perspective (things farther away are smaller)
- Create seasons (spring, summer, fall, winter)
- Add animation frames (flower growth sequence)
- Create a garden designer (parameters to customize everything)

## Checklist for Completion

- [ ] Code is organized into functions
- [ ] Uses at least one data structure (list or dictionary)
- [ ] Has proper layering (background to foreground)
- [ ] Includes variety (different sizes, colors, positions)
- [ ] Has comments explaining key sections
- [ ] Runs without errors
- [ ] Creates an interesting, complete scene

## Celebrating Your Achievement

You've completed all 15 lessons! You now know:

1. **Fundamentals:** Objects, methods, coordinates
2. **Loops:** For loops, while loops, nested loops
3. **Data:** Variables, lists, dictionaries
4. **Logic:** Conditionals, boolean operators
5. **Functions:** Definition, parameters, return values
6. **Organization:** Code structure, data-driven design

You're ready to create any visual program you can imagine!

## Next Steps

- Create your own themes (space, underwater, city, etc.)
- Share your projects with others
- Explore Python libraries (Pygame, Processing, etc.)
- Build interactive applications
- Keep learning and creating!
