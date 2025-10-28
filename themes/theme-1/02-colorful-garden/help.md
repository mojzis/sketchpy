## Loop Examples

### Drawing Multiple Shapes
```python
# Draw 5 circles in a row
for i in range(5):
    x = 100 + i * 100
    can.circle(x, 200, 30, fill=Color.RED)
```

### Varying Colors
```python
colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE]
for i, color in enumerate(colors):
    x = 100 + i * 100
    can.circle(x, 200, 30, fill=color)
```

### Creating a Grid
```python
for row in range(3):
    for col in range(4):
        x = 100 + col * 150
        y = 100 + row * 150
        can.circle(x, y, 30, fill=Color.BLUE)
```
