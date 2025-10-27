## Additional Help

### Common Issues

**Both conditions drawing at once?**
- Check your indentation - code inside if/else must be indented
- Make sure you're using `if`/`else`, not two separate `if` statements

**Condition never True?**
- Check spelling: `True` and `False` must be capitalized
- For comparisons, use `==` (two equals) not `=` (one equals)
- Example: `if speed == 100:` not `if speed = 100:`

**Nothing showing for one condition?**
- Make sure both if and else blocks have drawing code
- Check that variables used in both blocks are defined before the if

### Boolean Logic

**What are booleans?**
Booleans are True/False values that let your code make decisions:
```python
is_raining = True
is_sunny = False
temperature = 75
```

**If/Else Structure:**
```python
if condition:
    # This runs when condition is True
    can.rect(0, 0, 800, 600, fill="blue")
else:
    # This runs when condition is False
    can.rect(0, 0, 800, 600, fill="yellow")
```

**If/Elif/Else (three or more options):**
```python
if time == "morning":
    can.text(400, 50, "Good morning!")
elif time == "afternoon":
    can.text(400, 50, "Good afternoon!")
else:
    can.text(400, 50, "Good evening!")
```

### Comparison Examples

```python
# Numbers
if speed > 120:
    can.text(400, 50, "Too fast!", fill=Color.RED)

if age >= 18:
    can.text(400, 50, "Adult")

# Strings
if weather == "rainy":
    can.circle(100, 100, 20, fill=Color.BLUE)

# Booleans
if is_night:
    can.circle(700, 100, 40, fill=Color.YELLOW)  # Moon
```

### Common Patterns

**Toggle between two states:**
```python
is_on = True

if is_on:
    can.circle(400, 300, 50, fill=Color.GREEN)
else:
    can.circle(400, 300, 50, fill=Color.RED)
```

**Range checking:**
```python
if speed < 60:
    message = "Too slow"
elif speed >= 60 and speed <= 120:
    message = "Good speed"
else:
    message = "Too fast"

can.text(400, 50, message)
```

**Multiple conditions (and/or):**
```python
if is_night and speed > 100:
    can.text(400, 50, "Dangerous night driving!", fill=Color.RED)

if is_raining or is_snowing:
    can.text(400, 50, "Bad weather")
```

### Tips

- Start simple with just if/else before trying elif
- Test both True and False to see both code paths
- Use clear variable names: `is_night` is better than `n`
- Comment your conditions to explain what they check
