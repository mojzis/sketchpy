# sketchpy

A simple Python library for drawing shapes. Made for learning programming through visual art.

## What is this?

sketchpy lets you draw shapes on a canvas using Python. It creates SVG graphics that work in notebooks (like marimo) and web browsers. There's no complicated setup - you just tell the computer where to draw things.

The library works in two ways:
- Write code in a marimo notebook and see your drawings
- Use the browser-based lessons to learn and practice

## Quick start

Install with uv (requires Python 3.14+):

```bash
uv add sketchpy
```

Or with pip:

```bash
pip install sketchpy
```

## Basic example: Drawing a flower

Here's how to draw a simple flower:

```python
from sketchpy.shapes import Canvas, Color

# Create a canvas (like a piece of paper)
canvas = Canvas(400, 400)

# Draw the flower center
canvas.circle(200, 200, 30, fill=Color.YELLOW)

# Draw 8 petals around the center
for i in range(8):
    angle = i * 45  # Spread petals evenly
    x = 200 + 60 * (i % 2 == 0)  # Alternate distances
    y = 200 - 60 if i in [0, 4] else 200

    # Adjust position based on petal number
    if i == 1: x, y = 242, 158
    if i == 2: x, y = 260, 200
    if i == 3: x, y = 242, 242
    if i == 5: x, y = 158, 242
    if i == 6: x, y = 140, 200
    if i == 7: x, y = 158, 158

    canvas.circle(x, y, 25, fill=Color.PINK)

# Draw a stem
canvas.rect(195, 230, 10, 100, fill=Color.GREEN)

# Add two leaves
canvas.ellipse(180, 280, 20, 10, fill=Color.GREEN)
canvas.ellipse(220, 300, 20, 10, fill=Color.GREEN)

# In a marimo notebook, just write "canvas" to see it
# Or save to a file:
canvas.save("flower.svg")
```

## How to use

### In a marimo notebook

Create a file called `drawing.py`:

```python
import marimo as mo
from sketchpy.shapes import Canvas, Color

# Create your drawing
canvas = Canvas(800, 600)
canvas.circle(400, 300, 100, fill=Color.BLUE)
canvas.rect(350, 400, 100, 50, fill=Color.RED)

# Display it (marimo shows it automatically)
canvas
```

Run it: `marimo edit drawing.py`

### Available shapes

- `circle(x, y, radius, fill, stroke, stroke_width)` - Draw a circle
- `rect(x, y, width, height, fill, stroke, stroke_width)` - Draw a rectangle
- `ellipse(x, y, rx, ry, fill, stroke, stroke_width)` - Draw an oval
- `line(x1, y1, x2, y2, stroke, stroke_width)` - Draw a line
- `polygon(points, fill, stroke, stroke_width)` - Draw any shape from points
- `text(x, y, text, size, fill, font)` - Write text
- `rounded_rect(x, y, width, height, rx, ry, fill, stroke, stroke_width)` - Rectangle with rounded corners

### Available colors

Use the `Color` class for common colors:
- `Color.RED`, `Color.BLUE`, `Color.GREEN`, `Color.YELLOW`
- `Color.BLACK`, `Color.WHITE`, `Color.GRAY`, `Color.SILVER`
- `Color.ORANGE`, `Color.PURPLE`, `Color.PINK`, `Color.BROWN`

Or use any hex color like `"#FF5733"`.

### Method chaining

You can draw multiple shapes in one line:

```python
Canvas(400, 300).circle(100, 100, 50, fill=Color.RED).rect(200, 100, 80, 120, fill=Color.BLUE)
```

### Using the grid

When learning coordinates, turn on the grid to see where things are:

```python
canvas = Canvas(800, 600)
canvas.grid()  # Shows coordinate lines
canvas.circle(400, 300, 50, fill=Color.RED)  # Now you can see where 400, 300 is
```

## Browser-based lessons

The project includes interactive lessons that run in your browser. To use them:

```bash
# Install development tools
uv sync

# Start the lesson server
uv run srv

# Open https://localhost:8000 in your browser
# (You'll need to accept the security warning for the self-signed certificate)
```

The browser interface lets you write code and see the results immediately, with helpful lessons for beginners.

## Development

Run tests:
```bash
uv run pytest          # Python tests
npm test              # JavaScript tests
```

Build the browser interface:
```bash
uv run build          # Generates output/index.html
```

## License

MIT License - see LICENSE file for details.
