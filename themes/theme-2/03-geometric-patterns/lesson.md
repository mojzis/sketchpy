# Geometric Patterns

## What You'll Learn
- **Programming:** Nested loops, 2D grid calculations, loop variable relationships
- **Drawing:** Creating repeating patterns with rows and columns

## Why Nested Loops?

A single loop lets you draw things in a line (one dimension). But what if you want to create a grid pattern, like a field of flowers with multiple rows? You need a loop inside a loop - this is called a "nested loop."

The outer loop handles rows (vertical position), and the inner loop handles columns (horizontal position).

## How Nested Loops Work

```python
for row in range(3):       # Runs 3 times (rows)
    for col in range(4):   # Runs 4 times per row (columns)
        # This code runs 3 × 4 = 12 times total!
```

Think of it like reading a book: you read across each line (inner loop), then move down to the next line (outer loop).

## Instructions

### Step 1: Create a Simple Grid

```python
from sketchpy.shapes import Canvas, CreativeGardenPalette

can = Canvas(800, 600)
can.grid(spacing=50, show_coords=True)

# Draw a 3×4 grid of flower centers
for row in range(3):
    for col in range(4):
        x = 100 + col * 150  # Column controls horizontal position
        y = 100 + row * 150  # Row controls vertical position

        # Draw a small flower center at each grid position
        can.circle(x, y, 25, fill=CreativeGardenPalette.BUTTER_YELLOW,
                   stroke='#000', stroke_width=2)
```

**How it works:**
- Row 0, Col 0: (100, 100)
- Row 0, Col 1: (250, 100)
- Row 0, Col 2: (400, 100)
- Row 0, Col 3: (550, 100)
- Row 1, Col 0: (100, 250)
- And so on...

**Try it:** Change the `range()` values to create different grid sizes like 2×5 or 4×3.

### Step 2: Add Simple Flowers

```python
# Draw a field of simple flowers
for row in range(3):
    for col in range(4):
        x = 120 + col * 180
        y = 120 + row * 180

        # Flower center
        can.circle(x, y, 20, fill=CreativeGardenPalette.LEMON_CHIFFON,
                   stroke='#000', stroke_width=2)

        # 4 petals (top, right, bottom, left)
        can.circle(x, y - 30, 25, fill=CreativeGardenPalette.PEACH_WHISPER,
                   stroke='#000', stroke_width=1.5)
        can.circle(x + 30, y, 25, fill=CreativeGardenPalette.PEACH_WHISPER,
                   stroke='#000', stroke_width=1.5)
        can.circle(x, y + 30, 25, fill=CreativeGardenPalette.PEACH_WHISPER,
                   stroke='#000', stroke_width=1.5)
        can.circle(x - 30, y, 25, fill=CreativeGardenPalette.PEACH_WHISPER,
                   stroke='#000', stroke_width=1.5)
```

**Try it:** Add a stem to each flower using `can.line()`.

### Step 3: Create Alternating Patterns

```python
# Create a checkerboard pattern of flower colors
for row in range(4):
    for col in range(5):
        x = 100 + col * 140
        y = 100 + row * 140

        # Use modulo to alternate colors in a checkerboard pattern
        if (row + col) % 2 == 0:
            petal_color = CreativeGardenPalette.ROSE_QUARTZ
        else:
            petal_color = CreativeGardenPalette.LILAC_DREAM

        # Flower center
        can.circle(x, y, 18, fill=CreativeGardenPalette.BUTTER_YELLOW,
                   stroke='#000', stroke_width=2)

        # 4 petals with alternating colors
        can.circle(x, y - 28, 22, fill=petal_color,
                   stroke='#000', stroke_width=1.5)
        can.circle(x + 28, y, 22, fill=petal_color,
                   stroke='#000', stroke_width=1.5)
        can.circle(x, y + 28, 22, fill=petal_color,
                   stroke='#000', stroke_width=1.5)
        can.circle(x - 28, y, 22, fill=petal_color,
                   stroke='#000', stroke_width=1.5)
```

**How checkerboard logic works:**
- `(row + col) % 2` alternates between 0 and 1
- When row=0, col=0: (0+0) % 2 = 0 (even)
- When row=0, col=1: (0+1) % 2 = 1 (odd)
- When row=1, col=0: (1+0) % 2 = 1 (odd)
- When row=1, col=1: (1+1) % 2 = 0 (even)

This creates the classic checkerboard pattern!

**Challenge:** Create a pattern where colors change by row instead of in a checkerboard. Hint: Use just `row % 2` instead of `(row + col) % 2`.

## Common Issues

### Issue: Flowers overlap each other
**Solution:** Increase the spacing in your calculation. If flowers are 60 pixels wide, space them at least 80-100 pixels apart.

### Issue: Some flowers go off the edge
**Solution:** Calculate your maximum positions. With 5 columns starting at x=100 with 150-pixel spacing, the last column is at 100 + 4*150 = 700. Make sure this fits in your canvas!

### Issue: "NameError: name 'row' is not defined"
**Solution:** Make sure `row` is only used inside the outer loop, and `col` is only used inside the inner loop. Check your indentation.
