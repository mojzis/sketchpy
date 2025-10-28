# Compound Conditions

## What You'll Learn
- **Programming:** Logical operators (and, or, not), complex decision trees, condition combinations
- **Drawing:** Smart garden with multiple decision factors

## Logical Operators

You can combine multiple conditions using logical operators:

- `and` - Both conditions must be True
- `or` - At least one condition must be True
- `not` - Reverses True/False

```python
is_sunny = True
is_warm = True

# AND: Both must be true
nice_day = is_sunny and is_warm  # True

# OR: At least one must be true
good_weather = is_sunny or is_warm  # True

# NOT: Opposite
is_cloudy = not is_sunny  # False
```

## Truth Tables

Understanding how logical operators work:

```python
# AND truth table
True and True   = True
True and False  = False
False and True  = False
False and False = False

# OR truth table
True or True    = True
True or False   = True
False or True   = True
False or False  = False

# NOT truth table
not True  = False
not False = True
```

## Instructions

### Step 1: Use AND for Multiple Requirements

```python
from sketchpy.shapes import Canvas, CreativeGardenPalette

can = Canvas(800, 600)
can.grid(spacing=50, show_coords=True)

# Garden parameters
is_spring = True
has_water = True

# Draw background
can.rect(0, 0, 800, 350, fill=CreativeGardenPalette.SKY_BREEZE)
can.rect(0, 350, 800, 250, fill=CreativeGardenPalette.MINT_CREAM)

# Draw flowers only if it's spring AND there's water
for i in range(6):
    x = 100 + i * 120
    y = 450

    # Both conditions must be true for flowers to bloom
    if is_spring and has_water:
        # Healthy blooming flowers
        petal_color = CreativeGardenPalette.ROSE_QUARTZ
        center_color = CreativeGardenPalette.BUTTER_YELLOW
    else:
        # Wilted or absent flowers
        petal_color = '#D2B48C'  # Brown
        center_color = '#8B7355'  # Dark brown

    can.circle(x, y, 20, fill=center_color,
               stroke='#000', stroke_width=2)

    can.circle(x, y - 28, 22, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x + 28, y, 22, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x, y + 28, 22, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x - 28, y, 22, fill=petal_color,
               stroke='#000', stroke_width=1.5)
```

**Try it:** Change `has_water` to `False` and see the flowers turn brown!

### Step 2: Use OR for Alternatives

```python
# Draw sun if it's morning OR afternoon (but not evening)
hour = 14  # 2 PM (try values 0-23)

is_morning = hour >= 6 and hour < 12
is_afternoon = hour >= 12 and hour < 18

# Show sun if it's EITHER morning OR afternoon
if is_morning or is_afternoon:
    can.circle(700, 100, 50,
               fill=CreativeGardenPalette.BUTTER_YELLOW,
               stroke=CreativeGardenPalette.LEMON_CHIFFON,
               stroke_width=3)
else:
    # Evening/night - show moon instead
    can.circle(700, 100, 45,
               fill='#F4F4F4',
               stroke='#E0E0E0',
               stroke_width=2)
```

**Try it:** Change `hour` to 8 (morning), 15 (afternoon), or 20 (evening) to see different results.

### Step 3: Complex Conditions with Parentheses

```python
# Draw butterflies only under specific conditions
temperature = 75  # Degrees Fahrenheit
is_sunny = True
wind_speed = 5    # mph

# Butterflies appear when: sunny AND (warm OR light wind)
# Parentheses group conditions like in math
butterflies_visible = is_sunny and (temperature > 70 or wind_speed < 10)

if butterflies_visible:
    # Draw a few butterflies
    for i in range(3):
        bx = 200 + i * 200
        by = 250

        # Simple butterfly shape
        can.ellipse(bx, by, 12, 40, fill=CreativeGardenPalette.LILAC_DREAM,
                    stroke='#000', stroke_width=2)  # Body

        # Wings
        can.circle(bx - 20, by - 10, 18, fill=CreativeGardenPalette.PEACH_WHISPER,
                   stroke='#000', stroke_width=1.5)
        can.circle(bx + 20, by - 10, 18, fill=CreativeGardenPalette.PEACH_WHISPER,
                   stroke='#000', stroke_width=1.5)
        can.circle(bx - 18, by + 10, 15, fill=CreativeGardenPalette.CORAL_BLUSH,
                   stroke='#000', stroke_width=1.5)
        can.circle(bx + 18, by + 10, 15, fill=CreativeGardenPalette.CORAL_BLUSH,
                   stroke='#000', stroke_width=1.5)
```

**Try it:** Change the conditions and see when butterflies appear or disappear.

### Step 4: Use NOT to Reverse Conditions

```python
is_daytime = True
is_raining = False

# Draw rainbow if it's daytime AND not raining
if is_daytime and not is_raining:
    # Draw a simple rainbow arc with circles
    colors = [
        CreativeGardenPalette.ROSE_QUARTZ,
        CreativeGardenPalette.PEACH_WHISPER,
        CreativeGardenPalette.BUTTER_YELLOW,
        CreativeGardenPalette.MINT_CREAM,
        CreativeGardenPalette.SKY_BREEZE,
        CreativeGardenPalette.LILAC_DREAM
    ]

    for i, color in enumerate(colors):
        can.circle(400, 350, 200 + i * 15, fill='none',
                   stroke=color, stroke_width=12)
```

`not is_raining` is true when it's NOT raining.

**Challenge:** Create a complex garden that changes based on season, time of day, weather, and temperature. Use combinations of and, or, and not!

## Common Issues

### Issue: Condition always evaluates the same way
**Solution:** Check your logic carefully. Print the boolean values to debug: `print(f"is_sunny: {is_sunny}, is_warm: {is_warm}, result: {is_sunny and is_warm}")`

### Issue: "SyntaxError: invalid syntax" with and/or/not
**Solution:** These must be lowercase. Python uses `and`, `or`, `not` (not AND, OR, NOT).

### Issue: Unexpected results with complex conditions
**Solution:** Use parentheses to group conditions clearly. `a and b or c` might not mean what you think - use `(a and b) or c` or `a and (b or c)`.
