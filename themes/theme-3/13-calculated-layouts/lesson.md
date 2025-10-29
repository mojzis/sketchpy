## ⭕ Project 13: Calculated Layouts

### Goal
Create functions that calculate and return positions, then use those positions to draw perfectly spaced mandalas.

### What you'll learn
- Functions that return values
- Using `return` statement
- Capturing returned values in variables
- Separating calculation from drawing

### Functions That Calculate
Some functions don't draw - they calculate and return a value:

```python
def circle_position(center_x, center_y, radius, angle):
    """Calculate x, y position on a circle"""
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    return x, y  # Return two values!
```

Then use it:
```python
x, y = circle_position(400, 300, 150, math.pi)
draw_mandala(can, x, y)
```

### Why This Is Powerful
- **Reusable math**: Use the calculation many times
- **Cleaner code**: Separate "where" from "what"
- **Easy to change**: Modify layout without touching drawing code

### Steps
1. Create `circle_position()` function that returns x, y
2. Create a loop that calculates positions
3. At each position, draw a mandala
4. Result: Perfect circular arrangement of mandalas!

### Return Values
`return` sends a value back to the caller:
```python
result = my_function(10, 20)  # result gets the returned value
```

### Challenge
- Create `grid_position(row, col, spacing)` function
- Create `spiral_position(distance, angle)` function
- Use multiple layout functions in one composition!
