## 🔄 Lesson 13: Return Values

### Goal
Learn how functions can calculate values and return them for use in your code. Draw a car using functions that return calculated positions and colors.

### What you'll learn
- Using `return` statements in functions
- Capturing returned values in variables
- Functions as calculations (not just actions)
- Using returned values to draw shapes
- Composing functions together

### Autocomplete Tip
When calling functions, type the function name and press **Tab** to see its parameters and documentation!

### Steps
1. Create a canvas: `can = Canvas(800, 600)`
2. Study the `calculate_wheel_positions()` function - notice it returns a list of positions
3. Study the `get_car_color()` function - notice it returns a color based on speed
4. See how the returned values are captured in variables
5. Experiment with different speeds to see different car colors
6. Try creating your own function that returns a value

### Key Concept: Return Values
Functions can do two things:
- **Action functions**: Perform an action (like drawing)
- **Calculation functions**: Calculate and return a value

Return values let you separate calculation logic from drawing logic, making your code more flexible and reusable.

### Understanding Return Statements
```python
def get_car_color(speed):
    if speed > 150:
        return Color.RED  # Function stops here and sends back RED
    elif speed > 100:
        return Color.ORANGE  # Or stops here and sends back ORANGE
    else:
        return Color.BLUE  # Or stops here and sends back BLUE

# Capture the returned value
car_color = get_car_color(180)  # car_color now contains Color.RED
```

### Available Methods
- `can.rect(x, y, width, height, fill=...)` - Draw rectangles
- `can.circle(x, y, radius, fill=...)` - Draw circles
- `can.grid(spacing=50, show_coords=True)` - Show coordinate grid
- All `Color` constants: `Color.RED`, `Color.BLUE`, etc.

### Challenge
1. Try different speed values (50, 120, 180) and see how the car color changes
2. Create a function `calculate_car_height(width)` that returns a proportional height
3. Create a function that returns different wheel sizes based on car width
4. Draw multiple cars with different speeds and colors

### Tips
- Return statements immediately exit the function and send back a value
- You can return any type of value: numbers, strings, colors, lists, dictionaries
- Functions that return values are great for calculations and decisions
- Use descriptive variable names when capturing returned values
