## 🔄 Loops: Repeat Without Typing

### Goal
Learn how loops let you repeat code without copying and pasting.

### What You'll Learn
- `for` loops repeat code automatically
- `range(5)` means "do this 5 times"
- Loop variables (like `i`) change each time

### The Magic of Loops
Instead of writing:
```python
ocean.seaweed(100, 600)
ocean.seaweed(200, 600)
ocean.seaweed(300, 600)
ocean.seaweed(400, 600)
ocean.seaweed(500, 600)
```

We write:
```python
for i in range(5):
    x = 100 + i * 100
    ocean.seaweed(x, 600)
```

The loop does it 5 times automatically!

### How It Works
- `i` starts at 0, then 1, then 2, then 3, then 4
- `x = 100 + i * 100` calculates: 100, 200, 300, 400, 500
- Each seaweed appears 100 pixels apart

### Try This
1. Run the code - see the seaweed row
2. Change `range(5)` to `range(8)` - more seaweed!
3. Change `i * 100` to `i * 80` - they get closer together
4. Change the height to make them taller

### Challenge
Can you make two rows of seaweed at different heights?
