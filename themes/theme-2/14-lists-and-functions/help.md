# Help: Lists and Functions (Dictionaries)

## Quick Reference

### Creating Dictionaries
```python
# Dictionary with string keys
flower = {
    "name": "Rose",
    "color": "pink",
    "size": 20
}

# Access values by key
name = flower["name"]      # "Rose"
color = flower["color"]    # "pink"
```

### Dictionary Operations
```python
# Add or change values
flower["height"] = 100

# Check if key exists
if "name" in flower:
    print(flower["name"])

# Get with default
height = flower.get("height", 0)  # Returns 0 if key doesn't exist

# Get all keys
keys = flower.keys()

# Get all values
values = flower.values()
```

### List of Dictionaries
```python
garden = [
    {"name": "Rose", "color": "pink"},
    {"name": "Tulip", "color": "yellow"},
    {"name": "Daisy", "color": "white"}
]

# Access first flower
first = garden[0]
print(first["name"])  # "Rose"

# Loop through all
for flower in garden:
    print(flower["name"])
```

## Common Errors

### Error: "KeyError: 'color'"
**What it means:** Key doesn't exist in dictionary
**How to fix:**
- Check spelling: `flower["color"]` not `flower["Color"]`
- Make sure key was added to dictionary
- Use `if "color" in flower:` to check first
- Or use `.get()`: `flower.get("color", "default")`

### Error: "TypeError: list indices must be integers, not str"
**What it means:** Using dictionary syntax on a list
**How to fix:**
- Lists use numbers: `my_list[0]`
- Dictionaries use strings: `my_dict["key"]`

### Error: "TypeError: string indices must be integers"
**What it means:** Trying to use dictionary syntax on a string
**How to fix:** Make sure variable is actually a dictionary

## Debugging Tips

1. **Print the dictionary:**
   ```python
   print(flower)
   # Shows all keys and values
   ```

2. **Print specific key:**
   ```python
   print(f"Name: {flower['name']}")
   print(f"Size: {flower['size']}")
   ```

3. **Check available keys:**
   ```python
   print(flower.keys())
   # Shows all available keys
   ```

4. **Verify data type:**
   ```python
   print(type(flower))  # Should be <class 'dict'>
   ```

## Dictionary Patterns

### Define Data Structure
```python
# Each flower is a dictionary
flower = {
    "x": 100,
    "y": 200,
    "size": 20,
    "color": "pink"
}
```

### Collection of Objects
```python
# List of dictionaries
flowers = [
    {"x": 100, "size": 20, "color": "pink"},
    {"x": 200, "size": 25, "color": "purple"},
    {"x": 300, "size": 18, "color": "yellow"}
]

# Process each one
for flower in flowers:
    draw_flower(can, flower["x"], flower["size"])
```

### Optional Fields
```python
# Some flowers have names, some don't
flower = {"x": 100, "size": 20}

# Check before accessing
if "name" in flower:
    print(flower["name"])
else:
    print("Unnamed flower")

# Or use get with default
name = flower.get("name", "Unknown")
```

### Data-Driven Drawing
```python
def draw_from_data(can, obj_data):
    """Draw based on dictionary data"""
    x = obj_data["x"]
    y = obj_data["y"]
    size = obj_data["size"]
    color = obj_data["color"]

    can.circle(x, y, size, fill=color)

# Data separate from code
objects = [
    {"x": 100, "y": 200, "size": 20, "color": "red"},
    {"x": 300, "y": 200, "size": 30, "color": "blue"}
]

for obj in objects:
    draw_from_data(can, obj)
```

## Dictionary vs List

### When to Use Lists
- Ordered collection of similar items
- Access by position/index
- Example: `colors = ["red", "blue", "green"]`

### When to Use Dictionaries
- Named properties
- Access by meaningful key
- Example: `flower = {"name": "Rose", "color": "red", "size": 20}`

### Combining Both
```python
# List of dictionaries: powerful combination!
garden = [
    {"name": "Rose", "color": "red"},
    {"name": "Tulip", "color": "yellow"}
]
```

## Nested Dictionaries

```python
# Dictionary containing another dictionary
flower = {
    "name": "Rose",
    "position": {
        "x": 100,
        "y": 200
    },
    "colors": {
        "petal": "pink",
        "center": "yellow"
    }
}

# Access nested values
x = flower["position"]["x"]
petal_color = flower["colors"]["petal"]
```

## Related Lessons
- **Lesson 7:** Lists - dictionaries organize data more clearly
- **Lesson 13:** Return values - can return dictionaries too
- **Next:** Lesson 15 integrates everything in final project

## Extra Challenges

1. **Butterfly data:** Create dictionaries for butterflies with position, size, colors
2. **Complete scene:** Use dictionaries for all objects (flowers, butterflies, clouds, sun)
3. **Load from list:** Create a big list of dictionaries and loop through to draw all
4. **Nested structures:** Use nested dictionaries for complex objects
5. **Data validation:** Check if required keys exist before drawing
6. **JSON export:** Research how to save dictionary data to JSON files
