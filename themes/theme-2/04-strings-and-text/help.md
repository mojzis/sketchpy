# Help: Strings and Text

## Quick Reference

### String Basics
```python
# Simple strings
name = "Rose"
greeting = 'Hello'

# F-strings (formatted strings)
count = 5
message = f"I have {count} flowers"  # "I have 5 flowers"
```

### Drawing Text
```python
can.text(text, x, y,
         font_size=20,
         fill='#000',
         text_anchor='middle')  # 'start', 'middle', or 'end'
```

### Common F-String Patterns
```python
# Combining text and numbers
f"Flower {number}"

# Multiple variables
f"{name} has {count} petals"

# Math in f-strings
f"Position: {i + 1}"  # Convert 0-based to 1-based counting
```

## Common Errors

### Error: "SyntaxError: f-string: expecting '}'"
**What it means:** Missing closing brace in your f-string
**How to fix:** Make sure every `{` has a matching `}`: `f"Text {variable} more text"`

### Error: "NameError: name 'f' is not defined"
**What it means:** You wrote `f"..."` but Python doesn't recognize the f
**How to fix:** Make sure the `f` is right before the quote with no space: `f"text"` not `f "text"`

### Error: Text doesn't appear on canvas
**What it means:** Text might be outside canvas bounds or same color as background
**How to fix:**
- Check x is between 0 and canvas width
- Check y is between 0 and canvas height
- Use a visible color like `fill='#000'` (black)

### Error: "IndexError: list index out of range"
**What it means:** Trying to access a list element that doesn't exist
**How to fix:** If list has 5 items, valid indices are 0-4. Make sure `range()` matches list length

## Debugging Tips

1. **Print your strings:** Use `print(label)` to see what the f-string creates
2. **Check alignment:** Try different `text_anchor` values to see which looks best
3. **Start with simple text:** Get basic text working before adding f-strings
4. **Watch your quotes:** Strings need matching quotes - `"text"` or `'text'`

## Understanding Text Anchor

```python
# text_anchor controls horizontal alignment:

text_anchor='start'   # Text starts at x position (left-aligned)
# "Text here"
#  ^x position

text_anchor='middle'  # Text centered at x position
#   "Text here"
#       ^x position

text_anchor='end'     # Text ends at x position (right-aligned)
#       "Text here"
#                 ^x position
```

## F-String Examples

```python
# Basic variable insertion
name = "Rose"
f"This is a {name}"  # "This is a Rose"

# Math expressions
i = 3
f"Position {i + 1}"  # "Position 4"

# Multiple variables
x = 100
y = 200
f"At position ({x}, {y})"  # "At position (100, 200)"

# List indexing
flowers = ["Rose", "Tulip", "Daisy"]
i = 1
f"Flower: {flowers[i]}"  # "Flower: Tulip"
```

## Related Lessons
- **Lesson 3:** Nested loops - now we're labeling those patterns
- **Next:** Lesson 5 uses conditionals to change what we draw

## Extra Challenges

1. **Add descriptions:** Label flowers with color info like "Rose (pink)"
2. **Number formatting:** Display coordinates with f"{x:.0f}" to hide decimals
3. **Multi-line info:** Add both a name label and a position label for each flower
4. **Dynamic messages:** Use f-strings to create different messages based on loop variables
5. **Garden stats:** Add a label showing total flower count using `len(flower_names)`
