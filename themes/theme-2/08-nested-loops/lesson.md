# Nested Loops

## What You'll Learn
- **Programming:** Nested loop mechanics, 2D grid calculations, modulo operator for patterns
- **Drawing:** Creating a full flower field with rows and columns

## Nested Loops Revisited

You learned about nested loops in Lesson 3. Now we'll use them with lists and more complex patterns!

```python
for row in range(3):          # Outer loop: rows
    for col in range(4):      # Inner loop: columns
        # Runs 3 × 4 = 12 times total
```

The key insight: **outer loop controls rows (y), inner loop controls columns (x)**.

## The Modulo Operator (%)

The modulo operator `%` gives you the remainder after division. It's perfect for creating alternating patterns:

```python
0 % 2 = 0    # 0 divided by 2 = 0 remainder 0
1 % 2 = 1    # 1 divided by 2 = 0 remainder 1
2 % 2 = 0    # 2 divided by 2 = 1 remainder 0
3 % 2 = 1    # 3 divided by 2 = 1 remainder 1
```

This creates the pattern: 0, 1, 0, 1, 0, 1... perfect for checkerboards!

## Instructions

### Step 1: Create a Flower Field

```python
from sketchpy.shapes import Canvas, CreativeGardenPalette

can = Canvas(800, 600)
can.grid(spacing=50, show_coords=True)

# Draw sky and ground
can.rect(0, 0, 800, 300, fill=CreativeGardenPalette.SKY_BREEZE)
can.rect(0, 300, 800, 300, fill=CreativeGardenPalette.MINT_CREAM)

# Draw a 4×5 field of flowers (4 rows, 5 columns)
for row in range(4):
    for col in range(5):
        x = 100 + col * 130
        y = 350 + row * 80

        # Draw simple flower
        can.circle(x, y, 18, fill=CreativeGardenPalette.BUTTER_YELLOW,
                   stroke='#000', stroke_width=2)

        # 4 petals
        can.circle(x, y - 25, 20, fill=CreativeGardenPalette.ROSE_QUARTZ,
                   stroke='#000', stroke_width=1.5)
        can.circle(x + 25, y, 20, fill=CreativeGardenPalette.ROSE_QUARTZ,
                   stroke='#000', stroke_width=1.5)
        can.circle(x, y + 25, 20, fill=CreativeGardenPalette.ROSE_QUARTZ,
                   stroke='#000', stroke_width=1.5)
        can.circle(x - 25, y, 20, fill=CreativeGardenPalette.ROSE_QUARTZ,
                   stroke='#000', stroke_width=1.5)
```

**Try it:** Change `range(4)` and `range(5)` to create different field sizes.

### Step 2: Add Checkerboard Pattern

```python
# Create checkerboard pattern with two colors
for row in range(4):
    for col in range(6):
        x = 90 + col * 120
        y = 350 + row * 80

        # Alternate colors using modulo
        if (row + col) % 2 == 0:
            petal_color = CreativeGardenPalette.LILAC_DREAM
        else:
            petal_color = CreativeGardenPalette.PEACH_WHISPER

        can.circle(x, y, 18, fill=CreativeGardenPalette.LEMON_CHIFFON,
                   stroke='#000', stroke_width=2)

        can.circle(x, y - 25, 20, fill=petal_color,
                   stroke='#000', stroke_width=1.5)
        can.circle(x + 25, y, 20, fill=petal_color,
                   stroke='#000', stroke_width=1.5)
        can.circle(x, y + 25, 20, fill=petal_color,
                   stroke='#000', stroke_width=1.5)
        can.circle(x - 25, y, 20, fill=petal_color,
                   stroke='#000', stroke_width=1.5)
```

**How checkerboard works:**
- (row=0, col=0): (0+0) % 2 = 0 (even - first color)
- (row=0, col=1): (0+1) % 2 = 1 (odd - second color)
- (row=1, col=0): (1+0) % 2 = 1 (odd - second color)
- (row=1, col=1): (1+1) % 2 = 0 (even - first color)

**Try it:** Use just `row % 2` instead of `(row + col) % 2` to create row stripes instead.

### Step 3: Vary Size by Row

```python
# Make flowers smaller as they go up (depth effect)
for row in range(4):
    for col in range(5):
        x = 100 + col * 130
        y = 350 + row * 80

        # Flowers in front (higher row number) are bigger
        size_multiplier = 1.0 + (row * 0.15)  # 1.0, 1.15, 1.3, 1.45
        center_size = int(18 * size_multiplier)
        petal_size = int(20 * size_multiplier)
        petal_distance = int(25 * size_multiplier)

        can.circle(x, y, center_size,
                   fill=CreativeGardenPalette.BUTTER_YELLOW,
                   stroke='#000', stroke_width=2)

        can.circle(x, y - petal_distance, petal_size,
                   fill=CreativeGardenPalette.CORAL_BLUSH,
                   stroke='#000', stroke_width=1.5)
        can.circle(x + petal_distance, y, petal_size,
                   fill=CreativeGardenPalette.CORAL_BLUSH,
                   stroke='#000', stroke_width=1.5)
        can.circle(x, y + petal_distance, petal_size,
                   fill=CreativeGardenPalette.CORAL_BLUSH,
                   stroke='#000', stroke_width=1.5)
        can.circle(x - petal_distance, y, petal_size,
                   fill=CreativeGardenPalette.CORAL_BLUSH,
                   stroke='#000', stroke_width=1.5)
```

This creates a perspective effect - front row looks closer!

**Challenge:** Combine patterns - use checkerboard colors AND size variation together. Can you create a diagonal gradient using `row + col`?

## Common Issues

### Issue: Flowers only appear in one row or column
**Solution:** Make sure you're using both `row` in the y calculation and `col` in the x calculation.

### Issue: Unexpected pattern results
**Solution:** Print the values: `print(f"row={row}, col={col}, (row+col)%2={(row+col)%2}")` to debug your pattern logic.

### Issue: Flowers overlap
**Solution:** Increase spacing values in your calculations. Flowers need enough room!
