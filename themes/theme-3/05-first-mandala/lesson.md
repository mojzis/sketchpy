## ⭕ Project 5: First Mandala

### Goal
Create your first spirograph-style mandala by arranging 8 circles around a center point using trigonometry!

### What you'll learn
- Importing the `math` module
- Using `math.pi`, `math.cos()`, and `math.sin()`
- Converting angles to positions
- Creating circular arrangements

### Circle Math Magic
To place circles evenly around a point, we use:
```python
angle = (i / num_circles) * 2 * math.pi  # Full rotation
x = center_x + radius * math.cos(angle)
y = center_y + radius * math.sin(angle)
```

### What's Happening?
- `math.pi` is approximately 3.14159...
- `2 * math.pi` = full circle (360 degrees)
- `math.cos(angle)` = horizontal distance
- `math.sin(angle)` = vertical distance

### Steps
1. Import math: `import math`
2. Set center point and orbit radius
3. Loop through `range(8)` for 8 circles
4. Calculate angle for each circle
5. Use cos/sin to find x, y positions
6. Draw circle at (x, y)

### Mandala Variations
- `range(6)` - Hexagon pattern
- `range(12)` - Dense mandala
- Change `orbit_radius` to 100 or 200
- Change `circle_size` to 60 or 120

### Challenge
Can you make a double-ring mandala? Use two different `orbit_radius` values!
