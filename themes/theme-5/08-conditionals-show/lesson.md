## 🚦 Conditionals: Make Decisions

### Goal
Learn how `if/else` statements let your code make choices.

### What You'll Learn
- `if` statements check conditions
- `else` provides an alternative
- `elif` checks multiple conditions
- Create variety with logic

### How Conditionals Work
Instead of everything being the same:
```python
for i in range(6):
    cars.rounded_car(can, x, y, color=Color.BLUE)  # Always blue
```

Make choices:
```python
for i in range(6):
    if i % 2 == 0:  # If i is even
        cars.rounded_car(can, x, y, color=Color.BLUE)
    else:  # If i is odd
        cars.sports_car(can, x, y, color=Color.RED)
```

### Common Conditions
- `i % 2 == 0` - is i even?
- `i < 3` - is i less than 3?
- `color == Color.RED` - is color red?
- `x > 400` - is x greater than 400?

### The Demo Shows
- Alternating car colors using `i % 2 == 0`
- Different car types based on position
- Traffic light system with multiple conditions
- Creating patterns with logic

### Try This
1. Run the code - see the alternating pattern
2. Change the color in the `else` block
3. Add an `elif` for a third condition
4. Change `i % 2 == 0` to `i % 3 == 0` (every third)

### Challenge
Make traffic lights change based on position - left side green, right side red.
