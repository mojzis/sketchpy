## Additional Help

### Common Issues

**Loop never stops / browser freezes?**
- You forgot to update the loop variable!
- Make sure you have: `x = x + 120` inside the loop
- Check that your update moves toward the exit condition
- If going right, x should increase; if going down, y should increase

**No cars appear?**
- Check that your starting value satisfies the condition
- If `x = 800` and `while x < 750:`, loop never runs!
- Make sure condition is True at the start

**Only one car appears?**
- Check that you're updating the variable: `x = x + 120`
- Verify the update is inside the while loop (indented)
- Make sure you're using the updated variable in drawing

**Too many or too few cars?**
- Adjust the condition: `x < 750` stops when x reaches 750
- Or add a counter: `count < 6` for exactly 6 cars
- Calculate: (end - start) / spacing = number of iterations

### Understanding While Loop Conditions

The loop continues while the condition is **True**:

```python
x = 50
while x < 750:  # True when x is 50, 170, 290...
                # False when x reaches 750 or more
    x = x + 120
```

**Tracing execution:**
- Start: x=50, check 50<750 ✓, draw, update to x=170
- Next: x=170, check 170<750 ✓, draw, update to x=290
- ...continue...
- Later: x=770, check 770<750 ✗, STOP

### For vs While: When to Use Each

**Use `for` when:**
- You know how many times to repeat
- You're iterating over a list
- Example: Draw exactly 5 flowers

**Use `while` when:**
- You repeat until a condition changes
- You don't know how many iterations in advance
- Example: Draw cars until canvas is full

### Counter Patterns

**Basic counter:**
```python
count = 0
while count < 5:
    # Do something
    count = count + 1  # or count += 1
```

**Position counter:**
```python
x = 50
while x < 750:
    # Do something at x
    x = x + 120  # Move to next position
```

**Combined:**
```python
x = 50
count = 0
while x < 750 and count < 8:
    # Do something
    x = x + 120
    count = count + 1
```

### Debugging While Loops

1. **Add print statements:**
   ```python
   while x < 750:
       print(f"x = {x}")  # See what's happening
       # your drawing code
       x = x + 120
   ```

2. **Start with small numbers:**
   - Change condition to `x < 300` to limit iterations
   - Helps you understand the pattern without too many cars

3. **Check your math:**
   - Starting value: 50
   - Update amount: 120
   - End condition: 750
   - How many times will it loop? (750-50)/120 ≈ 6

4. **Verify update direction:**
   - If condition is `x < 750`, x should increase
   - If condition is `x > 0`, x should decrease

### Tips

- While loops are powerful but need careful management
- Always initialize your variables before the loop
- Always update variables inside the loop
- Test with small ranges first
- Use counters to limit iterations during testing
- Combine with if statements for interesting patterns
- Remember: the condition is checked BEFORE each iteration

### Common Patterns

**Move right until edge:**
```python
x = 50
while x < 750:
    # draw at x
    x = x + 120
```

**Count to N:**
```python
count = 0
while count < 10:
    # do something
    count = count + 1
```

**Multiple conditions:**
```python
x = 50
count = 0
while x < 750 and count < 6:
    # draw at x
    x = x + 120
    count = count + 1
```
