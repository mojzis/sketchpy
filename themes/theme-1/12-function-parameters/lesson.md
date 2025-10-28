## 🎨 Project 12: Customizable Cars

### Goal
Learn to make flexible, reusable functions by adding parameters that let you customize what the function draws.

### What you'll learn
- Adding parameters to make functions flexible
- Passing different arguments for different results
- Calculating proportional measurements
- Understanding the difference between parameters and arguments
- Creating truly reusable code

### Autocomplete Tip
Type `can.` to see Canvas methods! Press **Enter** to insert working example code with all parameters. Then customize the values!

### Steps
1. Create a canvas: `can = Canvas(800, 600)`
2. Define a function with multiple parameters: `def draw_car(canvas, x, y, width, color):`
3. Use parameters in your drawing code instead of fixed values
4. Calculate proportional sizes (height based on width)
5. Call the function multiple times with different arguments
6. Draw a parking lot full of different cars!

### Understanding Parameters vs Arguments

**Parameters** = Variables in the function definition (the recipe)
```python
def draw_car(canvas, x, y, width, color):
    #         ↑ These are PARAMETERS
```

**Arguments** = Actual values you pass when calling (the ingredients)
```python
draw_car(can, 50, 200, 150, Color.RED)
#             ↑ These are ARGUMENTS
```

### Why Parameters Make Functions Powerful

Without parameters (limited):
```python
def draw_car(canvas):
    canvas.rect(200, 300, 150, 75, fill=Color.RED)
    # Always same position, size, color!
```

With parameters (flexible):
```python
def draw_car(canvas, x, y, width, color):
    canvas.rect(x, y, width, width * 0.5, fill=color)
    # Can draw ANY car, ANYWHERE, ANY size, ANY color!
```

### Proportional Calculations
Make related measurements proportional to parameters:
```python
height = width * 0.5  # Height is always 50% of width
wheel_radius = height * 0.3  # Wheel is 30% of height
front_wheel_x = x + width * 0.25  # 25% from left edge
```

This keeps your drawing looking good at any size!

### Coordinate System
The canvas coordinates start at the top-left (0, 0). X increases to the right, Y increases downward.

### Available Methods
- `can.rect(x, y, width, height, fill=..., stroke=..., stroke_width=...)`
- `can.circle(x, y, radius, fill=...)`
- `can.grid(spacing=50, show_coords=True)` - Show coordinate grid

### Example: Different Cars
```python
# Small red car
draw_car(can, 50, 200, 150, Color.RED)

# Large blue car
draw_car(can, 250, 250, 200, Color.BLUE)

# Tiny green car
draw_car(can, 500, 180, 100, Color.GREEN)
```

### Tips
- Start with position parameters (x, y) - most common to vary
- Add size parameters (width, height) for flexibility
- Add appearance parameters (color) last
- Use descriptive parameter names
- Calculate related values from parameters for proportionality

### Challenge
Can you add more parameters? Try adding:
- `wheel_color` - customize wheel color
- `has_windows` - boolean to show/hide windows
- `roof_height` - vary the roof size
- `num_doors` - draw different number of doors
