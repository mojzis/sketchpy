## 🏷️ Project 4: Label Your Car Parts

### Goal
Add text labels to a car drawing to learn about strings and f-strings.

### What you'll learn
- Creating string variables to store text
- Using f-strings to combine text and numbers
- Adding text to your canvas with `text()`
- Positioning text labels on shapes

### Autocomplete Tip
Type `can.text(` to see the text method! Use Tab to insert example code with all parameters (x, y, text, size, fill).

### Steps
1. Create string variables: `car_type = "Sports Car"`
2. Store numbers in variables: `car_year = 2024`
3. Draw a car with body, wheels, and windows
4. Add labels using f-strings: `can.text(x, y, f"{car_type} ({car_year})", size=20)`
5. Label different car parts with descriptive text

### Coordinate System
Text is positioned by its center point. Use the grid to find good positions: `can.grid(spacing=50, show_coords=True)`

### Available Methods
- `can.text(x, y, text, size=16, fill=...)` - Draw text at position
- `can.rect(x, y, width, height, fill=...)` - Draw rectangles
- `can.circle(x, y, radius, fill=...)` - Draw circles

### F-String Format
F-strings let you put variables inside text:
- `f"Top Speed: {max_speed} km/h"` - Shows the speed value
- `f"{car_type} ({car_year})"` - Combines multiple variables
- Use curly braces `{}` around variable names

### Tips
- String variables hold text: `name = "My Car"`
- F-strings combine text and variables: `f"Speed: {speed}"`
- Text size affects readability (try 12, 16, 20, 24)
- White text shows well on dark colors, black on light colors

### Challenge
Can you create a "specification sheet" with 5+ labeled details? Try adding make, model, color, weight, and horsepower!
