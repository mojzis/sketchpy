## 🎯 Your Turn: Build Your Function

### Goal
Create your own function that draws a custom scene.

### Your Mission
Define a function that draws something interesting, then call it multiple times.

### Steps
1. Define a function with `def function_name(parameters):`
2. Inside the function, draw shapes
3. Call your function with different parameters

### Function Template
```python
def draw_street_scene(x, y, color):
    """Draw a car on a street"""
    # Draw street
    can.rect(x, y, 200, 100, fill="#555555")

    # Draw car
    cars.rounded_car(can, x + 50, y + 30, color=color)

# Call it
draw_street_scene(100, 200, Color.BLUE)
draw_street_scene(400, 200, Color.RED)
```

### Function Ideas
- `draw_parking_spot()` - Draw parking lines and a car
- `draw_gas_station()` - Draw a building and a car
- `draw_car_lineup()` - Draw several cars in a row
- `draw_street_corner()` - Draw intersection with multiple cars

### Tips
- Parameters should be things you want to change each time
- Common parameters: x, y, color, size
- Keep functions simple at first
- Test by calling with different values

### Challenge
- Create 2 different functions
- Make one function call another function
- Use loops inside your function to draw multiple things
