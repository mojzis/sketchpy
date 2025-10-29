## ⭕ Project 4: Opacity Gradient

### Goal
Create a row of circles that fade from solid to nearly invisible, demonstrating opacity control.

### What you'll learn
- Using the loop variable for calculations
- Creating gradual changes (gradients)
- How opacity affects visibility
- The relationship between numbers and visual effects

### Opacity Math
We can calculate opacity from the loop variable:
```python
opacity = 0.5 - (i * 0.08)
```
- When i=0: opacity = 0.5 (most visible)
- When i=1: opacity = 0.42
- When i=2: opacity = 0.34
- ...
- When i=5: opacity = 0.1 (barely visible)

### Steps
1. Use a `for` loop with `range(6)`
2. Calculate x position (like before)
3. Calculate opacity: `0.5 - (i * 0.08)`
4. Use the calculated opacity in `can.circle()`

### Fade Direction
The current formula fades from left to right. To reverse it:
```python
opacity = 0.1 + (i * 0.08)  # Fade right to left!
```

### Challenge
- Try different formulas: `0.4 - (i * 0.05)`
- Make it fade faster: `0.5 - (i * 0.1)`
- Create a V-shape fade (hard mode!)
