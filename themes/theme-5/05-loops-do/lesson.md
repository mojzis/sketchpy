## 🎯 Your Turn: Traffic Flow

### Goal
Use loops to create a busy traffic scene.

### Your Mission
Use a `for` loop to draw multiple vehicles in a pattern.

### Steps
1. Draw a road
2. Create a loop: `for i in range(???)`
3. Calculate x position: `x = ??? + i * ???`
4. Draw vehicles at that position
5. Experiment with different patterns!

### Pattern to Follow
```python
for i in range(???):  # How many vehicles?
    x = ??? + i * ???  # Starting position + spacing
    cars.rounded_car(can, x, y, ...)
```

### Tips
- Start vehicles at x=50 so they don't go off the edge
- Space them about 120-150 pixels apart (`i * 120`)
- Road at y=400, cars at y=350
- Try different car types in different loops

### Challenge Ideas
- Create 2 lanes with cars going different directions
- Make a parking lot grid (hint: use two loops, one inside the other!)
- Alternate colors: use `if i % 2 == 0:` to check even numbers
- Make cars get bigger as they go: `width = 100 + i * 10`

### Loop Inside Loop Example
```python
for row in range(3):
    for col in range(4):
        x = 50 + col * 150
        y = 200 + row * 100
        # Draw car at (x, y)
```
