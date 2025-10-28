## Additional Help

### Common Issues

**Function not doing anything?**

- You defined it but didn't call it! Add `function_name(can)` after the definition
- Make sure you're calling with parentheses: `draw_car(can)` not `draw_car`

**SyntaxError or IndentationError?**

- Function body must be indented (4 spaces or 1 tab)
- Make sure the `def` line ends with a colon `:`
- Everything in the function must be indented the same amount

**Canvas not passed correctly?**

- Function definition: `def draw_car(canvas):`
- Function call: `draw_car(can)`
- The parameter name (canvas) and argument name (can) don't have to match!

**Nothing displays?**

- Make sure `can` is on the last line (outside all functions)
- Functions need to be called to execute

### Understanding the Canvas Parameter

When you write:
```python
def draw_car(canvas):
    canvas.rect(200, 300, 200, 80, fill=Color.RED)

draw_car(can)
```

The `canvas` parameter is a **placeholder** - it receives whatever you pass when calling. When you call `draw_car(can)`, the `can` object becomes `canvas` inside the function.

### Tips

- **Define before calling**: Functions must be defined before you use them
- **One function, one purpose**: Each function should do one clear thing
- **Comment your functions**: Use docstrings or comments to explain
- **Test incrementally**: Write one function, test it, then write the next
- **Build complexity**: Start simple, add details gradually

### Function Definition vs. Function Call

**Definition** (creates the recipe):

```python
def draw_truck(canvas):
    canvas.rect(...)
```

**Call** (uses the recipe):

```python
draw_truck(can)
```

You can call a function as many times as you want!

### Debugging Strategy

1. Check if function is defined (before the call)
2. Check if function is called (with parentheses and canvas)
3. Test the drawing code outside the function first
4. Move working code into the function
5. Verify indentation is correct
