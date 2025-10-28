# Help: Boolean Conditionals

## Quick Reference

### Boolean Values
```python
is_daytime = True
is_raining = False
```

### If/Else Statement
```python
if condition:
    # Code runs when condition is True
else:
    # Code runs when condition is False
```

### Comparison Operators
```python
x < 5      # Less than
x > 10     # Greater than
x == 5     # Equal to (note: two = signs!)
x != 5     # Not equal to
x <= 5     # Less than or equal to
x >= 10    # Greater than or equal to
```

### Logical Operators
```python
is_daytime and not_raining  # Both must be True
is_daytime or is_sunset     # At least one must be True
not is_daytime              # Opposite of is_daytime
```

## Common Errors

### Error: "SyntaxError: invalid syntax" on if line
**What it means:** Missing colon at the end of if statement
**How to fix:** Add a colon: `if condition:` not `if condition`

### Error: "IndentationError: expected an indented block"
**What it means:** Code after if/else isn't indented
**How to fix:** Indent code that belongs inside the if/else block (use Tab or 4 spaces)

### Error: Using `=` instead of `==`
**What it means:** Single `=` assigns, double `==` compares
**How to fix:**
- Use `x = 5` to assign a value to x
- Use `x == 5` to check if x equals 5

### Error: Both if and else blocks run (or neither runs)
**What it means:** Indentation problem
**How to fix:** Make sure code is indented exactly one level under if/else

## Debugging Tips

1. **Print the condition:** Add `print(f"is_daytime: {is_daytime}")` to see the boolean value
2. **Test both cases:** Try both `True` and `False` to ensure both paths work
3. **Check indentation:** Use consistent indentation (4 spaces recommended)
4. **Watch for typos:** `True` and `False` must be capitalized exactly

## If/Else Patterns

### Simple if/else
```python
if is_daytime:
    color = "yellow"
else:
    color = "dark blue"
```

### If without else
```python
if is_raining:
    # Add umbrella
    can.circle(x, y, 30, fill="blue")
# Code continues whether it rained or not
```

### Multiple conditions with elif
```python
if hour < 6:
    sky = "dark"
elif hour < 12:
    sky = "morning light"
elif hour < 18:
    sky = "afternoon light"
else:
    sky = "evening"
```

## Boolean Logic Examples

```python
# AND: Both must be True
is_daytime = True
is_sunny = True
is_nice = is_daytime and is_sunny  # True

# OR: At least one must be True
is_weekend = False
is_holiday = True
is_free_day = is_weekend or is_holiday  # True

# NOT: Opposite
is_daytime = True
is_nighttime = not is_daytime  # False
```

## Related Lessons
- **Lesson 4:** Strings and text - now we're choosing between options
- **Next:** Lesson 6 explores for loops in more depth

## Extra Challenges

1. **Three states:** Add `elif` for sunset with orange sky colors
2. **Weather conditions:** Add `is_raining` and draw rain if True
3. **Seasons:** Use a `season` variable to change flower colors
4. **Hour-based:** Use hour (0-23) to determine sky color gradient
5. **Interactive changes:** Create several boolean variables and combine them
