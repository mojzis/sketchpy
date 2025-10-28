# Lists and Functions (Dictionaries)

## What You'll Learn
- **Programming:** Dictionaries (key-value pairs), list of dictionaries, data-driven programming
- **Drawing:** Garden scene defined by data structures

## What Are Dictionaries?

A dictionary stores data as key-value pairs. Instead of accessing items by position (like lists), you access them by name (key):

```python
# List: access by index
flower = ["Rose", "pink", 20]
name = flower[0]  # Have to remember 0 is name

# Dictionary: access by key name
flower = {
    "name": "Rose",
    "color": "pink",
    "size": 20
}
name = flower["name"]  # Clear and readable!
```

Dictionaries make your data self-documenting and easier to understand.

## Dictionary Syntax

```python
# Create a dictionary
flower = {
    "name": "Rose",        # key: value,
    "petal_color": "pink", # key: value,
    "size": 20             # key: value
}

# Access values
print(flower["name"])         # "Rose"
print(flower["petal_color"])  # "pink"

# Change values
flower["size"] = 25

# Add new keys
flower["center_color"] = "yellow"
```

## Instructions

### Step 1: Create a Flower Dictionary

```python
from sketchpy.shapes import Canvas, CreativeGardenPalette


def draw_flower_from_data(can, flower_data):
    """Draw a flower based on dictionary data"""
    # Extract data from dictionary using keys
    x = flower_data["x"]
    y = flower_data["y"]
    size = flower_data["size"]
    petal_color = flower_data["petal_color"]
    center_color = flower_data["center_color"]

    # Calculate dimensions
    center_size = int(size * 0.7)
    petal_distance = int(size * 1.4)

    # Draw the flower
    can.circle(x, y, center_size, fill=center_color,
               stroke='#000', stroke_width=2)

    can.circle(x, y - petal_distance, size, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x + petal_distance, y, size, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x, y + petal_distance, size, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x - petal_distance, y, size, fill=petal_color,
               stroke='#000', stroke_width=1.5)


def main():
    can = Canvas(800, 600)
    can.grid(spacing=50, show_coords=True)

    # Define a flower as data
    flower1 = {
        "x": 200,
        "y": 300,
        "size": 20,
        "petal_color": CreativeGardenPalette.ROSE_QUARTZ,
        "center_color": CreativeGardenPalette.BUTTER_YELLOW
    }

    # Draw it!
    draw_flower_from_data(can, flower1)

    return can
```

**Try it:** Create a second flower dictionary with different values and draw it.

### Step 2: List of Dictionaries

```python
def main():
    can = Canvas(800, 600)
    can.grid(spacing=50, show_coords=True)

    # Define entire garden as a list of flower dictionaries!
    garden = [
        {
            "x": 150,
            "y": 350,
            "size": 18,
            "petal_color": CreativeGardenPalette.ROSE_QUARTZ,
            "center_color": CreativeGardenPalette.BUTTER_YELLOW
        },
        {
            "x": 300,
            "y": 350,
            "size": 22,
            "petal_color": CreativeGardenPalette.LILAC_DREAM,
            "center_color": CreativeGardenPalette.LEMON_CHIFFON
        },
        {
            "x": 450,
            "y": 350,
            "size": 20,
            "petal_color": CreativeGardenPalette.PEACH_WHISPER,
            "center_color": CreativeGardenPalette.CORAL_BLUSH
        },
        {
            "x": 600,
            "y": 350,
            "size": 24,
            "petal_color": CreativeGardenPalette.MISTY_MAUVE,
            "center_color": CreativeGardenPalette.BUTTER_YELLOW
        }
    ]

    # Draw all flowers from data
    for flower_data in garden:
        draw_flower_from_data(can, flower_data)

    return can
```

Now your entire scene is **data**, separate from **code**! This is called "data-driven programming."

**Try it:** Add more flowers to the garden list.

### Step 3: Add Metadata

```python
def draw_labeled_flower(can, flower_data):
    """Draw a flower and its label from data"""
    # Draw the flower
    draw_flower_from_data(can, flower_data)

    # Add label if data includes name
    if "name" in flower_data:
        can.text(flower_data["name"],
                 flower_data["x"],
                 flower_data["y"] + 60,
                 font_size=16,
                 fill='#000',
                 text_anchor='middle')


def main():
    can = Canvas(800, 600)
    can.grid(spacing=50, show_coords=True)

    garden = [
        {
            "name": "Rose",
            "x": 200,
            "y": 300,
            "size": 20,
            "petal_color": CreativeGardenPalette.ROSE_QUARTZ,
            "center_color": CreativeGardenPalette.BUTTER_YELLOW
        },
        {
            "name": "Tulip",
            "x": 400,
            "y": 300,
            "size": 22,
            "petal_color": CreativeGardenPalette.LILAC_DREAM,
            "center_color": CreativeGardenPalette.LEMON_CHIFFON
        },
        {
            "name": "Daisy",
            "x": 600,
            "y": 300,
            "size": 18,
            "petal_color": CreativeGardenPalette.PEACH_WHISPER,
            "center_color": CreativeGardenPalette.CORAL_BLUSH
        }
    ]

    for flower_data in garden:
        draw_labeled_flower(can, flower_data)

    return can
```

Adding data (like names) doesn't require changing the code!

**Challenge:** Create a complete garden scene with dictionaries for flowers, butterflies, and clouds. Each object type has its own data structure and drawing function.

## Common Issues

### Issue: "KeyError: 'color'"
**Solution:** Trying to access a key that doesn't exist. Check spelling and make sure key was added to dictionary.

### Issue: "TypeError: list indices must be integers, not str"
**Solution:** Using dictionary syntax on a list, or list syntax on dictionary. Use `my_dict["key"]` for dictionaries, `my_list[0]` for lists.

### Issue: Dictionary values don't update
**Solution:** Make sure you're using `=` to assign: `my_dict["key"] = new_value`.
