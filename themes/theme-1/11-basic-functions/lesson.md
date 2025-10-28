## 🏭 Project 11: Vehicle Factory

### Goal
Learn to write and use functions by creating a vehicle factory that can draw different types of vehicles (cars, trucks, sports cars).

### What you'll learn
- Defining functions with `def`
- Understanding functions as reusable code blocks
- Calling functions to execute them
- Passing the canvas as a parameter
- Code organization and reusability

### Autocomplete Tip
Type `can.` to see Canvas methods! Press **Enter** to insert working example code with all parameters. Then customize the values!

### Steps
1. Create a canvas: `can = Canvas(800, 600)`
2. Define a function with `def function_name(canvas):`
3. Inside the function, write code to draw a vehicle
4. Call the function to execute it: `function_name(can)`
5. Create multiple functions for different vehicle types
6. Call each function to draw your vehicle factory

### Understanding Functions
Functions are like **recipes** - they're instructions you write once and can use many times!

```python
def draw_simple_car(canvas):
    # These instructions run when you call the function
    canvas.rect(200, 300, 200, 80, fill=Color.RED)
    canvas.circle(250, 390, 25, fill=Color.BLACK)
    # ... more drawing code

# Call the function to use it
draw_simple_car(can)
```

**Why use functions?**
- **Reusability**: Write code once, use it many times
- **Organization**: Keep related code together
- **Clarity**: Give meaningful names to complex operations
- **No copying**: Update in one place, changes apply everywhere

### Function Anatomy
```python
def function_name(parameter):
    """This is a docstring - explains what the function does"""
    # Function body - the code that runs
    # Indented 4 spaces
    canvas.rect(...)
```

### Coordinate System
The canvas coordinates start at the top-left (0, 0). X increases to the right, Y increases downward.

### Available Methods
- `can.rect(x, y, width, height, fill=...)`
- `can.circle(x, y, radius, fill=...)`
- `can.grid(spacing=50, show_coords=True)` - Show coordinate grid

### Tips
- Give functions descriptive names: `draw_truck()` not `function1()`
- Use docstrings to explain what your function does
- Test each function individually before calling them all
- Functions can call other functions!

### Challenge
Can you create a third vehicle function? Try `draw_sports_car()` or `draw_bus()`! Make it visually different from the car and truck.
