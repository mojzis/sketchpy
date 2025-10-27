## Additional Help

### Common Issues

**"List index out of range" error?**
- Make sure your lists are the same length
- If `colors` has 5 items and `sizes` has 3, you'll get an error
- Check: `len(colors)` should equal `len(sizes)`

**Cars not displaying?**
- Make sure your code ends with `can` on the last line
- Check that you created the canvas: `can = Canvas(800, 600)`

**Colors not working?**
- Use `Color.COLOR_NAME` or `CalmOasisPalette.COLOR_NAME`
- Make sure colors are in a list: `[Color.RED, Color.BLUE]`

**Cars overlapping or off screen?**
- Check your spacing calculation: `x = 50 + i * 150`
- Increase the multiplier (150) to spread cars further apart
- Use `can.grid(spacing=50, show_coords=True)` to see positions

### Understanding enumerate()

`enumerate()` gives you both the index (position) and the value:

```python
colors = [Color.RED, Color.BLUE, Color.GREEN]

# With enumerate
for i, color in enumerate(colors):
    print(f"Index: {i}, Color: {color}")
    # Index: 0, Color: RED
    # Index: 1, Color: BLUE
    # Index: 2, Color: GREEN
```

This is useful because:
- `i` is the position (0, 1, 2, ...)
- `color` is the actual value
- You can use `i` to access other lists: `sizes[i]`

### Tips

- Start simple: create one list of colors first
- Test with just 2-3 items before making longer lists
- Use descriptive variable names: `car_colors`, not just `c`
- Add comments to track what each list represents
- Draw one car manually first, then convert to a loop

### List Indexing Quick Reference

```python
items = ['A', 'B', 'C', 'D']

items[0]   # 'A' - first item
items[1]   # 'B' - second item
items[-1]  # 'D' - last item
len(items) # 4 - number of items
```

Remember: Lists start counting at 0, not 1!
