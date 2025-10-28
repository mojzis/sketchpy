# Colorful Garden

## What You'll Learn
- **Programming:** For loops with `range()`, loop variables, basic iteration
- **Drawing:** Creating multiple flowers with different positions

## Why Use Loops?

Imagine you want to draw 5 flowers. You could copy-paste the same code 5 times, but what if you wanted 10 flowers? Or 100? That would be exhausting!

Loops let you repeat code automatically. Instead of writing the same thing over and over, you tell Python "do this 5 times" and it handles the repetition for you.

## The For Loop

A `for` loop repeats a block of code a specific number of times:

```python
for i in range(5):
    # This code runs 5 times
    # i will be 0, then 1, then 2, then 3, then 4
```

The variable `i` (short for "index") automatically changes each time through the loop. You can use it to calculate different positions for each flower!

## Instructions

### Step 1: Draw Flowers in a Row

```python
from sketchpy.shapes import Canvas, CreativeGardenPalette

can = Canvas(800, 600)
can.grid(spacing=50, show_coords=True)

# Draw 5 flowers in a horizontal row
for i in range(5):
    x = 100 + i * 150  # Each flower is 150 pixels apart
    y = 300            # All at the same height

    # Draw flower center
    can.circle(x, y, 25, fill=CreativeGardenPalette.BUTTER_YELLOW,
               stroke='#000', stroke_width=2)

    # Draw simple petals (4 petals for simplicity)
    can.circle(x, y - 35, 30, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=2)
    can.circle(x + 35, y, 30, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=2)
    can.circle(x, y + 35, 30, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=2)
    can.circle(x - 35, y, 30, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=2)
```

**How it works:**
- When `i = 0`: x = 100 + 0 * 150 = 100
- When `i = 1`: x = 100 + 1 * 150 = 250
- When `i = 2`: x = 100 + 2 * 150 = 400
- And so on!

**Try it:** Change `range(5)` to `range(3)` or `range(7)` to draw different numbers of flowers.

### Step 2: Understanding `range()`

The `range()` function creates a sequence of numbers:
- `range(5)` gives you: 0, 1, 2, 3, 4 (5 numbers starting from 0)
- `range(3)` gives you: 0, 1, 2
- `range(10)` gives you: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9

**Try it:** Add `print(f"Drawing flower {i} at position {x}")` inside your loop to see the values.

### Step 3: Make It More Interesting

```python
# Draw flowers at different heights to look more natural
for i in range(6):
    x = 80 + i * 120
    y = 250 + (i % 2) * 80  # Alternating heights: 250, 330, 250, 330...

    # Flower center
    can.circle(x, y, 25, fill=CreativeGardenPalette.BUTTER_YELLOW,
               stroke='#000', stroke_width=2)

    # 4 petals
    can.circle(x, y - 35, 30, fill=CreativeGardenPalette.LILAC_DREAM,
               stroke='#000', stroke_width=2)
    can.circle(x + 35, y, 30, fill=CreativeGardenPalette.LILAC_DREAM,
               stroke='#000', stroke_width=2)
    can.circle(x, y + 35, 30, fill=CreativeGardenPalette.LILAC_DREAM,
               stroke='#000', stroke_width=2)
    can.circle(x - 35, y, 30, fill=CreativeGardenPalette.LILAC_DREAM,
               stroke='#000', stroke_width=2)

    # Stem
    can.line(x, y + 25, x, 500, stroke=CreativeGardenPalette.MINT_CREAM,
             stroke_width=6)
```

The `%` operator (called "modulo") gives you the remainder after division:
- `0 % 2 = 0` (0 divided by 2 = 0 remainder 0)
- `1 % 2 = 1` (1 divided by 2 = 0 remainder 1)
- `2 % 2 = 0` (2 divided by 2 = 1 remainder 0)
- `3 % 2 = 1` (3 divided by 2 = 1 remainder 1)

This creates an alternating pattern!

**Challenge:** Create a two-row garden by using a second loop below the first, or by calculating different y positions.

## Common Issues

### Issue: All flowers appear in the same spot
**Solution:** Make sure you're using the loop variable `i` in your position calculation. You need something like `x = 100 + i * 150`, not just `x = 100`.

### Issue: "NameError: name 'i' is not defined"
**Solution:** The variable `i` only exists inside the loop. Make sure all code using `i` is indented under the `for` statement.

### Issue: My flowers go off the edge
**Solution:** Check your math. If you have 5 flowers spaced 150 apart starting at x=100, the last one is at 100 + 4*150 = 700. Make sure this fits in your canvas width!
