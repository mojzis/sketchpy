## ⭕ Project 8: Grid of Mandalas

### Goal
Use nested loops to create a 3×3 grid of small mandalas, filling the canvas with repeating patterns.

### What you'll learn
- Nested loops (loop inside a loop)
- 2D grid calculations with row and column
- Creating complex patterns from simple building blocks
- How outer and inner loops work together

### Nested Loops Explained
```python
for row in range(3):      # Outer loop: 3 rows
    for col in range(3):  # Inner loop: 3 columns (runs 3 times per row!)
        # This code runs 3 × 3 = 9 times total
```

### Grid Position Formula
```python
x = 200 + col * 200  # Columns go left to right
y = 150 + row * 150  # Rows go top to bottom
```

### Steps
1. Outer loop for rows: `for row in range(3)`
2. Inner loop for columns: `for col in range(3)`
3. Calculate grid position from row and col
4. Draw a small mandala at that position
5. Each mandala needs its own mini-loop for circles!

### Triple-Nested Structure
- Outer loop: Rows
- Middle loop: Columns
- Inner loop: Circles in each mandala

### Challenge
- Make a 4×4 grid with `range(4)`
- Vary the colors by position: `colors[(row + col) % 3]`
- Make diagonal mandalas bigger: Check if `row == col`
