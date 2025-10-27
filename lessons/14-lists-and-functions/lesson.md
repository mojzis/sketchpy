## 🚦 Lesson 14: Lists + Functions - Building Scenes

### Goal
Learn to combine lists and functions for data-driven drawing. Create a traffic scene with multiple cars using dictionaries and loops.

### What you'll learn
- Using dictionaries to store structured data
- Separating data from drawing logic
- Processing lists of complex objects
- Building scalable, maintainable code
- Data-driven programming concepts

### Autocomplete Tip
Type `can.` to see Canvas methods! When working with dictionaries, type the variable name and `['` to see available keys.

### Steps
1. Study the `draw_car()` function - notice how it takes a dictionary parameter
2. Look at the `cars_in_scene` list - each car is a dictionary with properties
3. See how the loop processes each car dictionary
4. Try adding a new car to the `cars_in_scene` list
5. Experiment with different car properties (position, size, color)
6. Create your own drawing function that takes a dictionary

### Key Concept: Data-Driven Programming
Instead of writing repetitive code for each car, we:
1. Define a function that knows HOW to draw a car
2. Create a list of data describing WHAT cars to draw
3. Loop through the data and call the function

This separation makes it easy to add, remove, or modify objects without changing the drawing logic!

### Understanding Dictionaries
```python
# A dictionary stores key-value pairs
car = {
    'x': 100,
    'y': 200,
    'width': 150,
    'height': 80,
    'color': Color.RED
}

# Access values using keys
print(car['x'])  # Prints: 100
print(car['color'])  # Prints: Color.RED

# Use in drawing
can.rect(car['x'], car['y'], car['width'], car['height'], fill=car['color'])
```

### The Pattern
```python
# 1. Define function that takes structured data
def draw_car(canvas, car_data):
    canvas.rect(
        car_data['x'],
        car_data['y'],
        car_data['width'],
        car_data['height'],
        fill=car_data['color']
    )

# 2. Create list of data
cars = [
    {'x': 50, 'y': 300, 'width': 150, 'height': 80, 'color': Color.RED},
    {'x': 250, 'y': 320, 'width': 180, 'height': 90, 'color': Color.BLUE},
]

# 3. Process all data
for car in cars:
    draw_car(can, car)
```

### Available Methods
- `can.rect(x, y, width, height, fill=...)` - Draw rectangles
- `can.circle(x, y, radius, fill=...)` - Draw circles
- `can.grid(spacing=50, show_coords=True)` - Show coordinate grid
- All color palettes: `Color`, `CreativeGardenPalette`, `CalmOasisPalette`

### Challenge
1. Add 2-3 more cars to the `cars_in_scene` list
2. Create a `draw_tree()` function that takes a dictionary with tree properties
3. Create a list of trees and draw them all
4. Add a `speed` property to each car and use it to determine color
5. Create different car types (compact, sedan, truck) based on a `type` property

### Why This Matters
- **Scalability**: Easy to add 100 cars instead of 3
- **Maintainability**: Change drawing logic in one place
- **Readability**: Data is separate and easy to understand
- **Flexibility**: Same function works for any car data
- **Real-world**: This pattern is used in game development, data visualization, and web apps!

### Tips
- Use consistent key names in your dictionaries
- Document what keys your functions expect
- Start with simple dictionaries and add properties as needed
- Think about what data describes your object vs. how to draw it
