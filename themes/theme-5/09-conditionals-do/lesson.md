## 🎯 Your Turn: Smart Traffic

### Goal
Use conditionals to create intelligent traffic patterns.

### Your Mission
Create a scene that uses `if/else` to make decisions about what to draw.

### Steps
1. Use a loop to create multiple vehicles
2. Add `if/else` to make choices:
   - Alternate colors
   - Different car types
   - Different sizes
   - Different positions

### Patterns to Try
```python
# Alternating colors
if i % 2 == 0:
    color = Color.BLUE
else:
    color = Color.RED

# Size based on position
if i < 3:
    width = 100
else:
    width = 140

# Car type based on condition
if i % 3 == 0:
    cars.bus(can, x, y, color=color)
elif i % 3 == 1:
    cars.sports_car(can, x, y, color=color)
else:
    cars.rounded_car(can, x, y, color=color)
```

### Ideas
- Create a 3-color pattern (red, yellow, green)
- Make every third car a bus
- Alternate between top and bottom lane
- Create size gradient (small to large)
- Mix simple_car, rounded_car, sports_car

### Tips
- `%` (modulo) gives remainder: `5 % 2 = 1`, `6 % 2 = 0`
- `i % 2 == 0` checks if even
- `i % 3 == 0` checks if divisible by 3
- Combine conditions with `and`/`or`

### Challenge
Create a full traffic system:
- 2 lanes going opposite directions
- Traffic lights controlling each lane
- Different vehicle types based on lane
- Cars stop at red lights (draw closer to light)
