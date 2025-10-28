## Additional Help

### Common Issues

**KeyError: 'x' or similar?**

- Check that your dictionary has the key you're trying to access
- Make sure all dictionaries in your list have the same keys
- Typo in key name? Dictionary keys are case-sensitive: `'X'` ≠ `'x'`

**Function doesn't accept dictionary?**

- Make sure you're passing the whole dictionary: `draw_car(can, car)`
- Not individual values: `draw_car(can, x, y, width, height)` (wrong for dict version)

**Loop not working with dictionary?**

- When looping over a list: `for car in cars:` gives you each dictionary
- To access values: `car['x']`, `car['y']`, etc.
- Don't loop over the dictionary itself when you want the list!

**Cars all look the same?**

- Check that you're using the dictionary values: `car_data['color']`
- Not hardcoded values: `Color.RED` (unless that's what you want)

### Understanding Dictionary Access

```python
# Creating a dictionary
car = {'x': 100, 'y': 200, 'color': Color.RED}

# Accessing values (CORRECT)
x_pos = car['x']  # Gets 100
car_color = car['color']  # Gets Color.RED

# Common mistakes (WRONG)
x_pos = car.x  # ERROR: dictionaries use brackets, not dots
x_pos = car('x')  # ERROR: use square brackets, not parentheses
```

### Dictionary Best Practices

**Use consistent keys:**

```python
# Good - all cars have same keys
cars = [
    {'x': 50, 'y': 300, 'color': Color.RED},
    {'x': 150, 'y': 300, 'color': Color.BLUE},
    {'x': 250, 'y': 300, 'color': Color.GREEN},
]

# Problematic - inconsistent keys
cars = [
    {'x': 50, 'y': 300, 'color': Color.RED},
    {'x': 150, 'y': 300, 'colour': Color.BLUE},  # Typo!
    {'x': 250, 'y': 300},  # Missing color!
]
```

**Check for required keys:**

```python
def draw_car(canvas, car_data):
    # Optional: validate data
    required_keys = ['x', 'y', 'width', 'height', 'color']
    for key in required_keys:
        if key not in car_data:
            print(f"Warning: missing {key} in car data")
            return

    # Now safe to use
    canvas.rect(
        car_data['x'],
        car_data['y'],
        car_data['width'],
        car_data['height'],
        fill=car_data['color']
    )
```

### Tips for Data-Driven Drawing

**Start with one object:**

```python
# 1. Get one object working
car = {'x': 100, 'y': 200, 'width': 150, 'height': 80, 'color': Color.RED}
draw_car(can, car)

# 2. Then make it a list
cars = [
    {'x': 100, 'y': 200, 'width': 150, 'height': 80, 'color': Color.RED},
    {'x': 300, 'y': 200, 'width': 150, 'height': 80, 'color': Color.BLUE},
]
for car in cars:
    draw_car(can, car)
```

**Use default values:**

```python
def draw_car(canvas, car_data):
    # Provide defaults for optional keys
    width = car_data.get('width', 150)  # Default to 150 if not specified
    height = car_data.get('height', 80)  # Default to 80 if not specified
    color = car_data.get('color', Color.BLUE)  # Default to BLUE

    canvas.rect(car_data['x'], car_data['y'], width, height, fill=color)
```

**Add variety to your scene:**

```python
# Use loops to generate data
cars = []
for i in range(5):
    car = {
        'x': 50 + i * 150,
        'y': 300,
        'width': 150,
        'height': 80,
        'color': Color.RED if i % 2 == 0 else Color.BLUE  # Alternate colors
    }
    cars.append(car)

for car in cars:
    draw_car(can, car)
```

### Debugging Dictionary Issues

**Print to see what you have:**

```python
car = {'x': 100, 'y': 200, 'color': Color.RED}
print(car)  # See the whole dictionary
print(car['x'])  # See a specific value
print(car.keys())  # See all keys
```

**Check if a key exists:**

```python
if 'color' in car:
    print("Car has a color")
else:
    print("Car missing color - using default")
    car['color'] = Color.BLUE
```

### Common Patterns

**Conditional drawing based on data:**

```python
def draw_vehicle(canvas, vehicle_data):
    if vehicle_data['type'] == 'car':
        draw_car(canvas, vehicle_data)
    elif vehicle_data['type'] == 'truck':
        draw_truck(canvas, vehicle_data)
```

**Building lists dynamically:**

```python
# Create cars at regular intervals
cars = []
for i in range(10):
    cars.append({
        'x': i * 80,
        'y': 300,
        'width': 150,
        'height': 80,
        'color': Color.RED
    })
```

**Combining data and functions:**

```python
def create_car(x, y, color):
    """Helper function to create car dictionary"""
    return {
        'x': x,
        'y': y,
        'width': 150,
        'height': 80,
        'color': color
    }

cars = [
    create_car(50, 300, Color.RED),
    create_car(250, 300, Color.BLUE),
    create_car(450, 300, Color.GREEN),
]
```
