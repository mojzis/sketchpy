## 📦 Variables: Store and Reuse Values

### Goal
Learn how variables make your code flexible and easy to change.

### What You'll Learn
- Variables store values with names
- Change one variable to update everything
- Variables make code easier to read

### How Variables Work
Instead of typing numbers everywhere:
```python
cars.rounded_car(can, 100, 300, 140, 50, Color.BLUE)
cars.rounded_car(can, 300, 300, 140, 50, Color.BLUE)
```

Use variables:
```python
car_y = 300
car_width = 140
car_color = Color.BLUE
```

Now changing `car_color = Color.RED` changes all cars!

### The Demo Shows
- Three different car types (rounded, sports, bus)
- Variables for colors, sizes, and positions
- How one change affects multiple cars

### Try This
1. Run the code to see the three vehicles
2. Change `sedan_color` to Color.GREEN
3. Change `sports_y` to 150 (moves it up)
4. Change `bus_width` to 250 (makes it longer)

### Challenge
Add variables for a fourth car and draw it on the road.
