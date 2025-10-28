# First Flower

## What You'll Learn
- **Programming:** Creating objects, calling methods with parameters, using coordinates
- **Drawing:** Making a simple flower with circles and understanding the canvas coordinate system

## Objects and Methods

Think of the Canvas as your drawing paper. Before you can draw anything, you need to create that paper and tell it how big to be. In programming, we call this "creating an object."

Once you have your Canvas object, you can use its "methods" to draw shapes. A method is like a built-in command that knows how to do something specific - like drawing a circle or rectangle.

## The Coordinate System

The canvas uses a coordinate system to position shapes:
- The origin (0, 0) is at the **top-left corner**
- X values increase as you move right
- Y values increase as you move down

This might seem backwards compared to math class (where Y goes up), but it's standard for computer graphics!

## Instructions

### Step 1: Create Your Canvas

```python
from sketchpy.shapes import Canvas, CreativeGardenPalette

can = Canvas(800, 600)
can.grid(spacing=50, show_coords=True)
```

The `Canvas(800, 600)` creates a canvas that's 800 pixels wide and 600 pixels tall. The grid helps you see coordinates while you're learning.

**Try it:** Change the canvas size to 400x400 and see how the grid changes.

### Step 2: Draw the Flower Center

```python
# Draw a yellow center at position (400, 300) with radius 30
can.circle(400, 300, 30, fill=CreativeGardenPalette.BUTTER_YELLOW,
           stroke='#000', stroke_width=2)
```

The `circle()` method needs:
- `x` position (400 = horizontal center of 800-wide canvas)
- `y` position (300 = vertical center of 600-tall canvas)
- `radius` size (30 pixels)
- `fill` color (what color inside)
- `stroke` outline color (black)
- `stroke_width` how thick the outline is

**Try it:** Move the circle to different positions using the grid coordinates.

### Step 3: Add Petals Around the Center

```python
# Draw 6 pink petals arranged in a circle pattern
petal_positions = [
    (400, 230),  # Top
    (450, 265),  # Top-right
    (450, 335),  # Bottom-right
    (400, 370),  # Bottom
    (350, 335),  # Bottom-left
    (350, 265)   # Top-left
]

for x, y in petal_positions:
    can.circle(x, y, 40, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=2)
```

We use a list to store all the petal positions, then loop through them to draw each petal. This saves us from writing the same code 6 times!

**Try it:** Change the petal color to `CreativeGardenPalette.LILAC_DREAM` or `CreativeGardenPalette.PEACH_WHISPER`.

### Step 4: Add a Stem

```python
# Draw a green stem from the bottom of the flower down
can.line(400, 330, 400, 500, stroke=CreativeGardenPalette.MINT_CREAM,
         stroke_width=8)
```

The `line()` method draws from point (x1, y1) to point (x2, y2).

**Challenge:** Add two leaves to the stem using ellipses. Hint: Use `can.ellipse(x, y, width, height, fill=...)` positioned partway down the stem.

## Common Issues

### Issue: My flower appears in the wrong place
**Solution:** Check your coordinates against the grid. Remember that (0, 0) is the top-left corner, not the center.

### Issue: I can't see my shapes
**Solution:** Make sure your fill colors are different from the background (which is white by default). Also check that your coordinates are within the canvas bounds (0-800 for x, 0-600 for y).

### Issue: The colors don't work
**Solution:** Make sure you imported `CreativeGardenPalette` at the top of your file. Color names are case-sensitive!
