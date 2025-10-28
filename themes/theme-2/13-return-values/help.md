# Help: Return Values

## Quick Reference

### Basic Return
```python
def calculate_value(x):
    result = x * 2
    return result  # Send result back

# Capture the return value
answer = calculate_value(10)  # answer = 20
```

### Return Types
```python
def get_number():
    return 42  # Returns integer

def get_text():
    return "Hello"  # Returns string

def check_condition():
    return True  # Returns boolean

def get_color():
    return CreativeGardenPalette.ROSE_QUARTZ  # Returns color
```

### Multiple Return Values
```python
def get_dimensions(size):
    width = size * 2
    height = size * 3
    return width, height  # Returns tuple

# Capture both values
w, h = get_dimensions(10)  # w=20, h=30
```

### Early Return
```python
def get_grade(score):
    if score >= 90:
        return "A"  # Exits immediately
    elif score >= 80:
        return "B"  # Exits immediately
    else:
        return "C"  # Exits immediately
    # No code here runs - already returned!
```

## Common Errors

### Error: "TypeError: 'NoneType' object..."
**What it means:** Function doesn't return anything (returns None)
**How to fix:** Add `return` statement to function

### Error: Can't use return value
**What it means:** Forgot to capture or didn't return anything
**How to fix:**
- Add return: `return result`
- Capture: `value = my_function()`

### Error: Return value is None when it shouldn't be
**What it means:** Return statement not reached or missing
**How to fix:**
- Check indentation of return statement
- Make sure return is inside function
- Verify control flow reaches return

### Error: Code after return doesn't run
**What it means:** This is normal! Return exits the function
**How to fix:** Move code before return statement

## Debugging Tips

1. **Print before returning:**
   ```python
   def calculate(x):
       result = x * 2
       print(f"Returning: {result}")
       return result
   ```

2. **Check what you're returning:**
   ```python
   value = my_function()
   print(f"Got back: {value}, type: {type(value)}")
   ```

3. **Verify return is reached:**
   ```python
   def my_function():
       print("Function started")
       result = 42
       print(f"About to return {result}")
       return result
   ```

## Return vs Print

```python
# Print: shows value, doesn't send it back
def show_value(x):
    print(x * 2)  # Prints "20" for x=10
    # Returns None

# Return: sends value back, doesn't print
def calculate_value(x):
    return x * 2  # Returns 20 for x=10
    # Doesn't print anything

# Usage:
show_value(10)         # Prints 20, result is None
result = calculate_value(10)  # Returns 20, nothing printed
```

## Function Composition

```python
# Functions can use return values from other functions
def double(x):
    return x * 2

def triple(x):
    return x * 3

def six_times(x):
    doubled = double(x)
    result = triple(doubled)
    return result

# Or in one line:
def six_times_short(x):
    return triple(double(x))
```

## Return Value Patterns

### Calculation and Return
```python
def calculate_area(width, height):
    area = width * height
    return area
```

### Conditional Return
```python
def get_status(value):
    if value > 100:
        return "high"
    elif value > 50:
        return "medium"
    else:
        return "low"
```

### Return Multiple Values
```python
def get_min_max(numbers):
    smallest = min(numbers)
    largest = max(numbers)
    return smallest, largest

# Use it:
min_val, max_val = get_min_max([1, 5, 3, 9, 2])
```

### Return Boolean
```python
def is_valid(value):
    return value > 0 and value < 100

# Use in condition:
if is_valid(50):
    # do something
```

## None Return

```python
# Functions without return implicitly return None
def no_return():
    x = 10
    # No return statement

result = no_return()  # result is None
```

## Related Lessons
- **Lesson 12:** Function parameters - now returning calculated results
- **Next:** Lesson 14 combines returns with data structures

## Extra Challenges

1. **Position calculator:** Function that returns (x, y) tuple for centered position
2. **Color picker:** Function that returns color based on multiple conditions
3. **Dimension calculator:** Function returning all sizes needed for complex shape
4. **Validation function:** Returns True/False based on multiple checks
5. **Layout calculator:** Returns list of x positions for evenly spaced items
6. **Gradient calculator:** Returns color based on position in gradient
