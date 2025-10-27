## 🚦 Project 10: Smart Traffic System

### Goal
Build a smart traffic system that uses compound conditions to determine traffic status and display the appropriate message and car color.

### What you'll learn
- Combining multiple conditions with `and`, `or`, `not`
- Building complex decision trees
- Modeling real-world logic in code
- Using parentheses to group conditions

### Autocomplete Tip
Type `can.` to see Canvas methods! Press **Tab** or **Enter** to insert working example code with all parameters. Then customize the values!

### Steps
1. Create variables for traffic conditions: `time_of_day`, `is_weekend`, `traffic_level`
2. Use `if/elif/else` with compound conditions
3. Combine conditions with `and` (both must be true) and `or` (either can be true)
4. Set different colors and messages based on the conditions
5. Draw a car with the determined color

### Understanding Compound Conditions
- `and`: Both conditions must be true
  - `time_of_day == "morning" and is_weekend` (true only if morning AND weekend)
- `or`: Either condition can be true
  - `traffic_level > 70 or time_of_day == "evening"` (true if heavy traffic OR evening)
- `not`: Inverts a condition
  - `not is_weekend` (true on weekdays)

### Example Logic Flow
```
IF morning AND weekend:
    → "Leisure Drive" (blue car)
ELIF traffic level > 70 OR evening:
    → "Rush Hour!" (gray car)
ELSE:
    → "Normal Traffic" (green car)
```

### Coordinate System
The canvas coordinates start at the top-left (0, 0). X increases to the right, Y increases downward.

### Available Methods
- `can.rect(x, y, width, height, fill=...)`
- `can.circle(x, y, radius, fill=...)`
- `can.text(x, y, text, size=..., fill=...)`
- `can.grid(spacing=50, show_coords=True)` - Show coordinate grid

### Tips
- Try changing the variables at the top to see different results
- Experiment with different time values: "morning", "afternoon", "evening"
- Try different traffic levels: 0-100
- Add your own conditions with the `not` operator!

### Challenge
Can you add more conditions? Try adding weather (sunny/rainy) or season (summer/winter) variables and create 8+ different scenarios!
