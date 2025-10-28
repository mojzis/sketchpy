# Help: For Loops In Depth

## Quick Reference

### Range Variants
```python
range(5)           # 0, 1, 2, 3, 4
range(1, 6)        # 1, 2, 3, 4, 5 (start, stop)
range(0, 10, 2)    # 0, 2, 4, 6, 8 (start, stop, step)
range(5, 0, -1)    # 5, 4, 3, 2, 1 (backwards)
```

### Position Formula
```python
x = start_position + i * spacing

# Example: x = 100 + i * 50
# i=0: x = 100
# i=1: x = 150
# i=2: x = 200
```

### For Loop Structure
```python
for variable_name in range(count):
    # Code here uses variable_name
    # Runs 'count' times
```

## Common Errors

### Error: "TypeError: 'float' object cannot be interpreted as an integer"
**What it means:** Range requires integers (whole numbers)
**How to fix:** Use `range(5)` not `range(5.5)`. Convert floats: `range(int(5.7))`

### Error: Range produces no values
**What it means:** Stop value is less than or equal to start value
**How to fix:**
- For forward: `range(1, 5)` works, `range(5, 1)` doesn't
- For backward: Use negative step: `range(5, 1, -1)`

### Error: Loop runs one too few or one too many times
**What it means:** Range stops BEFORE the stop value
**How to fix:**
- `range(5)` gives 0-4 (5 numbers)
- `range(1, 6)` gives 1-5 (5 numbers)
- To get 1-5, use `range(1, 6)` NOT `range(1, 5)`

## Debugging Tips

1. **Print range values:** Add `print(list(range(1, 6)))` to see all values
2. **Print positions:** Add `print(f"i={i}, x={x}")` inside loop
3. **Test with small ranges:** Use `range(3)` instead of `range(10)` while debugging
4. **Check your math:** Calculate first and last positions by hand

## Range Examples

```python
# Basic counting
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# Start at 1
for i in range(1, 6):
    print(i)  # 1, 2, 3, 4, 5

# Count by 2s
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8

# Count by 10s
for i in range(0, 100, 10):
    print(i)  # 0, 10, 20, 30, ..., 90

# Backwards
for i in range(5, 0, -1):
    print(i)  # 5, 4, 3, 2, 1
```

## Position Calculation Patterns

```python
# Equal spacing
x = 100 + i * 50  # 100, 150, 200, 250...

# Using the range value directly
for x in range(100, 600, 50):
    can.circle(x, 300, 20)  # x is already the position!

# Centering items
total_items = 5
total_width = 800
spacing = total_width / (total_items + 1)
for i in range(total_items):
    x = spacing * (i + 1)  # Evenly distributed
```

## Related Lessons
- **Lesson 2:** First introduction to for loops
- **Next:** Lesson 7 uses lists to store different values for each iteration

## Extra Challenges

1. **Backwards row:** Use `range(5, 0, -1)` to number flowers 5 down to 1
2. **Every third:** Use step value to draw every 3rd position
3. **Two-row garden:** Create two for loops with different y positions
4. **Centered spacing:** Calculate spacing to perfectly center all flowers
5. **Alternating sizes:** Use modulo with loop variable to alternate flower sizes
6. **Custom spacing:** Make spacing increase as i increases (not constant)
