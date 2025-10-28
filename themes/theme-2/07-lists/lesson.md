# Lists

## What You'll Learn
- **Programming:** Lists, accessing elements by index, `enumerate()`, `len()` function
- **Drawing:** Multi-colored flower garden with varying properties

## What Are Lists?

A list is a collection of values stored in order. Instead of having separate variables for each flower color, you can store them all in one list:

```python
# Without lists (tedious!)
color1 = "red"
color2 = "blue"
color3 = "green"

# With lists (much better!)
colors = ["red", "blue", "green"]
```

## Accessing List Elements

Each item in a list has an index (position number) starting from 0:

```python
flowers = ["Rose", "Tulip", "Daisy", "Lily"]
#          [0]      [1]      [2]      [3]

print(flowers[0])  # "Rose"
print(flowers[2])  # "Daisy"
print(flowers[3])  # "Lily"
```

## Instructions

### Step 1: Create and Use a Color List

```python
from sketchpy.shapes import Canvas, CreativeGardenPalette

can = Canvas(800, 600)
can.grid(spacing=50, show_coords=True)

# List of colors for our flowers
petal_colors = [
    CreativeGardenPalette.ROSE_QUARTZ,
    CreativeGardenPalette.LILAC_DREAM,
    CreativeGardenPalette.PEACH_WHISPER,
    CreativeGardenPalette.CORAL_BLUSH,
    CreativeGardenPalette.MISTY_MAUVE
]

# Draw flowers using colors from the list
for i in range(5):
    x = 100 + i * 140
    y = 300

    # Get the color for this flower from the list
    petal_color = petal_colors[i]

    # Draw flower
    can.circle(x, y, 20, fill=CreativeGardenPalette.BUTTER_YELLOW,
               stroke='#000', stroke_width=2)

    can.circle(x, y - 28, 22, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x + 28, y, 22, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x, y + 28, 22, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x - 28, y, 22, fill=petal_color,
               stroke='#000', stroke_width=1.5)
```

**Try it:** Add more colors to the list and increase `range(5)` to `range(7)`.

### Step 2: Use len() to Get List Length

```python
flower_names = ["Rose", "Tulip", "Daisy", "Lily", "Violet", "Sunflower"]

# len() returns the number of items in the list
num_flowers = len(flower_names)  # 6

# Draw exactly as many flowers as we have names
for i in range(num_flowers):
    x = 80 + i * 115
    y = 400

    can.circle(x, y, 18, fill=CreativeGardenPalette.LEMON_CHIFFON,
               stroke='#000', stroke_width=2)

    # Label with the flower name
    can.text(flower_names[i], x, y + 40,
             font_size=16, fill='#000', text_anchor='middle')
```

Now you can add or remove names from the list without changing the loop!

**Try it:** Add "Orchid" to the list and watch it automatically appear.

### Step 3: Use enumerate() for Index and Value

```python
sizes = [15, 20, 25, 20, 15]  # Flower sizes (smaller on edges)

# enumerate() gives us both the index AND the value
for i, size in enumerate(sizes):
    x = 100 + i * 140
    y = 300

    # size is already the value from the list!
    can.circle(x, y, size, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=2)

    # We also have i for positioning
    can.text(f"#{i+1}", x, y + size + 20,
             font_size=14, fill='#000', text_anchor='middle')
```

`enumerate()` is cleaner than using `sizes[i]` - it gives you both at once!

**Challenge:** Create three lists (petal_colors, center_colors, sizes) and use all three to create a diverse garden where each flower is unique.

## Common Issues

### Issue: "IndexError: list index out of range"
**Solution:** You're trying to access an index that doesn't exist. If a list has 5 items, valid indices are 0-4.

### Issue: I changed my list but the flowers didn't change
**Solution:** Make sure your range matches your list length. Use `range(len(my_list))` to be safe.

### Issue: "TypeError: object of type 'range' has no len()"
**Solution:** Don't use `len(range(5))`. If you have a list, use `len(my_list)`.
