# Function Parameters

## What You'll Learn
- **Programming:** Multiple parameters, flexible functions, parameter-driven behavior
- **Drawing:** Customizable flowers with varying sizes, positions, and colors

## Parameters Make Functions Flexible

In Lesson 11, your flower function always drew the same flower. Parameters let you customize the function's behavior each time you call it.

```python
# Basic function: always draws same flower
def draw_flower(can, x, y):
    can.circle(x, y, 20, fill='pink')  # Always size 20, always pink

# Flexible function: can vary size and color!
def draw_custom_flower(can, x, y, size, color):
    can.circle(x, y, size, fill=color)  # Size and color can change!
```

## Understanding Parameters

Parameters are like blanks in a form - when you call the function, you fill in the values:

```python
def draw_flower(can, x, y, size, petal_color):
    # size and petal_color are parameters - they can be different each time!
    can.circle(x, y, size, fill=petal_color)

# Call with different values
draw_flower(can, 100, 200, 30, 'pink')      # Large pink flower
draw_flower(can, 300, 200, 15, 'purple')    # Small purple flower
draw_flower(can, 500, 200, 25, 'yellow')    # Medium yellow flower
```

## Instructions

### Step 1: Add Size Parameter

```python
from sketchpy.shapes import Canvas, CreativeGardenPalette


def draw_flower(can, x, y, size):
    """Draw a flower with customizable size"""
    # Use size to calculate all measurements proportionally
    center_size = int(size * 0.7)  # Center is 70% of total size
    petal_size = size
    petal_distance = int(size * 1.4)  # Petals are 1.4x size away

    # Center
    can.circle(x, y, center_size,
               fill=CreativeGardenPalette.BUTTER_YELLOW,
               stroke='#000', stroke_width=2)

    # Petals
    can.circle(x, y - petal_distance, petal_size,
               fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)
    can.circle(x + petal_distance, y, petal_size,
               fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)
    can.circle(x, y + petal_distance, petal_size,
               fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)
    can.circle(x - petal_distance, y, petal_size,
               fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)


def main():
    can = Canvas(800, 600)
    can.grid(spacing=50, show_coords=True)

    # Draw flowers of different sizes!
    draw_flower(can, 150, 300, 15)  # Small
    draw_flower(can, 300, 300, 22)  # Medium
    draw_flower(can, 500, 300, 30)  # Large

    return can
```

**Try it:** Draw flowers with sizes ranging from 10 to 40.

### Step 2: Add Color Parameters

```python
def draw_flower(can, x, y, size, petal_color, center_color):
    """Draw a flower with custom size and colors"""
    center_size = int(size * 0.7)
    petal_size = size
    petal_distance = int(size * 1.4)

    # Use the color parameters instead of hardcoded colors
    can.circle(x, y, center_size, fill=center_color,
               stroke='#000', stroke_width=2)

    can.circle(x, y - petal_distance, petal_size, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x + petal_distance, y, petal_size, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x, y + petal_distance, petal_size, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x - petal_distance, y, petal_size, fill=petal_color,
               stroke='#000', stroke_width=1.5)


def main():
    can = Canvas(800, 600)
    can.grid(spacing=50, show_coords=True)

    # Now each flower can be completely different!
    draw_flower(can, 150, 300, 20,
                CreativeGardenPalette.ROSE_QUARTZ,
                CreativeGardenPalette.BUTTER_YELLOW)

    draw_flower(can, 350, 300, 25,
                CreativeGardenPalette.LILAC_DREAM,
                CreativeGardenPalette.LEMON_CHIFFON)

    draw_flower(can, 550, 300, 18,
                CreativeGardenPalette.PEACH_WHISPER,
                CreativeGardenPalette.CORAL_BLUSH)

    return can
```

**Try it:** Create a diverse garden with 5-6 flowers, each with different sizes and colors.

### Step 3: Use Parameters with Loops

```python
def main():
    can = Canvas(800, 600)
    can.grid(spacing=50, show_coords=True)

    # Create gradient of sizes
    for i in range(6):
        x = 100 + i * 120
        size = 15 + i * 3  # Gradually increasing size

        draw_flower(can, x, 350, size,
                    CreativeGardenPalette.LILAC_DREAM,
                    CreativeGardenPalette.BUTTER_YELLOW)

    return can
```

Parameters + loops = powerful combinations!

**Try it:** Make colors alternate as well as sizes.

### Step 4: Default Parameters

```python
def draw_flower(can, x, y, size=20,
                petal_color=CreativeGardenPalette.ROSE_QUARTZ,
                center_color=CreativeGardenPalette.BUTTER_YELLOW):
    """Draw a flower with optional custom properties

    If you don't provide size/colors, defaults are used.
    """
    center_size = int(size * 0.7)
    petal_size = size
    petal_distance = int(size * 1.4)

    can.circle(x, y, center_size, fill=center_color,
               stroke='#000', stroke_width=2)

    can.circle(x, y - petal_distance, petal_size, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x + petal_distance, y, petal_size, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x, y + petal_distance, petal_size, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x - petal_distance, y, petal_size, fill=petal_color,
               stroke='#000', stroke_width=1.5)


def main():
    can = Canvas(800, 600)

    # Can call with just position (uses defaults)
    draw_flower(can, 200, 300)

    # Or override just size
    draw_flower(can, 400, 300, size=30)

    # Or customize everything
    draw_flower(can, 600, 300, 25,
                CreativeGardenPalette.LILAC_DREAM,
                CreativeGardenPalette.CORAL_BLUSH)

    return can
```

Default parameters make functions flexible but easy to use!

**Challenge:** Create a `draw_garden()` function that accepts parameters for number of flowers, spacing, and size variation.

## Common Issues

### Issue: "TypeError: function() got multiple values for argument 'x'"
**Solution:** You're passing arguments in wrong order or mixing positional and named arguments incorrectly.

### Issue: Function always uses same value even when I pass different ones
**Solution:** Make sure you're using the parameter variable inside the function, not a hardcoded value.

### Issue: "TypeError: function() missing required positional argument"
**Solution:** Provide all required parameters, or add default values to make them optional.
