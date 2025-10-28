## 🚗 Lesson 7: Multi-Colored Car Fleet

### Goal
Create a fleet of cars in different colors and sizes using lists to store car properties.

### What you'll learn
- Storing multiple values in a list
- Accessing list items by index
- Looping through lists with enumerate()
- Using multiple related lists together
- Understanding list length with len()

### Autocomplete Tip
Type `can.` to see Canvas methods! Press **Enter** to insert working example code with all parameters. Then customize the values!

### Steps
1. Create lists to store car colors and sizes
2. Use `enumerate()` to loop through the list with both index and value
3. Calculate car positions based on the index
4. Access the sizes list using the index: `sizes[i]`
5. Draw each car with its unique color and size

### Understanding Lists
```python
# Lists store multiple values in order
colors = [Color.RED, Color.BLUE, Color.GREEN]
sizes = [100, 120, 90]

# Access by index (starts at 0)
first_color = colors[0]  # RED
second_size = sizes[1]   # 120

# Loop with enumerate to get index and value
for i, color in enumerate(colors):
    print(f"Car {i} is {color}")
```

### Coordinate System
The canvas coordinates start at the top-left (0, 0). X increases to the right, Y increases downward.

### Available Methods
- `can.circle(x, y, radius, fill=...)`
- `can.rect(x, y, width, height, fill=...)`
- `can.grid(spacing=50, show_coords=True)` - Show coordinate grid
- `can.show_palette(PaletteClass)` - Display palette colors

### Color Palettes
**Basic Colors:** `Color.RED`, `Color.BLUE`, `Color.GREEN`, `Color.YELLOW`, `Color.ORANGE`, `Color.BLACK`, `Color.GRAY`

**Calm Oasis:** `CalmOasisPalette.SKY_BLUE`, `MINT_FRESH`, `LAVENDER_MIST`, `OCEAN_DEEP`

### Tips
- Lists keep items in order - first item is index 0
- Use `enumerate()` to get both the position (index) and value
- Related data (like colors and sizes) can use separate lists with the same index
- Calculate positions using the index: `x = 50 + i * 150`

### Challenge
- Add a third list for car heights and make some cars taller than others
- Create a list of y-positions to make cars at different vertical levels
- Add 2-3 more colors to create a longer fleet
- Try using different color palettes for variety
