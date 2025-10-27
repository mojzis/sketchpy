## 🏢 Lesson 8: Multi-Story Parking Garage

### Goal
Create a grid of cars arranged in rows and columns using nested loops, like a multi-story parking garage.

### What you'll learn
- Using nested loops (loop inside a loop)
- Creating 2D grid patterns
- Calculating positions for rows and columns
- Combining loops with conditionals
- Creating alternating patterns

### Autocomplete Tip
Type `can.` to see Canvas methods! Press **Tab** or **Enter** to insert working example code with all parameters. Then customize the values!

### Steps
1. Create outer loop for rows: `for row in range(3):`
2. Create inner loop for columns: `for col in range(4):`
3. Calculate x position based on column: `x = 50 + col * 180`
4. Calculate y position based on row: `y = 100 + row * 180`
5. Use `(row + col) % 2` to create alternating colors
6. Draw car body and wheels at calculated position

### Understanding Nested Loops
```python
# Outer loop runs 3 times
for row in range(3):
    # Inner loop runs 4 times for EACH row
    for col in range(4):
        # This code runs 3 × 4 = 12 times total
        x = 50 + col * 180  # col changes faster
        y = 100 + row * 180 # row changes slower
```

**Pattern of execution:**
- Row 0: col 0, 1, 2, 3
- Row 1: col 0, 1, 2, 3
- Row 2: col 0, 1, 2, 3

### Coordinate System
The canvas coordinates start at the top-left (0, 0). X increases to the right, Y increases downward.

### Available Methods
- `can.rect(x, y, width, height, fill=...)`
- `can.circle(x, y, radius, fill=...)`
- `can.grid(spacing=50, show_coords=True)` - Show coordinate grid
- `can.show_palette(PaletteClass)` - Display palette colors

### Alternating Colors
```python
# Using modulo (%) to alternate
if (row + col) % 2 == 0:
    color = Color.RED  # Even positions
else:
    color = Color.BLUE # Odd positions
```

**Why this works:**
- When row + col is even (0, 2, 4...), we get one color
- When row + col is odd (1, 3, 5...), we get another color
- Creates a checkerboard pattern

### Color Palettes
**Basic Colors:** `Color.RED`, `Color.BLUE`, `Color.GREEN`, `Color.YELLOW`, `Color.BLACK`, `Color.GRAY`

### Tips
- Start with small numbers (2 rows × 3 cols) to see the pattern
- Use `can.grid()` to visualize the coordinate system
- Adjust spacing by changing the multiplier (180)
- The inner loop completes fully before outer loop advances

### Challenge
- Change to 4 rows × 5 columns
- Try different color patterns: `row % 2`, `col % 3`, `(row * col) % 2`
- Make spacing smaller to fit more cars
- Add windows to the cars: `can.rect(x + 10, y + 20, 30, 25, fill=Color.CYAN)`
- Create a gradient effect where color changes based on row or column number
