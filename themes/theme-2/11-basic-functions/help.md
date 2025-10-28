# Help: Basic Functions

## Quick Reference

### Defining a Function
```python
def function_name(parameter1, parameter2):
    """Docstring describing what function does"""
    # Function body (indented)
    # Do something with parameters
```

### Calling a Function
```python
# After defining it, call it:
function_name(value1, value2)
```

### Complete Example
```python
# Define
def draw_circle_at(can, x, y):
    """Draw a circle at position (x, y)"""
    can.circle(x, y, 20, fill='red')

# Call
draw_circle_at(can, 100, 200)  # Draws at (100, 200)
draw_circle_at(can, 300, 400)  # Draws at (300, 400)
```

## Common Errors

### Error: "NameError: name 'my_function' is not defined"
**What it means:** Calling function before defining it
**How to fix:**
- Define function before calling it
- Make sure function definition comes before main() or before where you use it

### Error: "TypeError: function() missing required positional argument"
**What it means:** Not passing all required parameters
**How to fix:**
- If function needs (can, x, y), you must provide all three
- Example: `draw_flower(can, 100, 200)` not `draw_flower(100, 200)`

### Error: "TypeError: function() takes 2 positional arguments but 3 were given"
**What it means:** Passing too many arguments
**How to fix:** Check function definition - only pass what it expects

### Error: Function code runs even without calling it
**What it means:** Code is NOT indented under function
**How to fix:** All function code must be indented one level

## Debugging Tips

1. **Print from inside function:**
   ```python
   def draw_flower(can, x, y):
       print(f"Drawing flower at ({x}, {y})")
       # rest of code
   ```

2. **Test function separately:**
   ```python
   # Call just once to test
   draw_flower(can, 400, 300)
   # If that works, use in loop
   ```

3. **Check parameter order:**
   ```python
   # Function expects: can, x, y
   # Must call with: can, x, y (same order!)
   ```

## Function Naming Conventions

- Use lowercase with underscores: `draw_flower`
- Start with verb: `draw_`, `create_`, `calculate_`
- Be descriptive: `draw_flower` not `df`
- Examples:
  - `draw_butterfly()`
  - `create_garden()`
  - `calculate_position()`

## Parameters vs Arguments

```python
def draw_flower(can, x, y):  # can, x, y are PARAMETERS
    # Function body

draw_flower(my_canvas, 100, 200)  # Values are ARGUMENTS
```

- **Parameters:** Variables in function definition
- **Arguments:** Actual values you pass when calling

## Function Organization

```python
# Good organization:

# 1. All functions first
def draw_flower(can, x, y):
    # ...

def draw_stem(can, x, y):
    # ...

# 2. Then main
def main():
    can = Canvas(800, 600)
    draw_flower(can, 100, 200)
    return can

# 3. Then if __name__ block
if __name__ == '__main__':
    # ...
```

## Functions Calling Functions

```python
def draw_petal(can, x, y):
    can.circle(x, y, 20, fill='pink')

def draw_flower(can, x, y):
    # This function calls another function!
    draw_petal(can, x, y - 30)  # Top
    draw_petal(can, x + 30, y)  # Right
    draw_petal(can, x, y + 30)  # Bottom
    draw_petal(can, x - 30, y)  # Left
```

## Docstrings

Always include a docstring (description) after `def` line:

```python
def draw_flower(can, x, y):
    """Draw a simple flower at position (x, y)

    Args:
        can: Canvas object to draw on
        x: Horizontal position
        y: Vertical position
    """
    # Function code
```

Use triple quotes `"""..."""` for docstrings.

## Related Lessons
- **Lesson 10:** Complex conditions - now organizing code with functions
- **Next:** Lesson 12 explores function parameters in depth

## Extra Challenges

1. **Grass function:** Create `draw_grass(can, x, y)` for a grass tuft
2. **Butterfly function:** Create `draw_butterfly(can, x, y)`
3. **Complete scene:** Create `draw_garden_scene(can)` that draws everything
4. **Leaf function:** Create `draw_leaf(can, x, y, angle)` for angled leaves
5. **Cloud function:** Create `draw_cloud(can, x, y)` using multiple circles
6. **Function library:** Create 5-6 different drawing functions
