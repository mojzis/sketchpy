## Pattern Recipes

### Checkerboard
```python
size = 50
for row in range(8):
    for col in range(8):
        if (row + col) % 2 == 0:
            x, y = col * size, row * size
            can.rect(x, y, size, size, fill=Color.BLACK)
```

### Concentric Circles
```python
cx, cy = 400, 300
for i in range(10):
    radius = 20 + i * 20
    can.circle(cx, cy, radius, outline=Color.BLUE)
```

### Triangle Pattern
```python
# Use polygon to draw triangles
for i in range(5):
    x = 100 + i * 100
    points = [(x, 100), (x+40, 150), (x-40, 150)]
    can.polygon(points, fill=Color.GREEN)
```
