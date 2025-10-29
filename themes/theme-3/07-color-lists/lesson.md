## ⭕ Project 7: Color Lists

### Goal
Create a multi-colored mandala by cycling through a list of colors using the modulo operator.

### What you'll learn
- Creating lists in Python
- Accessing list elements by index
- Using modulo (`%`) to cycle through values
- Combining loops with lists

### Lists in Python
A list holds multiple values:
```python
colors = [
    MathDoodlingPalette.MIST_BLUE,
    MathDoodlingPalette.MIST_ROSE,
    MathDoodlingPalette.MIST_MINT
]
```

### The Modulo Operator (`%`)
Modulo gives the remainder after division:
- `0 % 3 = 0` → colors[0] = MIST_BLUE
- `1 % 3 = 1` → colors[1] = MIST_ROSE
- `2 % 3 = 2` → colors[2] = MIST_MINT
- `3 % 3 = 0` → colors[0] = MIST_BLUE (cycles back!)
- `4 % 3 = 1` → colors[1] = MIST_ROSE

This makes colors repeat: Blue, Rose, Mint, Blue, Rose, Mint...

### Steps
1. Create a list of 3 colors
2. Loop through 12 circles
3. Use `i % 3` to pick a color
4. Draw mandala with alternating colors

### Challenge
- Add more colors to the list
- Use `i % 2` for two-color alternation
- Try `colors[i % len(colors)]` to work with any list size!
