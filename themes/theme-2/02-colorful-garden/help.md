# Help: Colorful Garden

## Quick Reference

### For Loop Syntax
```python
for i in range(5):  # Runs 5 times: i = 0, 1, 2, 3, 4
    # Code here runs each time
    # Use i to calculate positions or vary properties
```

### Range Function
```python
range(5)       # 0, 1, 2, 3, 4
range(3)       # 0, 1, 2
range(1, 6)    # 1, 2, 3, 4, 5 (start at 1, stop before 6)
range(0, 10, 2) # 0, 2, 4, 6, 8 (start, stop, step by 2)
```

### Position Calculation Pattern
```python
x = start_position + i * spacing
# Example: x = 100 + i * 150
# Loop 0: x = 100
# Loop 1: x = 250
# Loop 2: x = 400
```

## Common Errors

### Error: "NameError: name 'i' is not defined"
**What it means:** You're trying to use `i` outside the for loop
**How to fix:** Make sure all code using `i` is indented inside the loop block

### Error: All flowers appear in the same spot
**What it means:** You're not using `i` to change the position
**How to fix:** Use `i` in your calculation: `x = 100 + i * 150` (not just `x = 100`)

### Error: "SyntaxError: invalid syntax" on the for line
**What it means:** Missing colon or incorrect syntax
**How to fix:** For loops need a colon at the end: `for i in range(5):`

### Error: Flowers go off the edge of the canvas
**What it means:** Your position calculations create values too large for the canvas
**How to fix:**
- Check your math: If starting at 100 with 5 flowers spaced 150 apart, last is at 100 + 4*150 = 700
- Reduce spacing, starting position, or number of flowers
- For 800-wide canvas, keep x values between 0 and 800

## Debugging Tips

1. **Print the loop variable:** Add `print(f"i = {i}, x = {x}")` inside your loop to see what values are being used
2. **Start small:** Test with `range(2)` or `range(3)` before doing many iterations
3. **Check your math:** Calculate by hand where the first and last items will appear
4. **Use the grid:** The coordinate grid shows you exactly where 100, 250, 400, etc. are located

## Understanding Modulo (%)

The `%` operator gives you the remainder after division:

```python
0 % 2 = 0    # 0 ÷ 2 = 0 remainder 0
1 % 2 = 1    # 1 ÷ 2 = 0 remainder 1
2 % 2 = 0    # 2 ÷ 2 = 1 remainder 0
3 % 2 = 1    # 3 ÷ 2 = 1 remainder 1
4 % 2 = 0    # 4 ÷ 2 = 2 remainder 0
```

This creates alternating patterns (0, 1, 0, 1, 0, 1...) useful for positioning!

## Related Lessons
- **Lesson 1:** Basic shapes and positioning - what we're repeating here
- **Next:** Lesson 3 uses nested loops to create 2D patterns

## Extra Challenges

1. **Different spacing:** Make flowers closer together or farther apart
2. **Two rows:** Add a second loop to draw flowers at y=400
3. **Alternating heights:** Use modulo to make every other flower higher/lower
4. **Different colors:** Try using different CreativeGardenPalette colors for each flower
5. **Add variety:** Make some flowers bigger or with more petals
6. **Diagonal line:** Use the loop variable to change both x and y positions
