# Help: Geometric Patterns

## Quick Reference

### Nested Loop Syntax
```python
for row in range(3):           # Outer loop (rows)
    for col in range(4):       # Inner loop (columns)
        # This runs 3 × 4 = 12 times
        x = start_x + col * spacing_x
        y = start_y + row * spacing_y
```

### Grid Position Calculation
```python
# For a grid starting at (100, 100) with 150-pixel spacing:
x = 100 + col * 150  # Column controls horizontal
y = 100 + row * 150  # Row controls vertical

# Row 0, Col 0: (100, 100)
# Row 0, Col 1: (250, 100)
# Row 1, Col 0: (100, 250)
# Row 1, Col 1: (250, 250)
```

### Checkerboard Pattern
```python
if (row + col) % 2 == 0:
    color = Color1  # Even positions
else:
    color = Color2  # Odd positions
```

## Common Errors

### Error: "NameError: name 'col' is not defined"
**What it means:** Using `col` outside the inner loop
**How to fix:** Make sure code using `col` is indented inside the `for col in range():` loop

### Error: All items appear in a vertical line
**What it means:** Not using `col` in the x calculation
**How to fix:** Use `x = start + col * spacing`, not just `x = start`

### Error: All items appear in a horizontal line
**What it means:** Not using `row` in the y calculation
**How to fix:** Use `y = start + row * spacing`, not just `y = start`

### Error: Items overlap or are too close
**What it means:** Spacing is too small for the size of your shapes
**How to fix:** If shapes are 50 pixels wide, space them at least 70-80 pixels apart

## Debugging Tips

1. **Print positions:** Add `print(f"Row {row}, Col {col}: ({x}, {y})")` to see all positions
2. **Start small:** Test with `range(2)` for both loops (just 4 items total)
3. **Draw just centers:** Start by drawing only the centers, then add petals once positions are correct
4. **Use the grid:** Verify positions match where you expect them on the coordinate grid

## Understanding Nested Loop Order

```python
for row in range(2):
    for col in range(3):
        print(f"Row {row}, Col {col}")

# Output:
# Row 0, Col 0
# Row 0, Col 1
# Row 0, Col 2
# Row 1, Col 0
# Row 1, Col 1
# Row 1, Col 2
```

The inner loop (col) completes all its iterations before the outer loop (row) moves to the next value.

## Checkerboard Pattern Logic

```python
(row + col) % 2

# Creates this pattern for a 3×3 grid:
# 0 1 0
# 1 0 1
# 0 1 0

# Use with if/else to alternate colors:
if (row + col) % 2 == 0:
    # Even positions (0)
else:
    # Odd positions (1)
```

## Related Lessons
- **Lesson 2:** Single loops - now we're stacking loops
- **Next:** Lesson 4 adds text labels to your patterns

## Extra Challenges

1. **Bigger field:** Create a 5×6 or 6×4 grid
2. **Diagonal pattern:** Use `row == col` to color the diagonal differently
3. **Row stripes:** Color changes every row using `row % 2`
4. **Column stripes:** Color changes every column using `col % 2`
5. **Size variation:** Make flowers smaller as they go up (farther away)
6. **Three colors:** Use `(row + col) % 3` to cycle through three colors
