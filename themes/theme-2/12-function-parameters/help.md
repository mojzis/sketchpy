# Help: Function Parameters

## Quick Reference

### Function with Parameters
```python
def function_name(param1, param2, param3):
    """Description"""
    # Use param1, param2, param3 in function

# Call with values
function_name(value1, value2, value3)
```

### Default Parameters
```python
def draw_flower(can, x, y, size=20, color='pink'):
    """size and color have default values"""
    can.circle(x, y, size, fill=color)

# Can call different ways:
draw_flower(can, 100, 200)              # Uses defaults
draw_flower(can, 100, 200, 30)          # Custom size
draw_flower(can, 100, 200, 30, 'blue')  # Custom both
```

### Named Arguments
```python
# Can specify parameter names when calling:
draw_flower(can, x=100, y=200, size=30, color='blue')

# Useful for clarity and skipping defaults:
draw_flower(can, 100, 200, color='blue')  # Use default size
```

## Common Errors

### Error: "TypeError: function() missing required positional argument"
**What it means:** Not providing all required parameters
**How to fix:**
- Function needs (can, x, y, size) → must provide all 4
- Or add default values: `def function(can, x, y, size=20):`

### Error: "TypeError: function() takes 3 positional arguments but 4 were given"
**What it means:** Passing too many arguments
**How to fix:** Check function definition - only pass what it expects

### Error: "TypeError: function() got multiple values for argument 'x'"
**What it means:** Passing same parameter twice (positionally AND named)
**How to fix:**
- Bad: `draw_flower(can, 100, 200, x=150)`
- Good: `draw_flower(can, x=100, y=200)` OR `draw_flower(can, 100, 200)`

### Error: Function ignores my parameter values
**What it means:** Not using the parameter inside function
**How to fix:**
- Bad: `def draw(can, x, y, size): can.circle(100, 200, 20)`
- Good: `def draw(can, x, y, size): can.circle(x, y, size)`

## Debugging Tips

1. **Print parameter values:**
   ```python
   def draw_flower(can, x, y, size):
       print(f"Drawing at ({x}, {y}) with size {size}")
       # rest of function
   ```

2. **Test with simple values:**
   ```python
   # Use round numbers while testing
   draw_flower(can, 100, 200, 20)  # Easy to verify
   ```

3. **Check parameter order:**
   ```python
   # Function definition order must match call order!
   def function(a, b, c):  # Expects a, then b, then c
   function(1, 2, 3)       # Passes 1 to a, 2 to b, 3 to c
   ```

## Parameter Patterns

### Proportional Calculations
```python
def draw_flower(can, x, y, size):
    # Calculate everything relative to size
    center_size = int(size * 0.7)  # 70% of size
    petal_size = size
    petal_distance = int(size * 1.4)  # 1.4x size

    # Now everything scales together!
```

### Multiple Related Parameters
```python
def draw_flower(can, x, y, size, petal_color, center_color):
    # Group related things as parameters
    # Position: x, y
    # Appearance: size, petal_color, center_color
```

### Optional Parameters with Defaults
```python
def draw_flower(can, x, y, size=20, color='pink'):
    # Required: can, x, y
    # Optional: size (defaults to 20), color (defaults to 'pink')
```

## Positional vs Named Arguments

```python
def draw_flower(can, x, y, size, color):
    pass

# Positional: order matters
draw_flower(can, 100, 200, 30, 'pink')

# Named: order doesn't matter
draw_flower(can, color='pink', size=30, y=200, x=100)

# Mixed: positional first, then named
draw_flower(can, 100, 200, size=30, color='pink')
```

## Default Parameter Rules

```python
# Good: defaults at end
def function(required1, required2, optional1=10, optional2=20):
    pass

# Bad: defaults before required
def function(optional1=10, required1, required2):  # SyntaxError!
    pass
```

## Related Lessons
- **Lesson 11:** Basic functions - now making them flexible
- **Next:** Lesson 13 introduces return values

## Extra Challenges

1. **Six parameters:** Add stem_height and stem_color parameters
2. **Validation:** Add checks like `if size < 5: size = 5` to prevent tiny flowers
3. **Calculated defaults:** Use one parameter to calculate another's default
4. **Complex function:** Create function with 8+ parameters for full customization
5. **Named arguments:** Practice calling functions using parameter names
6. **Gradient function:** Create function that draws gradient of flowers with varying sizes
