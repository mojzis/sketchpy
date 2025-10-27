## Additional Help

### Common Issues

**TypeError: missing required argument?**
- Count your parameters: `def draw_car(canvas, x, y, width, color):`
- Count your arguments: `draw_car(can, 50, 200, 150, Color.RED)`
- They must match! 5 parameters = 5 arguments

**Parameters in wrong order?**
- Arguments are matched by position: first argument → first parameter
- If you define `def draw_car(canvas, x, y, width, color):`
- Then call `draw_car(can, Color.RED, 50, 200, 150)` - RED becomes x! ❌
- Order matters! Keep arguments in the same order as parameters ✓

**Car parts in wrong positions?**
- Use parameters for calculations instead of fixed numbers
- ❌ `canvas.rect(200, 300, ...)` - fixed position
- ✓ `canvas.rect(x, y, ...)` - uses parameter
- ✓ `canvas.circle(x + width * 0.25, y + height, ...)` - proportional

**Car looks weird at different sizes?**
- Use proportional calculations, not fixed values
- ❌ `height = 75` - always same height
- ✓ `height = width * 0.5` - scales with width
- ❌ `wheel_radius = 25` - always same wheel size
- ✓ `wheel_radius = height * 0.3` - scales with car

### Understanding Parameter Scope

Variables defined as parameters only exist inside the function:
```python
def draw_car(canvas, x, y, width, color):
    # x, y, width, color available here
    height = width * 0.5  # Local variable, also only inside
    canvas.rect(x, y, width, height, fill=color)

# x, y, width, color DON'T exist here!
draw_car(can, 50, 200, 150, Color.RED)  # Must pass values
```

### Tips for Proportional Design

1. **Choose a base parameter**: Usually width or height
2. **Calculate everything from it**:
   ```python
   height = width * 0.5
   wheel_radius = height * 0.3
   window_width = width * 0.2
   ```
3. **Position relative to x, y**:
   ```python
   # Wheel at 25% from left, below car
   wheel_x = x + width * 0.25
   wheel_y = y + height + wheel_radius
   ```

### Function Design Principles

**Good parameter naming:**
- ✓ `def draw_car(canvas, x, y, width, color)` - clear!
- ❌ `def draw_car(c, a, b, w, col)` - confusing!

**Logical parameter order:**
1. Canvas (always first)
2. Position (x, y)
3. Size (width, height)
4. Appearance (color, stroke, etc.)

**Keep it simple:**
- Start with fewer parameters
- Add more as needed
- Too many parameters (>5-6) can be confusing

### Debugging Strategy

1. Print/display parameter values with `can.text()`
2. Test with simple values first (100, 200, 300)
3. Check calculations step by step
4. Draw one element at a time
5. Verify proportions at different sizes

### Advanced: Default Parameters

Once comfortable, you can add defaults:
```python
def draw_car(canvas, x, y, width=150, color=Color.RED):
    # width and color are optional - use defaults if not provided
    ...

draw_car(can, 50, 200)  # Uses width=150, color=RED
draw_car(can, 50, 200, 200)  # Uses width=200, color=RED
draw_car(can, 50, 200, 200, Color.BLUE)  # All specified
```
