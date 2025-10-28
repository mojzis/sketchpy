# Basic Functions

## What You'll Learn
- **Programming:** Function definition with `def`, function parameters, function calls, code organization
- **Drawing:** Reusable flower drawing functions

## Why Use Functions?

Imagine you want to draw the same flower 10 times. You could copy-paste the code 10 times, but what if you want to change the flower design? You'd have to update it in 10 places!

Functions let you write code once and reuse it many times. They're like recipes - write the instructions once, use them whenever needed.

## Defining a Function

```python
def draw_simple_flower(can, x, y):
    """Draw a simple flower at position (x, y)"""
    # Center
    can.circle(x, y, 20, fill=CreativeGardenPalette.BUTTER_YELLOW,
               stroke='#000', stroke_width=2)

    # Petals
    can.circle(x, y - 28, 22, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)
    can.circle(x + 28, y, 22, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)
    can.circle(x, y + 28, 22, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)
    can.circle(x - 28, y, 22, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)
```

**Parts of a function:**
- `def` - keyword that starts function definition
- `draw_simple_flower` - function name (use lowercase with underscores)
- `(can, x, y)` - parameters (inputs the function needs)
- `"""..."""` - docstring (describes what function does)
- Indented code - function body (what it does)

## Calling a Function

```python
# After defining the function, call it like this:
draw_simple_flower(can, 200, 300)  # Draw at (200, 300)
draw_simple_flower(can, 400, 300)  # Draw at (400, 300)
draw_simple_flower(can, 600, 300)  # Draw at (600, 300)
```

Three lines of code draw three flowers! Much better than copying the shape code three times.

## Instructions

### Step 1: Create a Flower Function

```python
from sketchpy.shapes import Canvas, CreativeGardenPalette


def draw_flower(can, x, y):
    """Draw a flower at the specified position"""
    # Draw flower center
    can.circle(x, y, 20, fill=CreativeGardenPalette.BUTTER_YELLOW,
               stroke='#000', stroke_width=2)

    # Draw 4 petals
    can.circle(x, y - 28, 22, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)
    can.circle(x + 28, y, 22, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)
    can.circle(x, y + 28, 22, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)
    can.circle(x - 28, y, 22, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)


def main():
    can = Canvas(800, 600)
    can.grid(spacing=50, show_coords=True)

    # Now we can draw many flowers easily!
    for i in range(6):
        x = 100 + i * 120
        draw_flower(can, x, 400)

    return can
```

**Try it:** Change the loop to draw flowers in a different pattern.

### Step 2: Create Multiple Functions

```python
def draw_stem(can, x, y, height):
    """Draw a stem from y down to y + height"""
    can.line(x, y, x, y + height,
             stroke=CreativeGardenPalette.MINT_CREAM,
             stroke_width=6)


def draw_butterfly(can, x, y):
    """Draw a simple butterfly"""
    # Body
    can.ellipse(x, y, 12, 40, fill=CreativeGardenPalette.LILAC_DREAM,
                stroke='#000', stroke_width=2)

    # Wings
    can.circle(x - 20, y - 10, 18, fill=CreativeGardenPalette.PEACH_WHISPER,
               stroke='#000', stroke_width=1.5)
    can.circle(x + 20, y - 10, 18, fill=CreativeGardenPalette.PEACH_WHISPER,
               stroke='#000', stroke_width=1.5)


def main():
    can = Canvas(800, 600)
    can.grid(spacing=50, show_coords=True)

    # Draw flowers with stems
    for i in range(5):
        x = 120 + i * 140
        draw_stem(can, x, 450, 80)
        draw_flower(can, x, 450)

    # Add some butterflies
    draw_butterfly(can, 300, 250)
    draw_butterfly(can, 500, 200)

    return can
```

Now you have a library of reusable drawing functions!

**Try it:** Create a `draw_grass()` function that draws a small grass tuft.

### Step 3: Functions Can Call Other Functions

```python
def draw_complete_flower(can, x, y):
    """Draw a flower with stem"""
    # Draw stem first (back layer)
    draw_stem(can, x, y, 80)

    # Draw flower on top
    draw_flower(can, x, y)


def main():
    can = Canvas(800, 600)
    can.grid(spacing=50, show_coords=True)

    # One function call draws both stem and flower!
    for i in range(6):
        x = 100 + i * 120
        draw_complete_flower(can, x, 450)

    return can
```

Functions can call other functions to build complex drawings from simple parts!

**Challenge:** Create a `draw_garden()` function that draws an entire scene with ground, flowers, and butterflies.

## Common Issues

### Issue: "NameError: name 'draw_flower' is not defined"
**Solution:** Make sure you define functions BEFORE you call them. Function definitions must come before `main()` or before any code that uses them.

### Issue: Nothing appears when I call my function
**Solution:** Check that you're passing the canvas object as the first parameter: `draw_flower(can, x, y)` not `draw_flower(x, y)`.

### Issue: "TypeError: draw_flower() takes 3 positional arguments but 2 were given"
**Solution:** You're not passing enough arguments. If function needs (can, x, y), you must provide all three.
