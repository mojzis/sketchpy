## 🌙 Project 5: Day and Night Scene

### Goal
Draw a car scene that changes between day and night using conditional logic.

### What you'll learn
- Boolean variables (True/False values)
- Using if/else statements to make decisions
- Comparison operators (>, <, ==)
- Drawing different things based on conditions

### Autocomplete Tip
After typing `if`, marimo will show you the structure. Use conditions to control what gets drawn!

### Steps
1. Create boolean variable: `is_night = True`
2. Use if/else to draw different skies:
   ```python
   if is_night:
       can.rect(0, 0, 800, 600, fill="#001122")  # Dark sky
   else:
       can.rect(0, 0, 800, 600, fill="#87CEEB")  # Light sky
   ```
3. Add conditional elements (moon/sun, stars)
4. Draw a car (same for both conditions)
5. Use comparison to show speed warning: `if speed > 120:`

### Coordinate System
Start with the background (sky) at (0, 0), then add foreground elements like roads and cars on top.

### Available Methods
- `can.rect(x, y, width, height, fill=...)` - Rectangles for sky, road, car
- `can.circle(x, y, radius, fill=...)` - Circles for sun, moon, stars, wheels
- `can.text(x, y, text, size=..., fill=...)` - Text labels

### Boolean Basics
- Booleans are True or False: `is_night = True`
- Change the value to see different results: `is_night = False`
- They control if/else decisions in your code

### Comparison Operators
- `>` greater than: `speed > 120`
- `<` less than: `speed < 60`
- `==` equal to: `time == "morning"`
- `!=` not equal to: `color != "red"`

### If/Else Pattern
```python
if condition:
    # Code runs when condition is True
else:
    # Code runs when condition is False
```

### Tips
- Background shapes should be drawn first (they're behind everything)
- Use hex colors for custom shades: `"#001122"` for dark blue
- Draw common elements (like the car) outside the if/else
- Try changing `is_night` to see both versions

### Challenge
Can you add three conditions using elif? Try morning/afternoon/night with different sky colors and sun positions!
