# For Loops In Depth

## What You'll Learn
- **Programming:** For loops with different `range()` variants, position calculations
- **Drawing:** Creating a flower garden with precisely spaced flowers

## Understanding `range()` Better

You've used `range(5)` before, but `range()` has more tricks:

```python
range(5)        # 0, 1, 2, 3, 4 (start at 0, count 5 times)
range(1, 6)     # 1, 2, 3, 4, 5 (start at 1, stop before 6)
range(0, 10, 2) # 0, 2, 4, 6, 8 (start at 0, stop before 10, step by 2)
range(10, 0, -1)# 10, 9, 8, 7, 6, 5, 4, 3, 2, 1 (count backwards!)
```

## The Position Formula

When drawing things in a row, use this pattern:
```python
x = start_position + i * spacing
```

This formula is incredibly useful! It lets you control:
- **start_position:** Where the first item appears
- **spacing:** How far apart items are
- **i:** Which item this is (0, 1, 2, 3...)

## Instructions

### Step 1: Draw Flowers at Exact Positions

```python
from sketchpy.shapes import Canvas, CreativeGardenPalette

can = Canvas(800, 600)
can.grid(spacing=50, show_coords=True)

# Draw the ground
can.rect(0, 400, 800, 200, fill=CreativeGardenPalette.MINT_CREAM)

# Draw 6 flowers with perfect spacing
for i in range(6):
    x = 80 + i * 120  # Start at 80, space every 120 pixels
    y = 450           # Ground level

    # Draw stem
    can.line(x, y, x, y - 80, stroke=CreativeGardenPalette.MINT_CREAM,
             stroke_width=6)

    # Draw flower center
    can.circle(x, y - 80, 22, fill=CreativeGardenPalette.BUTTER_YELLOW,
               stroke='#000', stroke_width=2)

    # Draw petals
    can.circle(x, y - 110, 25, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=2)
    can.circle(x + 30, y - 80, 25, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=2)
    can.circle(x, y - 50, 25, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=2)
    can.circle(x - 30, y - 80, 25, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=2)
```

**Try it:** Change the spacing to 100 or 150 and see how it affects the garden.

### Step 2: Use Range with Start and Stop

```python
# Draw flowers numbered 1-5 (not starting from 0)
for flower_num in range(1, 6):  # 1, 2, 3, 4, 5
    x = flower_num * 130
    y = 300

    can.circle(x, y, 20, fill=CreativeGardenPalette.LEMON_CHIFFON,
               stroke='#000', stroke_width=2)

    # Label with the actual flower number
    can.text(f"#{flower_num}", x, y + 50,
             font_size=18, fill='#000', text_anchor='middle')
```

**Try it:** Use `range(3, 8)` to draw flowers numbered 3-7.

### Step 3: Create Patterns with Step Values

```python
# Draw every other position using step value
for i in range(0, 10, 2):  # 0, 2, 4, 6, 8 (every other number)
    x = 100 + i * 60
    y = 300

    can.circle(x, y, 25, fill=CreativeGardenPalette.LILAC_DREAM,
               stroke='#000', stroke_width=2)
```

This creates flowers at positions 0, 2, 4, 6, 8 - leaving gaps where 1, 3, 5, 7, 9 would be!

**Challenge:** Create two rows of flowers where one row has flowers at even positions and the other at odd positions. Use `range(0, 10, 2)` and `range(1, 10, 2)`.

## Common Issues

### Issue: Flowers overlap or are too far apart
**Solution:** Adjust the spacing value in your formula. Flowers should be spaced at least as far apart as they are wide.

### Issue: First flower is cut off at the edge
**Solution:** Increase your start_position to give some margin from the edge (try 80 or 100 instead of 0).

### Issue: "TypeError: 'float' object cannot be interpreted as an integer"
**Solution:** Range values must be integers (whole numbers), not decimals. Use `range(5)` not `range(5.5)`.
