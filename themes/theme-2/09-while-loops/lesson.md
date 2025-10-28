# While Loops

## What You'll Learn
- **Programming:** While loops, condition-based iteration, loop control variables
- **Drawing:** Growing a garden until the canvas is full

## While Loops vs For Loops

A `for` loop runs a specific number of times. A `while` loop runs as long as a condition is true:

```python
# For loop: "Do this 5 times"
for i in range(5):
    print(i)

# While loop: "Keep doing this while x < 500"
x = 0
while x < 500:
    print(x)
    x = x + 100  # IMPORTANT: Update the variable!
```

## The While Loop Pattern

Every while loop needs three parts:
1. **Initialize** the variable before the loop
2. **Check** the condition at each iteration
3. **Update** the variable inside the loop

```python
x = 0           # 1. Initialize
while x < 800:  # 2. Check condition
    # Do something with x
    x = x + 100 # 3. Update (prevents infinite loop!)
```

## Instructions

### Step 1: Draw Flowers While There's Room

```python
from sketchpy.shapes import Canvas, CreativeGardenPalette

can = Canvas(800, 600)
can.grid(spacing=50, show_coords=True)

# Draw ground
can.rect(0, 400, 800, 200, fill=CreativeGardenPalette.MINT_CREAM)

# Draw flowers from left to right until we reach the edge
x = 80  # Start position
flower_spacing = 120

while x < 750:  # Keep going while there's room (750 = 800 - 50 margin)
    y = 450

    # Draw flower
    can.circle(x, y, 20, fill=CreativeGardenPalette.BUTTER_YELLOW,
               stroke='#000', stroke_width=2)

    # Petals
    can.circle(x, y - 28, 22, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)
    can.circle(x + 28, y, 22, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)
    can.circle(x, y + 28, 22, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)
    can.circle(x - 28, y, 22, fill=CreativeGardenPalette.ROSE_QUARTZ,
               stroke='#000', stroke_width=1.5)

    # CRITICAL: Move to next position
    x = x + flower_spacing
```

The loop stops automatically when there's no more room!

**Try it:** Change `flower_spacing` to 100 or 150 and see how it affects the number of flowers.

### Step 2: Use Multiple Conditions

```python
# Draw flowers until we run out of room OR reach 10 flowers
x = 80
count = 0
max_flowers = 10

while x < 750 and count < max_flowers:
    y = 450

    # Draw flower (same as before)
    can.circle(x, y, 20, fill=CreativeGardenPalette.LEMON_CHIFFON,
               stroke='#000', stroke_width=2)

    can.circle(x, y - 28, 22, fill=CreativeGardenPalette.LILAC_DREAM,
               stroke='#000', stroke_width=1.5)
    can.circle(x + 28, y, 22, fill=CreativeGardenPalette.LILAC_DREAM,
               stroke='#000', stroke_width=1.5)
    can.circle(x, y + 28, 22, fill=CreativeGardenPalette.LILAC_DREAM,
               stroke='#000', stroke_width=1.5)
    can.circle(x - 28, y, 22, fill=CreativeGardenPalette.LILAC_DREAM,
               stroke='#000', stroke_width=1.5)

    # Update BOTH variables
    x = x + 120
    count = count + 1
```

The loop stops for whichever condition fails first!

**Try it:** Set `max_flowers` to 3 and see it stop early.

### Step 3: Fill Multiple Rows

```python
y = 380  # Start higher up

while y < 550:  # Keep adding rows until bottom
    x = 80

    while x < 750:  # Fill each row left to right
        # Draw flower
        can.circle(x, y, 18, fill=CreativeGardenPalette.BUTTER_YELLOW,
                   stroke='#000', stroke_width=2)

        # Simple petals
        can.circle(x, y - 25, 20, fill=CreativeGardenPalette.PEACH_WHISPER,
                   stroke='#000', stroke_width=1.5)
        can.circle(x + 25, y, 20, fill=CreativeGardenPalette.PEACH_WHISPER,
                   stroke='#000', stroke_width=1.5)
        can.circle(x, y + 25, 20, fill=CreativeGardenPalette.PEACH_WHISPER,
                   stroke='#000', stroke_width=1.5)
        can.circle(x - 25, y, 20, fill=CreativeGardenPalette.PEACH_WHISPER,
                   stroke='#000', stroke_width=1.5)

        x = x + 120  # Next column

    y = y + 80  # Next row
```

Nested while loops fill the entire space!

**Challenge:** Add a counter to display how many total flowers were drawn. Use `can.text()` to show the count.

## Common Issues

### Issue: Infinite loop - program never stops!
**Solution:** Make sure you update the loop variable inside the loop! Without `x = x + 100`, x never changes and the condition stays true forever.

### Issue: Loop doesn't run at all
**Solution:** Check that your initial value makes the condition true. If you start with `x = 900` and check `while x < 800`, it won't run.

### Issue: Loop runs one too many or too few times
**Solution:** Check your condition carefully. `while x < 800` stops before 800, while `x <= 800` includes 800.
