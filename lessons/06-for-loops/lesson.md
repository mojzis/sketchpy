## 🚗 Project 6: Parking Lot with Loops

### Goal
Draw multiple cars in a row using for loops to avoid repeating code.

### What you'll learn
- Using `for` loops to repeat actions
- The `range()` function for counting
- Loop variables (like `i`) that change each time
- Calculating positions based on the loop variable

### Autocomplete Tip
Type `for i in range(` to see the loop structure. The loop will repeat the indented code!

### Steps
1. Create a canvas: `can = Canvas(800, 600)`
2. Draw background (sky and ground)
3. Create a for loop: `for i in range(5):`
4. Inside the loop, calculate position: `x_position = 50 + i * 150`
5. Draw one car at the calculated position
6. Watch as the loop draws 5 cars automatically!

### Coordinate System
The loop variable `i` starts at 0 and counts up: 0, 1, 2, 3, 4. Use it to calculate different x positions.

### Available Methods
- `can.rect(x, y, width, height, fill=...)` - Car body and background
- `can.circle(x, y, radius, fill=...)` - Wheels
- `can.grid(spacing=50)` - Helper to see positions

### For Loop Pattern
```python
for i in range(5):
    # This code runs 5 times
    # i will be 0, then 1, then 2, then 3, then 4
    x = 50 + i * 150
    can.rect(x, 300, 100, 60, fill=Color.RED)
```

### Range Function
- `range(5)` gives you: 0, 1, 2, 3, 4 (five numbers)
- `range(3)` gives you: 0, 1, 2 (three numbers)
- `range(10)` gives you: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 (ten numbers)

### Calculating Positions
If you want cars evenly spaced:
- First car: `x = 50 + 0 * 150 = 50`
- Second car: `x = 50 + 1 * 150 = 200`
- Third car: `x = 50 + 2 * 150 = 350`
- The pattern: `x = starting_position + i * spacing`

### Tips
- Everything inside the loop must be indented
- Change `range(5)` to `range(3)` or `range(7)` to draw different numbers of cars
- Adjust the spacing (150) to make cars closer or farther apart
- Use the loop variable `i` to calculate positions

### Challenge
Can you draw cars at different y positions too? Try making each car slightly lower than the previous one! Bonus: Draw windows on each car.
