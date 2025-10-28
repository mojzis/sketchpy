# Help: First Flower

## Quick Reference

### Creating a Canvas
```python
from sketchpy.shapes import Canvas, CreativeGardenPalette

can = Canvas(width, height)  # Creates a canvas
```

### Drawing Shapes
```python
# Circle
can.circle(x, y, radius, fill=color, stroke=outline, stroke_width=thickness)

# Line
can.line(x1, y1, x2, y2, stroke=color, stroke_width=thickness)

# Ellipse (oval)
can.ellipse(x, y, width, height, fill=color, stroke=outline, stroke_width=thickness)
```

### Coordinate Grid
```python
can.grid(spacing=50, show_coords=True)  # Shows a grid with coordinate labels
```

## Common Errors

### Error: "NameError: name 'Canvas' is not defined"
**What it means:** You forgot to import Canvas
**How to fix:** Add at the top: `from sketchpy.shapes import Canvas, CreativeGardenPalette`

### Error: "NameError: name 'CreativeGardenPalette' is not defined"
**What it means:** You're using palette colors but didn't import the palette
**How to fix:** Add `CreativeGardenPalette` to your import: `from sketchpy.shapes import Canvas, CreativeGardenPalette`

### Error: My shape doesn't appear
**What it means:** The shape might be outside the canvas boundaries or the same color as the background
**How to fix:**
- Check that x is between 0 and canvas width
- Check that y is between 0 and canvas height
- Use the grid to verify positions
- Make sure you're using a visible color

### Error: "TypeError: circle() missing required positional argument"
**What it means:** You forgot one of the required parameters (x, y, or radius)
**How to fix:** Circle needs at least 3 numbers: `can.circle(x, y, radius)`

## Debugging Tips

1. **Use the grid:** Always include `can.grid(spacing=50, show_coords=True)` while learning - it shows you exactly where coordinates are
2. **Start simple:** Draw one shape at a time, check it works, then add the next
3. **Check the numbers:** For an 800x600 canvas, the center is at (400, 300)
4. **Colors need quotes:** Hex colors like `'#000'` need quotes, but palette colors don't: `CreativeGardenPalette.ROSE_QUARTZ`

## Color Palette Reference

### CreativeGardenPalette Colors
- **PEACH_WHISPER** - Soft peach
- **ROSE_QUARTZ** - Muted pink
- **BUTTER_YELLOW** - Soft yellow
- **MINT_CREAM** - Mint green
- **SKY_BREEZE** - Powder blue
- **LILAC_DREAM** - Soft lilac
- **CORAL_BLUSH** - Gentle coral
- **LEMON_CHIFFON** - Pale yellow
- **MISTY_MAUVE** - Soft mauve
- **HONEYDEW** - Very pale green
- **VANILLA_CREAM** - Warm white

## Related Lessons
- **Next:** Lesson 2 uses for loops to draw multiple flowers

## Extra Challenges

1. **Different flower:** Change the number of petals (try 4 or 8 petals)
2. **Color variations:** Use different petal colors from CreativeGardenPalette
3. **Add leaves:** Use ellipses to draw leaves on the stem
4. **Multiple flowers:** Draw 2-3 flowers at different positions
5. **Bigger/smaller:** Try different petal and center sizes
