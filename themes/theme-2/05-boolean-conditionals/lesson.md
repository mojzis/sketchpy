# Boolean Conditionals

## What You'll Learn
- **Programming:** Boolean variables (True/False), if/else statements, comparison operators
- **Drawing:** Creating a garden scene that changes based on conditions (day vs night)

## What Are Booleans?

A boolean is a value that's either `True` or `False`. They're named after George Boole, a mathematician who studied logic. Booleans help your program make decisions.

```python
is_daytime = True
is_raining = False
```

## If/Else Statements

Conditionals let your program do different things based on whether something is true or false:

```python
if is_daytime:
    # Code here runs when is_daytime is True
    sky_color = "light blue"
else:
    # Code here runs when is_daytime is False
    sky_color = "dark blue"
```

Think of it like: "IF it's daytime, use light blue, ELSE use dark blue."

## Instructions

### Step 1: Create a Day/Night Variable

```python
from sketchpy.shapes import Canvas, CreativeGardenPalette

can = Canvas(800, 600)
can.grid(spacing=50, show_coords=True)

# Try changing this to False to see the night scene!
is_daytime = True

# Choose colors based on time of day
if is_daytime:
    sky_color = CreativeGardenPalette.SKY_BREEZE
    ground_color = CreativeGardenPalette.MINT_CREAM
else:
    sky_color = '#2C3E50'  # Dark blue
    ground_color = '#34495E'  # Dark grey-blue

# Draw the sky and ground
can.rect(0, 0, 800, 350, fill=sky_color)
can.rect(0, 350, 800, 250, fill=ground_color)
```

**Try it:** Change `is_daytime` to `False` and see how the colors change!

### Step 2: Add a Sun or Moon

```python
# Draw sun during day, moon at night
if is_daytime:
    # Draw a yellow sun
    can.circle(650, 100, 50,
               fill=CreativeGardenPalette.BUTTER_YELLOW,
               stroke=CreativeGardenPalette.LEMON_CHIFFON,
               stroke_width=3)
else:
    # Draw a pale moon
    can.circle(650, 100, 45,
               fill='#F4F4F4',
               stroke='#E0E0E0',
               stroke_width=2)
```

**Try it:** Make the sun bigger or position it in a different location.

### Step 3: Draw Flowers That Change

```python
# Draw flowers with different colors for day/night
for i in range(5):
    x = 120 + i * 140
    y = 450

    # Flower colors change based on time of day
    if is_daytime:
        petal_color = CreativeGardenPalette.ROSE_QUARTZ
        center_color = CreativeGardenPalette.BUTTER_YELLOW
    else:
        petal_color = CreativeGardenPalette.MISTY_MAUVE  # Darker at night
        center_color = CreativeGardenPalette.LILAC_DREAM  # Softer at night

    # Draw flower center
    can.circle(x, y, 20, fill=center_color,
               stroke='#000', stroke_width=2)

    # Draw petals
    can.circle(x, y - 28, 22, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x + 28, y, 22, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x, y + 28, 22, fill=petal_color,
               stroke='#000', stroke_width=1.5)
    can.circle(x - 28, y, 22, fill=petal_color,
               stroke='#000', stroke_width=1.5)
```

### Step 4: Use Comparison Operators

```python
# Draw different numbers of stars based on hour
hour = 21  # 9 PM (try values from 0-23)

# It's nighttime if hour is less than 6 or greater than 19
is_nighttime = hour < 6 or hour > 19

if is_nighttime:
    # Draw some stars
    can.circle(100, 80, 3, fill='#FFFFFF')
    can.circle(250, 120, 3, fill='#FFFFFF')
    can.circle(400, 60, 3, fill='#FFFFFF')
    can.circle(550, 100, 3, fill='#FFFFFF')
```

**Comparison operators:**
- `<` less than
- `>` greater than
- `==` equal to (note: two equals signs!)
- `!=` not equal to
- `<=` less than or equal to
- `>=` greater than or equal to

**Challenge:** Add more scene variations. Draw rain if `is_raining = True`, or add butterflies only during the day!

## Common Issues

### Issue: My if statement doesn't work
**Solution:** Make sure you have a colon (`:`) at the end of the if line, and the code inside is indented.

### Issue: "SyntaxError: invalid syntax" on if statement
**Solution:** Check for the colon at the end: `if condition:` not `if condition`

### Issue: Both if and else code seem to run
**Solution:** Check your indentation. Code must be indented under the if or else to belong to it.
