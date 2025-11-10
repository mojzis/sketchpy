## 🔄 Loops: Repeat Without Typing

### Goal
Learn how loops let you repeat code without copying and pasting.

### What You'll Learn
- `for` loops repeat code automatically
- `range(5)` means "do this 5 times"
- Loop variables (like `i`) change each time
- Create patterns with math

### The Magic of Loops
Instead of writing:
```python
cars.simple_car(can, 50, 400, color=Color.BLUE)
cars.simple_car(can, 200, 400, color=Color.BLUE)
cars.simple_car(can, 350, 400, color=Color.BLUE)
cars.simple_car(can, 500, 400, color=Color.BLUE)
```

We write:
```python
for i in range(4):
    x = 50 + i * 150
    cars.simple_car(can, x, 400, color=Color.BLUE)
```

The loop does it 4 times automatically!

### How It Works
- `i` starts at 0, then 1, then 2, then 3
- `x = 50 + i * 150` calculates: 50, 200, 350, 500
- Each car appears 150 pixels apart

### The Demo Shows
- A parking lot with rows of cars
- Different car types in different rows
- Using loops to create neat patterns

### Try This
1. Run the code - see the parking lot
2. Change `range(5)` to `range(7)` in a loop - more cars!
3. Change spacing (`i * 150` to `i * 120`) - cars get closer
4. Change colors in the loops

### Challenge
Can you add a third row with sports cars?
