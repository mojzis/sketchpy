## Additional Help

### Common Issues

**Text not showing?**
- Check the color - white text on white background won't show
- Make sure you're using quotes: `"text"` not just text
- Verify the position is inside the canvas (0-800, 0-600)

**F-strings not working?**
- Make sure to put `f` before the quotes: `f"text {variable}"`
- Variables go inside curly braces: `{variable_name}`
- Check that variable names are spelled correctly

**Text in wrong position?**
- Text is centered at the x, y position you provide
- Use `can.grid(show_coords=True)` to see coordinates
- Adjust x and y values to move text

### String Basics

**Creating strings:**
```python
car_type = "Sports Car"
car_color = "Red"
```

**Combining strings with +:**
```python
message = "This is a " + car_type
```

**Using f-strings (easier!):**
```python
message = f"This is a {car_type}"
label = f"{car_type} - Top Speed: {max_speed}"
```

### Text Styling Tips

- **Small text:** size=12 for details
- **Medium text:** size=16 for labels
- **Large text:** size=20-24 for titles
- **Contrast:** Light text on dark shapes, dark text on light shapes
- **Spacing:** Leave room between labels so they don't overlap

### Common Patterns

**Label above a shape:**
```python
can.rect(200, 300, 100, 50, fill=Color.RED)
can.text(250, 280, "Roof", size=14)  # Above the rectangle
```

**Label inside a shape:**
```python
can.rect(200, 300, 100, 50, fill=Color.RED)
can.text(250, 325, "Body", size=14, fill=Color.WHITE)  # Inside
```

**Specification list:**
```python
y_start = 500
can.text(100, y_start, f"Type: {car_type}", size=14)
can.text(100, y_start + 20, f"Year: {car_year}", size=14)
can.text(100, y_start + 40, f"Speed: {max_speed} km/h", size=14)
```
