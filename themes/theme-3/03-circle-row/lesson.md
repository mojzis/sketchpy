## ⭕ Project 3: Circle Row

### Goal
Use a `for` loop to draw a row of overlapping circles, creating a beautiful chain pattern.

### What you'll learn
- Using `for` loops with `range()`
- Calculating positions with loop variables
- Creating patterns through repetition
- How many overlaps create deeper colors

### The Power of Loops
Instead of writing `can.circle()` five times, we can use a loop! The loop variable `i` helps us calculate where each circle should go.

### Position Formula
```python
x = 200 + i * 100
```
- When i=0: x = 200
- When i=1: x = 300
- When i=2: x = 400
- And so on!

### Steps
1. Use `for i in range(5):` to repeat 5 times
2. Calculate x position: `200 + i * 100`
3. Keep y position constant (300)
4. Draw a circle at (x, 300)

### Overlap Sweet Spot
With radius=60 and spacing of 100 pixels, circles overlap by 20 pixels - perfect for blending!

### Challenge
Try different values:
- `range(10)` - More circles!
- `i * 80` - Closer together (more overlap)
- `i * 120` - Further apart (less overlap)
