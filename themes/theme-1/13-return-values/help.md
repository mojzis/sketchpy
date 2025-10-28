## Additional Help

### Common Issues

**Function returns `None`?**

- Make sure your function has a `return` statement
- Check that all code paths return a value
- If your function prints but doesn't return, you'll get `None`

**Can't use the returned value?**

- Capture it in a variable first: `result = my_function()`
- Then use the variable: `can.circle(100, 100, 30, fill=result)`
- Don't try to use it directly in some cases without capturing first

**Function stops too early?**

- Remember: `return` immediately exits the function
- Any code after `return` will not run
- This is useful for conditional returns!

### Understanding Return vs Print

```python
# This function PRINTS but doesn't return
def bad_example(speed):
    if speed > 100:
        print(Color.RED)  # Just prints to console
    # Returns None (nothing)

# This function RETURNS a value
def good_example(speed):
    if speed > 100:
        return Color.RED  # Sends back the value
    return Color.BLUE
```

### Tips for Return Values

**Return early for simpler code:**

```python
def get_size(width):
    if width < 100:
        return "small"
    if width < 200:
        return "medium"
    return "large"
```

**Return multiple values using tuples:**

```python
def calculate_positions(x, y):
    front = x + 50
    back = x - 50
    return (front, back)  # Returns both values

# Use both returned values
front_x, back_x = calculate_positions(200, 300)
```

**Return lists for multiple items:**

```python
def get_rainbow_colors():
    return [Color.RED, Color.ORANGE, Color.YELLOW, Color.GREEN, Color.BLUE]

colors = get_rainbow_colors()
for color in colors:
    # Draw with each color
```

### Debugging Return Values

```python
# See what your function returns
result = calculate_wheel_positions(200, 300, 250)
print(result)  # Check what it returns

# Use the result
for x, y in result:
    can.circle(x, y, 25, fill=Color.BLACK)
```

### Common Patterns

**Return based on conditions:**

```python
def get_vehicle_type(width):
    if width > 200:
        return "truck"
    elif width > 150:
        return "sedan"
    else:
        return "compact"
```

**Return calculated positions:**

```python
def calculate_center(x, y, width, height):
    center_x = x + width / 2
    center_y = y + height / 2
    return (center_x, center_y)
```

**Return colors based on data:**

```python
def get_speed_color(speed):
    if speed > 150:
        return Color.RED
    elif speed > 100:
        return Color.ORANGE
    else:
        return Color.BLUE
```
