## Additional Help

### Common Issues

**Loop only runs once?**
- Check indentation - code inside the loop must be indented
- Make sure you're using a colon `:` after the for statement
- Example: `for i in range(5):` (don't forget the colon!)

**All cars in same spot?**
- You must use the loop variable `i` in your position calculation
- Wrong: `x = 100` (same every time)
- Right: `x = 100 + i * 150` (different each time)

**Getting an error about 'i'?**
- Make sure `i` is only used inside the loop (below the for statement)
- Check that it's indented properly

### Loop Basics

**What is a loop?**
A loop repeats code multiple times without copying/pasting:

```python
# Without loop (repetitive!)
can.circle(50, 300, 20, fill=Color.RED)
can.circle(200, 300, 20, fill=Color.RED)
can.circle(350, 300, 20, fill=Color.RED)

# With loop (clean!)
for i in range(3):
    x = 50 + i * 150
    can.circle(x, 300, 20, fill=Color.RED)
```

**Understanding range():**
```python
range(5)   # → 0, 1, 2, 3, 4 (five numbers starting from 0)
range(10)  # → 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 (ten numbers)
range(1)   # → 0 (just one number)
```

### Position Math

**Spacing items evenly:**
```python
starting_x = 50      # Where first item goes
spacing = 150        # Gap between items

for i in range(5):
    x = starting_x + i * spacing
    # i=0: x = 50 + 0*150 = 50
    # i=1: x = 50 + 1*150 = 200
    # i=2: x = 50 + 2*150 = 350
    # i=3: x = 50 + 3*150 = 500
    # i=4: x = 50 + 4*150 = 650
```

**Vertical spacing:**
```python
for i in range(4):
    y = 100 + i * 100  # Each row 100 pixels lower
    can.rect(200, y, 80, 50, fill=Color.BLUE)
```

### Common Patterns

**Draw a row of shapes:**
```python
for i in range(8):
    x = 50 + i * 90
    can.circle(x, 300, 30, fill=Color.GREEN)
```

**Draw with different colors:**
```python
colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE]

for i in range(5):
    x = 50 + i * 150
    can.rect(x, 200, 100, 60, fill=colors[i])
```

**Draw with varying sizes:**
```python
for i in range(6):
    x = 100 + i * 100
    size = 20 + i * 10  # Each circle bigger
    can.circle(x, 300, size, fill=Color.PURPLE)
```

**Preview of nested loops (grid):**
```python
# This creates a 3×3 grid
for row in range(3):
    for col in range(3):
        x = 100 + col * 100
        y = 100 + row * 100
        can.circle(x, y, 20, fill=Color.BLUE)
```

### Tips

- The loop variable `i` is just a name - you can use other names like `car` or `count`
- Start with a small range (like 3) to test, then increase it
- Use variables for starting position and spacing to make adjustments easy:
  ```python
  start_x = 50
  spacing = 150
  for i in range(5):
      x = start_x + i * spacing
      can.rect(x, 300, 120, 60, fill=Color.RED)
  ```
- Print the loop variable to understand what's happening: `print(f"Drawing car {i} at x={x}")`
