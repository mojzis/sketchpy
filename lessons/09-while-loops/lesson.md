## 🚦 Lesson 9: Traffic Jam

### Goal
Create a traffic jam by drawing cars until the canvas is full using a while loop with conditions.

### What you'll learn
- Using while loops for condition-based repetition
- Updating loop variables (counters)
- Understanding loop exit conditions
- Comparing while vs for loops
- Using conditionals inside loops

### Autocomplete Tip
Type `can.` to see Canvas methods! Press **Tab** or **Enter** to insert working example code with all parameters. Then customize the values!

### Steps
1. Create variables for starting position: `x = 50`, `y = 300`
2. Start while loop with condition: `while x < 750:`
3. Draw car at current position
4. Update x position: `x = x + 120`
5. Optional: Use if statement to vary y position

### Understanding While Loops
```python
x = 50                 # Initialize counter
while x < 750:         # Condition - keep going while true
    # Draw something at x
    x = x + 120        # Update counter - IMPORTANT!
```

**Key differences from for loops:**
- `for` loop: "Do this N times"
- `while` loop: "Do this until condition is false"

**Warning:** Forgetting to update `x` creates an infinite loop!

### Loop Variables
You need to:
1. **Initialize** before the loop: `x = 50`
2. **Check condition** in while statement: `while x < 750:`
3. **Update** inside the loop: `x = x + 120`

### Coordinate System
The canvas coordinates start at the top-left (0, 0). X increases to the right, Y increases downward.

### Available Methods
- `can.rect(x, y, width, height, fill=...)`
- `can.circle(x, y, radius, fill=...)`
- `can.grid(spacing=50, show_coords=True)` - Show coordinate grid
- `can.show_palette(PaletteClass)` - Display palette colors

### Conditional Updates
```python
x = 50
y = 300

while x < 750:
    # Draw car
    can.rect(x, y, 100, 60, fill=Color.RED)

    x = x + 120

    # Change y after reaching middle
    if x > 400:
        y = y + 20
```

This makes cars shift downward after a certain point!

### Color Palettes
**Basic Colors:** `Color.RED`, `Color.BLUE`, `Color.GREEN`, `Color.YELLOW`, `Color.ORANGE`, `Color.BLACK`, `Color.GRAY`

### Using Counters
You can use a counter to limit iterations:

```python
x = 50
count = 0

while x < 750 and count < 6:  # Stop after 6 cars OR when full
    # Draw car
    x = x + 120
    count = count + 1  # Increment counter
```

### Tips
- Always update your loop variable or the loop never ends!
- Test your condition: what value makes it false?
- Start with a simple condition, add complexity later
- You can combine conditions: `while x < 750 and y < 500:`
- Use print() to debug: `print(f"Drawing car at x={x}")`

### Challenge
- Add a counter to stop after exactly 6 cars
- Make cars alternate colors (use counter % 2)
- Create a second lane (another while loop with different y)
- Vary spacing: `x = x + 100 + (count * 10)` for increasing gaps
- Add condition to change color after x > 400
- Make the loop stop when count reaches 8, even if space remains
