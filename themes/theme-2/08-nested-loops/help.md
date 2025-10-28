# Help: Nested Loops

## Quick Reference

### Nested Loop Pattern
```python
for row in range(rows):      # Outer: controls y position
    for col in range(cols):  # Inner: controls x position
        x = start_x + col * spacing_x
        y = start_y + row * spacing_y
        # Draw at (x, y)
```

### Modulo for Patterns
```python
# Checkerboard
(row + col) % 2  # Alternates: 0,1,0,1 in diagonal pattern

# Row stripes
row % 2          # Alternates by row: all 0s, all 1s, all 0s...

# Column stripes
col % 2          # Alternates by column

# Three-color pattern
(row + col) % 3  # Cycles: 0,1,2,0,1,2...
```

### Loop Execution Order
```python
for row in range(2):
    for col in range(3):
        print(f"({row},{col})")

# Output:
# (0,0) (0,1) (0,2)  <- First row completes
# (1,0) (1,1) (1,2)  <- Second row completes
```

## Common Errors

### Error: Only one row/column of items appears
**What it means:** Not using both loop variables in position calculations
**How to fix:**
- x must use `col`: `x = start + col * spacing`
- y must use `row`: `y = start + row * spacing`

### Error: Pattern doesn't match expectations
**What it means:** Wrong modulo formula for desired pattern
**How to fix:**
- Checkerboard: `(row + col) % 2`
- Rows: `row % 2`
- Columns: `col % 2`
- Print values to debug: `print(f"{row},{col}: {(row+col)%2}")`

### Error: Items overlap
**What it means:** Spacing too small for item sizes
**How to fix:** If items are 50px wide, space them at least 60-70px apart

## Debugging Tips

1. **Print positions:** Add `print(f"Row {row}, Col {col}: ({x},{y})")`
2. **Start small:** Test with `range(2)` for both loops (4 items total)
3. **Visualize the pattern:** Draw it on paper first
4. **Print modulo values:** `print(f"{row},{col}: {(row+col)%2}")` to see pattern

## Modulo Pattern Examples

### Checkerboard Pattern
```python
for row in range(4):
    for col in range(4):
        if (row + col) % 2 == 0:
            color = "white"
        else:
            color = "black"

# Pattern:
# W B W B
# B W B W
# W B W B
# B W B W
```

### Row Stripes
```python
if row % 2 == 0:
    color = "light"
else:
    color = "dark"

# Pattern:
# L L L L
# D D D D
# L L L L
# D D D D
```

### Column Stripes
```python
if col % 2 == 0:
    color = "light"
else:
    color = "dark"

# Pattern:
# L D L D
# L D L D
# L D L D
# L D L D
```

### Three-Color Diagonal
```python
colors = ["red", "green", "blue"]
color = colors[(row + col) % 3]

# Pattern:
# R G B R
# G B R G
# B R G B
# R G B R
```

## Position Calculation Examples

```python
# Basic grid
x = 100 + col * 50
y = 100 + row * 50

# Offset every other row (brick pattern)
x_offset = (row % 2) * 25  # 0 for even rows, 25 for odd
x = 100 + col * 50 + x_offset

# Vary spacing by row
row_spacing = 40 + row * 10  # Increases each row
y = 100 + row * row_spacing
```

## Related Lessons
- **Lesson 3:** First introduction to nested loops
- **Lesson 7:** Lists - combine with nested loops for complex data
- **Next:** Lesson 9 introduces while loops

## Extra Challenges

1. **Bigger field:** Create a 6×8 or larger grid
2. **Diagonal pattern:** Use `row == col` to highlight the diagonal
3. **Three colors:** Use `(row + col) % 3` for three-color pattern
4. **Size gradient:** Make flowers bigger in one direction
5. **Diamond pattern:** Use `abs(row - center) + abs(col - center)` for distance from center
6. **Brick offset:** Offset every other row like bricks: `x_offset = (row % 2) * 25`
