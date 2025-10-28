# Return Values

## What You'll Learn
- **Programming:** Return statement, capturing returned values, function composition
- **Drawing:** Functions that calculate positions and return values for use in drawing

## What Are Return Values?

So far, your functions have performed actions (drawing shapes). But functions can also **calculate and return values** that you use elsewhere.

```python
# Action function: does something, returns nothing
def draw_flower(can, x, y):
    can.circle(x, y, 20)  # Draws, but doesn't return anything

# Calculation function: computes and returns a value
def calculate_flower_height(size):
    height = size * 2.5
    return height  # Returns the calculated value
```

The `return` statement sends a value back to wherever the function was called.

## Using Return Values

```python
# Call function and capture the return value
flower_height = calculate_flower_height(20)  # flower_height = 50

# Use the returned value
print(f"Flower height: {flower_height}")
y_position = 500 - flower_height  # Calculate position based on height
```

## Instructions

### Step 1: Function That Returns a Calculation

```python
from sketchpy.shapes import Canvas, CreativeGardenPalette


def calculate_petal_distance(size):
    """Calculate how far petals should be from center

    Returns the calculated distance based on flower size.
    """
    distance = int(size * 1.4)
    return distance  # Send the value back


def draw_flower(can, x, y, size):
    """Draw a flower using calculated positions"""
    # Call function and use its return value
    petal_distance = calculate_petal_distance(size)
    center_size = int(size * 0.7)

    # Draw center
    can.circle(x, y, center_size,
               fill=CreativeGardenPalette.BUTTER_YELLOW,
               stroke='#000', stroke_width=2)

    # Draw petals using the calculated distance
    can.circle(x, y - petal_distance, size,
               fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)
    can.circle(x + petal_distance, y, size,
               fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)
    can.circle(x, y + petal_distance, size,
               fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)
    can.circle(x - petal_distance, y, size,
               fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)


def main():
    can = Canvas(800, 600)
    can.grid(spacing=50, show_coords=True)

    draw_flower(can, 300, 300, 20)
    draw_flower(can, 500, 300, 30)

    return can
```

**Try it:** Create a `calculate_center_size(size)` function that returns `int(size * 0.7)`.

### Step 2: Return Different Data Types

```python
def should_draw_butterfly(temperature, is_sunny):
    """Determine if conditions are right for butterflies

    Returns True if butterflies should appear, False otherwise.
    """
    if temperature > 70 and is_sunny:
        return True
    else:
        return False


def main():
    can = Canvas(800, 600)
    can.grid(spacing=50, show_coords=True)

    # Use the function's return value in an if statement
    if should_draw_butterfly(75, True):
        # Draw butterfly at (400, 200)
        can.ellipse(400, 200, 12, 40,
                    fill=CreativeGardenPalette.LILAC_DREAM,
                    stroke='#000', stroke_width=2)
        can.circle(380, 190, 18,
                   fill=CreativeGardenPalette.PEACH_WHISPER,
                   stroke='#000', stroke_width=1.5)
        can.circle(420, 190, 18,
                   fill=CreativeGardenPalette.PEACH_WHISPER,
                   stroke='#000', stroke_width=1.5)

    return can
```

Functions can return numbers, booleans, strings, or any data type!

**Try it:** Create a function that returns a color based on temperature.

### Step 3: Return Multiple Values

```python
def calculate_flower_dimensions(base_size):
    """Calculate all flower dimensions from base size

    Returns a tuple of (center_size, petal_size, petal_distance).
    """
    center_size = int(base_size * 0.7)
    petal_size = base_size
    petal_distance = int(base_size * 1.4)

    return center_size, petal_size, petal_distance  # Return multiple values


def draw_flower(can, x, y, base_size):
    """Draw flower using dimensions from calculation function"""
    # Capture all three return values
    center_size, petal_size, petal_distance = calculate_flower_dimensions(base_size)

    can.circle(x, y, center_size,
               fill=CreativeGardenPalette.BUTTER_YELLOW,
               stroke='#000', stroke_width=2)

    can.circle(x, y - petal_distance, petal_size,
               fill=CreativeGardenPalette.LILAC_DREAM,
               stroke='#000', stroke_width=1.5)
    can.circle(x + petal_distance, y, petal_size,
               fill=CreativeGardenPalette.LILAC_DREAM,
               stroke='#000', stroke_width=1.5)
    can.circle(x, y + petal_distance, petal_size,
               fill=CreativeGardenPalette.LILAC_DREAM,
               stroke='#000', stroke_width=1.5)
    can.circle(x - petal_distance, y, petal_size,
               fill=CreativeGardenPalette.LILAC_DREAM,
               stroke='#000', stroke_width=1.5)
```

Returning multiple values keeps calculations organized!

### Step 4: Early Return

```python
def get_flower_color(temperature):
    """Return flower color based on temperature"""
    if temperature > 80:
        return CreativeGardenPalette.CORAL_BLUSH  # Hot: coral
    elif temperature > 60:
        return CreativeGardenPalette.ROSE_QUARTZ  # Moderate: pink
    else:
        return CreativeGardenPalette.LILAC_DREAM  # Cool: purple
    # Function exits immediately when it hits a return statement
```

When Python hits a `return`, the function stops immediately and sends back the value.

**Challenge:** Create a `calculate_garden_layout(num_flowers, canvas_width)` function that returns the starting x position and spacing needed to fit all flowers.

## Common Issues

### Issue: "TypeError: 'NoneType' object is not subscriptable"
**Solution:** Function doesn't have a return statement, so it returns `None` by default. Add `return` statement.

### Issue: Return value is always None
**Solution:** Make sure `return` statement is actually executed. Check indentation and control flow.

### Issue: Can't use value after return
**Solution:** Return exits the function immediately. Code after `return` never runs.
