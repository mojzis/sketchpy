# sketchpy

[![PyPI version](https://img.shields.io/pypi/v/sketchpy.svg)](https://pypi.org/project/sketchpy/)
[![Python versions](https://img.shields.io/pypi/pyversions/sketchpy.svg)](https://pypi.org/project/sketchpy/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple Python library for drawing shapes. Made for learning programming through visual art.

## What is sketchpy?

sketchpy lets you draw shapes on a canvas using Python. It creates SVG graphics that work in notebooks (like marimo and Jupyter) and web browsers via Pyodide. There's no complicated setup - you just tell the computer where to draw things.

**Zero dependencies.** Pure Python. Works everywhere.

## Why sketchpy?

- **🎯 Education-first**: Designed specifically for teaching programming through visual feedback
- **🚀 Zero dependencies**: No heavy libraries, just pure Python
- **🌐 Browser-native**: Runs in web browsers via Pyodide (no backend required)
- **📓 Notebook-friendly**: Works seamlessly in marimo and Jupyter
- **🎨 No turtle paradigm**: Direct coordinate positioning (no state machine)
- **🔒 Safe by default**: Built-in security limits for browser environments
- **⛓️ Method chaining**: Fluent API for elegant code
- **🎨 Rich palettes**: Curated color palettes for different moods and themes

### Comparison with other libraries

| Feature | sketchpy | turtle | matplotlib | PIL/Pillow |
|---------|----------|--------|------------|------------|
| Dependencies | 0 | stdlib | Many | C libraries |
| Browser support | ✅ (Pyodide) | ❌ | Limited | ❌ |
| Educational focus | ✅ | ✅ | ❌ | ❌ |
| Vector graphics | ✅ (SVG) | Limited | ✅ | ❌ (raster) |
| API complexity | Simple | Simple | Complex | Medium |
| State machine | No | Yes | No | No |
| File size | ~5KB SVG | N/A | Large PNG | Large PNG |

## Quick start

Install with pip:

```bash
pip install sketchpy
```

Or with uv:

```bash
uv add sketchpy
```

## Basic example: Drawing a flower

```python
from sketchpy import Canvas, Color

# Create a canvas (like a piece of paper)
can = Canvas(400, 400)

# Draw the flower center
can.circle(200, 200, 30, fill=Color.YELLOW)

# Draw 8 petals around the center
petal_positions = [
    (200, 140), (242, 158), (260, 200), (242, 242),
    (200, 260), (158, 242), (140, 200), (158, 158)
]

for x, y in petal_positions:
    can.circle(x, y, 25, fill=Color.PINK)

# Draw a stem
can.rect(195, 230, 10, 100, fill=Color.GREEN)

# Add two leaves
can.ellipse(180, 280, 20, 10, fill=Color.GREEN)
can.ellipse(220, 300, 20, 10, fill=Color.GREEN)

# In a marimo/Jupyter notebook, just write "can" to see it
# Or save to a file:
can.save("flower.svg")
```

## Features

### Basic Shapes

All the shapes you need to get started:

```python
from sketchpy import Canvas, Color

can = Canvas(800, 600)

# Circles and ellipses
can.circle(100, 100, 50, fill=Color.RED)
can.ellipse(250, 100, 60, 40, fill=Color.BLUE)

# Rectangles (regular and rounded)
can.rect(400, 50, 100, 100, fill=Color.GREEN)
can.rounded_rect(550, 50, 100, 100, rx=15, fill=Color.ORANGE)

# Lines and polygons
can.line(100, 250, 200, 350, stroke=Color.BLACK, stroke_width=3)
can.polygon([(400, 250), (500, 250), (450, 350)], fill=Color.PURPLE)

# Text
can.text(100, 450, "Hello, World!", size=24, fill=Color.BLACK)
```

### Organic Shapes

Create natural, flowing shapes perfect for creative projects:

```python
from sketchpy import Canvas, Color
import random

random.seed(42)  # For reproducible randomness
can = Canvas(800, 600)

# Blobs - organic irregular circles
can.blob(200, 300, radius=80, wobble=0.3, fill=Color.BLUE)

# Tentacles - flowing curves with S-shapes
can.tentacle(400, 100, 300, 400, curl=0.5, twist=0.6,
             thickness=30, taper=0.3, fill=Color.PURPLE)

# Waves - sinusoidal lines
can.wave(0, 300, 800, 320, height=20, waves=4, stroke=Color.BLUE)
```

### Gradients

Beautiful color transitions:

```python
from sketchpy import Canvas

can = Canvas(800, 600)

# Linear gradient
can.linear_gradient("sunset",
    start=(0, 0), end=(100, 0),
    colors=["#FF6B6B", "#FFA500", "#FFD93D"])

can.rect(100, 100, 600, 200, fill="gradient:sunset")

# Radial gradient
can.radial_gradient("glow",
    center=(50, 50), radius=50,
    colors=["#FFFFFF", "#FF0000"])

can.circle(400, 450, 100, fill="gradient:glow")
```

### Groups and Transformations

Organize and manipulate multiple shapes together:

```python
from sketchpy import Canvas, Color

can = Canvas(800, 600)

# Group shapes together
with can.group("car"):
    can.rect(100, 200, 120, 50, fill=Color.RED)
    can.circle(130, 250, 15, fill=Color.BLACK)
    can.circle(190, 250, 15, fill=Color.BLACK)

# Move the entire group
can.move_group("car", dx=100, dy=50)

# Rotate the group
can.rotate_group("car", angle=15, cx=160, cy=225)

# Hide/show groups
can.hide_group("car")
can.show_group("car")
```

### Color Palettes

Curated color palettes for different moods:

```python
from sketchpy import Canvas, Color, CalmOasisPalette, CreativeGardenPalette

can = Canvas(800, 600)

# Basic colors
can.circle(100, 100, 40, fill=Color.RED)
can.circle(200, 100, 40, fill=Color.BLUE)

# Calm, therapeutic colors
can.circle(300, 100, 40, fill=CalmOasisPalette.SKY_BLUE)
can.circle(400, 100, 40, fill=CalmOasisPalette.MINT_FRESH)

# Creative, expressive colors
can.circle(500, 100, 40, fill=CreativeGardenPalette.PEACH_WHISPER)
can.circle(600, 100, 40, fill=CreativeGardenPalette.ROSE_QUARTZ)

# Display all colors in a palette
can.show_palette(CalmOasisPalette)
```

Available palettes:
- **Color**: 12 basic colors (RED, BLUE, GREEN, etc.)
- **CalmOasisPalette**: 12 calming blues/greens for focus and relaxation
- **CreativeGardenPalette**: 12 pastel colors for creative expression
- **MathDoodlingPalette**: Triadic palette for geometric patterns with transparency
- **OceanPalette**: Ocean-themed colors for underwater scenes

### Helper Shapes

Pre-built complex shapes for educational scaffolding:

```python
from sketchpy import Canvas, OceanShapes, CarShapes

can = Canvas(800, 600)

# Ocean creatures
ocean = OceanShapes(can)
ocean.octopus(400, 300, size=120)
ocean.jellyfish(200, 150, size=80)
ocean.seaweed(100, 600, height=200)

# Vehicles (static methods)
CarShapes.simple_car(can, x=100, y=400, width=120, color="#FF0000")
CarShapes.traffic_light(can, x=500, y=300, state="green")
CarShapes.road(can, x1=0, y1=500, x2=800, y2=500)
```

### Learning Aids

Tools to help understand coordinates:

```python
from sketchpy import Canvas, Color

can = Canvas(800, 600)

# Show a coordinate grid
can.grid(spacing=50, show_coords=True)

# Now draw shapes - the grid helps you see where they go
can.circle(400, 300, 50, fill=Color.RED)
```

### Method Chaining

Write elegant, concise code:

```python
from sketchpy import Canvas, Color

# Chain multiple operations
can = (Canvas(400, 300)
    .circle(100, 100, 50, fill=Color.RED)
    .rect(200, 100, 80, 120, fill=Color.BLUE)
    .text(150, 250, "Chained!", size=20, fill=Color.BLACK))
```

## Usage

### In marimo notebooks

Create a file called `drawing.py`:

```python
import marimo as mo
from sketchpy import Canvas, Color

# Create your drawing
can = Canvas(800, 600)
can.circle(400, 300, 100, fill=Color.BLUE)
can.rect(350, 400, 100, 50, fill=Color.RED)

# Display it (marimo shows it automatically)
can
```

Run it: `marimo edit drawing.py`

### In Jupyter notebooks

```python
from sketchpy import Canvas, Color

can = Canvas(800, 600)
can.circle(400, 300, 100, fill=Color.BLUE)

# Display automatically
can
```

### Standalone scripts

```python
from sketchpy import Canvas, Color

can = Canvas(800, 600)
can.circle(400, 300, 100, fill=Color.BLUE)

# Save to file
can.save("output.svg")
```

### In the browser (via Pyodide)

sketchpy works in the browser without any backend:

```html
<script type="module">
  import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.mjs";

  const pyodide = await loadPyodide();
  await pyodide.loadPackage("micropip");
  await pyodide.runPythonAsync(`
    import micropip
    await micropip.install('sketchpy')

    from sketchpy import Canvas, Color

    can = Canvas(400, 400)
    can.circle(200, 200, 100, fill=Color.BLUE)

    can.to_svg()
  `);
</script>
```

## API Reference

### Canvas

Main drawing surface:

```python
Canvas(width=800, height=600, background=Color.WHITE)
```

**Shape methods:**
- `circle(x, y, radius, fill, stroke, stroke_width, opacity)` - Draw a circle
- `rect(x, y, width, height, fill, stroke, stroke_width)` - Draw a rectangle
- `ellipse(x, y, rx, ry, fill, stroke, stroke_width)` - Draw an ellipse
- `line(x1, y1, x2, y2, stroke, stroke_width)` - Draw a line
- `polygon(points, fill, stroke, stroke_width)` - Draw a polygon from points
- `text(x, y, text, size, fill, font)` - Draw text
- `rounded_rect(x, y, width, height, rx, ry, fill, stroke, stroke_width)` - Rectangle with rounded corners

**Organic shapes:**
- `blob(x, y, radius, wobble, points, fill, stroke, stroke_width)` - Irregular organic circle
- `tentacle(x1, y1, x2, y2, curl, twist, thickness, taper, fill, stroke, stroke_width)` - Flowing curve
- `wave(x1, y1, x2, y2, height, waves, stroke, stroke_width)` - Sinusoidal wave line

**Gradients:**
- `linear_gradient(name, start, end, colors)` - Define linear gradient
- `radial_gradient(name, center, radius, colors)` - Define radial gradient

**Groups:**
- `group(name)` - Context manager for grouping shapes
- `move_group(name, dx, dy)` - Move a group
- `rotate_group(name, angle, cx, cy)` - Rotate a group
- `hide_group(name)` - Hide a group
- `show_group(name)` - Show a group
- `remove_group(name)` - Delete a group

**Utilities:**
- `grid(spacing, color, show_coords)` - Draw coordinate grid
- `show_palette(palette_class, ...)` - Display color palette
- `clear()` - Remove all shapes
- `to_svg()` - Get SVG string
- `save(filename)` - Save to SVG file

All drawing methods return `self` for method chaining.

### Color Palettes

Import specific palettes:

```python
from sketchpy import Color, CalmOasisPalette, CreativeGardenPalette, MathDoodlingPalette, OceanPalette
```

Each palette is a class with color constants (e.g., `Color.RED`, `CalmOasisPalette.SKY_BLUE`).

### Helper Shapes

```python
from sketchpy import OceanShapes, CarShapes

# OceanShapes (instance-based)
ocean = OceanShapes(canvas)
ocean.octopus(x, y, size, body_color, eye_color)
ocean.jellyfish(x, y, size, body_color, tentacle_count)
ocean.seaweed(x, y, height, sway, color)

# CarShapes (static methods)
CarShapes.simple_car(canvas, x, y, width, height, color)
CarShapes.wheel(canvas, x, y, radius, tire_color, rim_color)
CarShapes.traffic_light(canvas, x, y, size, state)
CarShapes.road(canvas, x1, y1, x2, y2, width, lanes)
```

## Examples

Check out the `examples/` directory for complete working examples:

- **house.mo.py** - Complete house scene (marimo notebook)
- **ocean_scene.py** - Underwater scene with octopi and jellyfish
- **organic_shapes_demo.py** - Showcase of blobs and tentacles
- **math_doodling_demo.py** - Geometric patterns with transparency
- **convex_blobs_demo.py** - Blob shape variations
- **ocean_primitives.py** - Ocean creature building blocks

Run any example:

```bash
python examples/ocean_scene.py
```

Or open in marimo:

```bash
marimo edit examples/house.mo.py
```

## Interactive Lessons

The project includes browser-based interactive lessons. To run them locally:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Start the lesson server
srv

# Open https://localhost:8007/sketchpy/ in your browser
# (Accept the security warning for the self-signed certificate)
```

The browser interface lets you write code and see results immediately, with step-by-step tutorials.

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/mojzis/sketchpy.git
cd sketchpy

# Install with development dependencies
pip install -e ".[dev]"

# Or with uv
uv sync
```

### Running Tests

```bash
# Python tests
pytest

# JavaScript tests
npm test

# Run all tests
npm test && pytest
```

### Building

```bash
# Build package
python -m build

# Build browser interface
build
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Links

- **Homepage**: https://github.com/mojzis/sketchpy
- **Documentation**: https://github.com/mojzis/sketchpy#readme
- **Issues**: https://github.com/mojzis/sketchpy/issues
- **PyPI**: https://pypi.org/project/sketchpy/
