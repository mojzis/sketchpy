## ⭕ Project 9: Growing Spiral

### Goal
Use a `while` loop to create a spiral that grows outward until it reaches the edge of the canvas.

### What you'll learn
- Using `while` loops instead of `for` loops
- Condition-based iteration (loop until something happens)
- Creating spirals with increasing radius
- When to use `while` vs `for`

### While Loops vs For Loops
- **For loop**: "Do this exactly N times"
- **While loop**: "Keep doing this until a condition is met"

```python
while radius < 250:  # Keep going until radius gets too big
    # Draw circle
    radius = radius + 15  # Grow the radius
    angle = angle + 0.5   # Rotate a bit
```

### Spiral Formula
Each circle is:
- A bit further from center (radius increases)
- Rotated from the last one (angle increases)

```python
x = center_x + radius * math.cos(angle)
y = center_y + radius * math.sin(angle)
```

### Steps
1. Initialize `radius = 0` and `angle = 0`
2. Use `while radius < 250:` to loop
3. Calculate x, y from radius and angle
4. Draw circle
5. Increase radius and angle

### Infinite Loop Warning!
Always make sure the condition will eventually become False, or the loop never stops!

### Challenge
- Make it spiral faster: Increase angle by 0.8
- Make it grow slower: Increase radius by 10
- Fade as it grows: `opacity = 0.4 - (radius / 1000)`
