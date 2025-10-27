## Additional Help

### Common Issues

**Cars all in one spot?**
- Make sure you're calculating x AND y based on col and row
- Check: `x = 50 + col * 180` (not just `x = 50`)
- Check: `y = 100 + row * 180` (not just `y = 100`)

**Wrong number of cars?**
- Count how many you expect: rows × columns
- 3 rows × 4 columns = 12 cars total
- Check your range() values match what you want

**Cars overlapping?**
- Increase spacing: change 180 to 200 or higher
- Make sure car width/height is smaller than spacing
- Use grid to visualize: `can.grid(spacing=50, show_coords=True)`

**All cars same color?**
- Check your if statement is inside both loops
- Verify you're using the calculated color, not a fixed one
- Try simpler pattern first: `if row % 2 == 0:`

### Understanding Nested Loop Execution

Nested loops can be tricky! Here's how they work:

```python
for row in range(2):     # Outer: runs 2 times
    for col in range(3): # Inner: runs 3 times per outer
        print(f"Row {row}, Col {col}")

# Output:
# Row 0, Col 0
# Row 0, Col 1
# Row 0, Col 2
# Row 1, Col 0
# Row 1, Col 1
# Row 1, Col 2
```

**Key point:** The inner loop completes ALL its iterations before the outer loop advances once.

### Position Calculation Tips

```python
# Starting position + (index × spacing)
x = 50 + col * 180
#   ^    ^    ^
#   |    |    spacing between items
#   |    which column (0, 1, 2, 3...)
#   left margin
```

**Example:**
- col=0: x = 50 + 0×180 = 50
- col=1: x = 50 + 1×180 = 230
- col=2: x = 50 + 2×180 = 410

### Modulo (%) Operator

The `%` operator gives you the remainder after division:

```python
0 % 2 = 0  # 0 ÷ 2 = 0 remainder 0
1 % 2 = 1  # 1 ÷ 2 = 0 remainder 1
2 % 2 = 0  # 2 ÷ 2 = 1 remainder 0
3 % 2 = 1  # 3 ÷ 2 = 1 remainder 1
```

Great for alternating patterns!

### Debugging Strategy

1. **Start simple:** Begin with 2×2 grid
2. **Add print statements:**
   ```python
   print(f"Drawing car at row={row}, col={col}, x={x}, y={y}")
   ```
3. **Test one loop first:** Comment out the inner loop and just draw one row
4. **Visualize:** Use `can.grid(spacing=50, show_coords=True)`
5. **Build up:** Once basic grid works, add colors and details

### Tips

- Think "rows of columns" - outer loop does rows, inner does columns
- Always calculate positions using BOTH row and col
- Test your math: do positions make sense?
- Use variables for spacing to adjust easily
- Draw background elements before or after the loops, not inside
