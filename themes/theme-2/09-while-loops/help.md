# Help: While Loops

## Quick Reference

### While Loop Structure
```python
# Initialize variable
x = 0

# Check condition and loop
while x < 100:
    # Do something
    x = x + 10  # Update variable (CRITICAL!)
```

### Three Required Parts
```python
count = 0           # 1. INITIALIZE before loop
while count < 5:    # 2. CHECK condition
    print(count)
    count = count + 1   # 3. UPDATE inside loop
```

### Common Patterns
```python
# Increment by fixed amount
x = x + 10

# Increment by 1
count = count + 1
# or shorter:
count += 1

# Multiple conditions
while x < 800 and y < 600:
    # Runs while BOTH are true
```

## Common Errors

### Error: Program freezes (infinite loop)
**What it means:** Loop condition never becomes false
**How to fix:**
- Make sure you UPDATE the variable inside the loop
- Check that the update moves toward the end condition
- Example: If checking `while x < 800`, must increase x inside loop

### Error: Loop doesn't run at all
**What it means:** Condition is false from the start
**How to fix:**
- Check initial value makes condition true
- `x = 900; while x < 800:` won't run because 900 is not less than 800

### Error: "NameError: name 'x' is not defined"
**What it means:** Forgot to initialize variable before loop
**How to fix:** Add `x = 0` (or starting value) before the while statement

### Error: Loop runs one too many or too few times
**What it means:** Wrong comparison operator
**How to fix:**
- `while x < 800` stops when x reaches 800 (doesn't include 800)
- `while x <= 800` includes 800
- `while x != 800` can overshoot if you increment by more than 1

## Debugging Tips

1. **Print the variable:** Add `print(f"x = {x}")` inside loop to watch it change
2. **Start with small limits:** Test with `while x < 100` before `while x < 800`
3. **Count iterations:** Add `count = 0` before loop, `count += 1` inside, print at end
4. **Add safety limit:** Use `and count < 100` to prevent infinite loops while debugging

## While vs For Loops

### Use FOR when:
- You know exactly how many iterations needed
- Iterating over a list or range
- Example: "Draw 5 flowers"

### Use WHILE when:
- Condition-based stopping
- Don't know exactly how many iterations
- Example: "Draw flowers until canvas is full"

```python
# FOR: Known count
for i in range(10):
    draw_flower()

# WHILE: Until condition
x = 0
while x < canvas_width:
    draw_flower(x)
    x = x + spacing
```

## Multiple Conditions

```python
# AND: Both must be true
while x < 800 and count < 10:
    # Stops when EITHER condition becomes false

# OR: At least one must be true
while x < 800 or keep_going:
    # Stops when BOTH conditions are false
```

## Nested While Loops

```python
y = 0
while y < 600:      # Outer: rows
    x = 0
    while x < 800:  # Inner: columns
        # Draw at (x, y)
        x = x + 100 # Update inner variable
    y = y + 100     # Update outer variable
```

## Related Lessons
- **Lesson 6:** For loops - while loops are more flexible
- **Next:** Lesson 10 uses complex conditions

## Extra Challenges

1. **Row counter:** Draw flowers in rows until y reaches bottom
2. **Alternating colors:** Use a counter to alternate colors each iteration
3. **Decreasing spacing:** Make spacing smaller each time: `spacing = spacing - 5`
4. **Fill canvas:** Use nested while loops to fill entire canvas
5. **Conditional drawing:** Add `if` inside while to skip some positions
6. **Safety limit:** Add counter to prevent more than 100 iterations
