## ⭕ Project 12: Customizable Mandala

### Goal
Extend your mandala function with parameters for size, color, circle count, and opacity - making it fully customizable!

### What you'll learn
- Functions with multiple parameters
- Default parameter values
- How parameters give flexibility
- Creating a "mandala toolkit"

### Multiple Parameters
Each parameter controls one aspect:

```python
def draw_mandala(canvas, cx, cy, num_circles, orbit_radius,
                 circle_size, color, opacity):
    # Now fully customizable!
```

### Default Parameters
We can make some parameters optional:

```python
def draw_mandala(canvas, cx, cy, num_circles=8, color=MIST_BLUE):
    # If not provided, num_circles defaults to 8
```

### Steps
1. Add parameters to `draw_mandala()`:
   - `num_circles` - How many circles
   - `orbit_radius` - How far from center
   - `circle_size` - Size of each circle
   - `color` - Which color to use
   - `opacity` - Transparency level
2. Use these parameters in the function body
3. Create different mandalas with different settings!

### Parameter Power
Same function, infinite variations:
```python
draw_mandala(can, 200, 200, 12, 100, 60, MIST_BLUE, 0.3)
draw_mandala(can, 600, 200, 6, 120, 80, MIST_ROSE, 0.2)
```

### Challenge
- Add a `stroke_color` parameter
- Create a "small", "medium", "large" helper function that calls your function with preset sizes
- Make a rainbow by drawing the same mandala multiple times with different colors and slight offsets
