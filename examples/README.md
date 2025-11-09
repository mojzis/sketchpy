# sketchpy Examples

This directory contains example scripts demonstrating various features of sketchpy.

## Running Examples

All examples can be run directly with Python:

```bash
python examples/simple_shapes.py
python examples/ocean_scene.py
python examples/math_doodling_demo.py
```

The marimo notebook can be opened with:

```bash
marimo edit examples/house.mo.py
```

## Example Files

### Beginner Examples

**simple_shapes.py** - Start here!
- Basic shapes (circles, rectangles, lines)
- Color usage
- Saving to SVG file
- Perfect for first-time users

**house.mo.py** - Complete scene (marimo notebook)
- Drawing a house with windows and door
- Using multiple shapes together
- Sky, ground, sun, and flowers
- Shows marimo notebook integration

### Organic Shapes

**organic_shapes_demo.py** - Blobs and tentacles showcase
- Smooth Bézier blob curves
- S-curve tentacles with twist parameter
- Demonstrates wobble and curl effects
- Great for understanding organic shapes

**convex_blobs_demo.py** - Blob variations
- Different wobble values
- Point count variations
- Understanding blob parameters

### Ocean Theme

**ocean_scene.py** - Complete underwater scene
- Multiple octopi with OceanShapes helper
- Jellyfish floating in water
- Seaweed on ocean floor
- Sandy bottom with blobs
- Ocean gradient background
- Demonstrates helper classes

**ocean_primitives.py** - Building blocks
- Individual ocean creature components
- Shows how helpers are constructed
- Educational for understanding complex shapes

### Mathematical Patterns

**math_doodling_demo.py** - Geometric patterns
- Six different pattern examples
- Overlapping circles with transparency
- Spirograph patterns
- Mandala designs
- Demonstrates MathDoodlingPalette usage
- Perfect for exploring symmetry

## Output

By default, examples that save files will create output in a `debug_out/` directory (you may need to create this directory first):

```bash
mkdir -p debug_out
python examples/ocean_scene.py
```

You can modify the examples to save files to any location you prefer.

## Learning Path

Recommended order for learning:

1. **simple_shapes.py** - Get comfortable with basic drawing
2. **house.mo.py** - See how shapes combine into scenes
3. **ocean_scene.py** - Learn helper classes
4. **organic_shapes_demo.py** - Explore advanced organic shapes
5. **math_doodling_demo.py** - Create mathematical art

## Creating Your Own Examples

Start with this template:

```python
from sketchpy import Canvas, Color

# Create canvas
can = Canvas(800, 600)

# Draw shapes
can.circle(400, 300, 100, fill=Color.BLUE)
can.rect(350, 400, 100, 50, fill=Color.RED)

# Save
can.save("my_drawing.svg")
print("Saved to my_drawing.svg")
```

## Tips

- **Coordinate System**: Origin (0,0) is top-left corner
- **Use Grid**: Add `can.grid()` to see coordinates while learning
- **Method Chaining**: Chain methods for concise code: `can.circle(...).rect(...)`
- **Color Palettes**: Explore different palettes for themed drawings
- **Randomness**: Use `random.seed()` for reproducible random shapes

## Need Help?

- Check the main [README.md](../README.md) for API reference
- See [CLAUDE.md](../CLAUDE.md) for development documentation
- Open an issue on GitHub if you find problems
