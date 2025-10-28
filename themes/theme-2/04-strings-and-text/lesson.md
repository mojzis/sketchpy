# Strings and Text

## What You'll Learn
- **Programming:** String variables, f-strings (formatted string literals), combining text and numbers
- **Drawing:** Adding text labels to your garden drawings

## Why Use Text?

Text makes your drawings more informative and interesting. You can label flower types, add garden signs, or display information about what you've drawn. In programming, text is called a "string" (a string of characters).

## Strings and F-Strings

A string is text enclosed in quotes:
```python
name = "Rose"           # A simple string
greeting = 'Hello!'     # Single or double quotes both work
```

An f-string (formatted string literal) lets you insert variable values into strings:
```python
flower_count = 5
message = f"I have {flower_count} flowers"  # Result: "I have 5 flowers"
```

The `f` before the quote tells Python this is an f-string, and anything in `{curly braces}` gets evaluated and inserted.

## Instructions

### Step 1: Add a Simple Label

```python
from sketchpy.shapes import Canvas, CreativeGardenPalette

can = Canvas(800, 600)
can.grid(spacing=50, show_coords=True)

# Draw a flower
can.circle(400, 250, 25, fill=CreativeGardenPalette.BUTTER_YELLOW,
           stroke='#000', stroke_width=2)

# Add a text label below the flower
can.text("Sunflower", 400, 320,
         font_size=24, fill='#000', text_anchor='middle')
```

**Text parameters:**
- First two numbers: x and y position (where the text appears)
- `font_size`: How big the text is
- `fill`: Text color
- `text_anchor`: Alignment ('start', 'middle', or 'end')

**Try it:** Change the label to a different flower name like "Daisy" or "Rose".

### Step 2: Use Variables and F-Strings

```python
# Store flower information in variables
flower_name = "Garden Rose"
petal_count = 6

# Draw a flower
center_x = 300
center_y = 200

can.circle(center_x, center_y, 25,
           fill=CreativeGardenPalette.ROSE_QUARTZ,
           stroke='#000', stroke_width=2)

# Use f-string to create a label with the petal count
label = f"{flower_name} ({petal_count} petals)"
can.text(label, center_x, center_y + 80,
         font_size=20, fill='#333', text_anchor='middle')
```

**Try it:** Change the variables to describe different flowers.

### Step 3: Label Multiple Flowers

```python
# List of flower names
flower_names = ["Rose", "Tulip", "Daisy", "Lily", "Violet"]

# Draw and label flowers in a row
for i in range(5):
    x = 100 + i * 140
    y = 300

    # Draw flower center
    can.circle(x, y, 20, fill=CreativeGardenPalette.LEMON_CHIFFON,
               stroke='#000', stroke_width=2)

    # Draw petals
    can.circle(x, y - 28, 22, fill=CreativeGardenPalette.LILAC_DREAM,
               stroke='#000', stroke_width=1.5)
    can.circle(x + 28, y, 22, fill=CreativeGardenPalette.LILAC_DREAM,
               stroke='#000', stroke_width=1.5)
    can.circle(x, y + 28, 22, fill=CreativeGardenPalette.LILAC_DREAM,
               stroke='#000', stroke_width=1.5)
    can.circle(x - 28, y, 22, fill=CreativeGardenPalette.LILAC_DREAM,
               stroke='#000', stroke_width=1.5)

    # Label with flower name and position number
    label = f"{i+1}. {flower_names[i]}"
    can.text(label, x, y + 60,
             font_size=18, fill='#000', text_anchor='middle')
```

**How it works:**
- `flower_names[i]` gets the i-th flower name from the list
- `i+1` shows position starting from 1 instead of 0 (more natural for humans)
- The f-string combines the number and name: "1. Rose", "2. Tulip", etc.

**Challenge:** Add a title at the top of the canvas like "My Flower Garden" using a larger font size.

## Common Issues

### Issue: Text doesn't appear
**Solution:** Check that x and y are within canvas bounds. Also make sure the text color (`fill`) is different from the background.

### Issue: Text is cut off or misaligned
**Solution:** Use `text_anchor='middle'` to center text, or adjust the x position if using 'start' or 'end'.

### Issue: "SyntaxError: f-string: expecting '}'"
**Solution:** Make sure every `{` has a matching `}` in your f-string, and you're not missing any quotes.
