# Help: Compound Conditions

## Quick Reference

### Logical Operators
```python
# AND - both must be True
condition1 and condition2

# OR - at least one must be True
condition1 or condition2

# NOT - reverses True/False
not condition
```

### Truth Tables
```python
# AND
True and True   = True
True and False  = False
False and True  = False
False and False = False

# OR
True or True    = True
True or False   = True
False or True   = True
False or False  = False

# NOT
not True  = False
not False = True
```

### Using Parentheses
```python
# Without parentheses (unclear!)
a and b or c

# With parentheses (clear!)
(a and b) or c   # Do a AND b first, then OR with c
a and (b or c)   # Do b OR c first, then AND with a
```

## Common Errors

### Error: "SyntaxError: invalid syntax" with logical operators
**What it means:** Using wrong case or symbols
**How to fix:**
- Use `and` not `AND` or `&&`
- Use `or` not `OR` or `||`
- Use `not` not `NOT` or `!`

### Error: Condition always True or always False
**What it means:** Logic error in your conditions
**How to fix:**
- Print the boolean values: `print(f"a={a}, b={b}, result={a and b}")`
- Check your operator: Did you mean `and` or `or`?
- Verify variable values are what you expect

### Error: "TypeError: unsupported operand type(s)"
**What it means:** Using logical operators on non-boolean values incorrectly
**How to fix:** Make sure comparisons return booleans:
- Good: `x > 5 and y < 10`
- Bad: `x and y` (only works if x and y are boolean)

## Debugging Tips

1. **Print intermediate values:**
   ```python
   print(f"is_sunny: {is_sunny}")
   print(f"is_warm: {is_warm}")
   print(f"nice_day: {is_sunny and is_warm}")
   ```

2. **Break complex conditions into parts:**
   ```python
   # Instead of:
   if is_sunny and temperature > 70 and not is_raining:

   # Try:
   is_warm = temperature > 70
   good_weather = is_sunny and is_warm and not is_raining
   if good_weather:
   ```

3. **Test each condition separately:**
   ```python
   print(f"is_sunny: {is_sunny}")
   print(f"temperature > 70: {temperature > 70}")
   print(f"not is_raining: {not is_raining}")
   ```

## Operator Precedence

Python evaluates in this order:
1. Parentheses `()`
2. `not`
3. `and`
4. `or`

```python
# These are equivalent:
not a or b and c
(not a) or (b and c)

# Use parentheses for clarity!
```

## Common Patterns

### Multiple Requirements (all must be true)
```python
if is_spring and has_water and is_sunny:
    # All three conditions must be true
```

### Alternative Options (any can be true)
```python
if is_spring or is_summer or is_fall:
    # At least one must be true
```

### Excluding Cases
```python
if is_daytime and not is_raining:
    # Daytime but NOT raining
```

### Range Checking
```python
if temperature >= 65 and temperature <= 85:
    # Temperature is between 65 and 85
    # Can also write as: 65 <= temperature <= 85
```

### Complex Decision
```python
# Butterflies visible if: sunny AND (warm OR calm wind)
if is_sunny and (temperature > 70 or wind_speed < 5):
    draw_butterflies()
```

## Comparison Operators

Use these to create boolean values:
```python
x == 5   # Equal to
x != 5   # Not equal to
x < 5    # Less than
x > 5    # Greater than
x <= 5   # Less than or equal to
x >= 5   # Greater than or equal to
```

## Related Lessons
- **Lesson 5:** Basic conditionals - now combining them
- **Next:** Lesson 11 introduces functions

## Extra Challenges

1. **Four seasons:** Use compound conditions to check season based on month
2. **Time of day:** Combine hour checks to determine morning/afternoon/evening/night
3. **Weather combinations:** Check multiple weather variables (temp, rain, wind)
4. **Complex eligibility:** Create a flower that only blooms under very specific conditions
5. **Gradual changes:** Use multiple if/elif with compound conditions for gradual transitions
6. **Boolean functions:** Create variables that store complex boolean expressions
