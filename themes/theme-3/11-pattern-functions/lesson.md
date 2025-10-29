## ⭕ Project 11: Pattern Functions

### Goal
Create a reusable function that draws a mandala, then call it multiple times to create a composition.

### What you'll learn
- Defining functions with `def`
- Function parameters for customization
- Code organization and reusability
- How functions make code cleaner

### Why Functions?
Instead of copying the same mandala code 3 times, we write it once as a function:

```python
def draw_mandala(canvas, cx, cy):
    # Mandala drawing code here
    ...
```

Then call it multiple times:
```python
draw_mandala(can, 200, 200)  # Top-left
draw_mandala(can, 600, 200)  # Top-right
draw_mandala(can, 400, 450)  # Bottom-center
```

### Function Structure
```python
def function_name(parameter1, parameter2):
    """Description of what the function does"""
    # Code that uses the parameters
    return result  # Optional
```

### Steps
1. Define `draw_mandala(canvas, cx, cy)` function
2. Move your mandala code inside the function
3. Use `cx` and `cy` instead of hardcoded center
4. Call the function 3 times with different positions

### Parameters Make Functions Flexible
The function uses `cx` and `cy` instead of fixed numbers, so we can draw mandalas anywhere!

### Challenge
- Add a `color` parameter to customize each mandala
- Add a `size` parameter to make some bigger/smaller
- Create a grid by calling the function in nested loops!
