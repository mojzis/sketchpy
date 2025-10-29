## ⭕ Project 10: Conditional Symmetry

### Goal
Create a mandala where circle properties change based on their position using conditional logic.

### What you'll learn
- Using `if/else` statements to make decisions
- Combining conditions with `and`/`or`
- Creating variation within patterns
- How conditions create visual interest

### Conditional Coloring
Instead of all circles being the same, we can change them based on position:

```python
if i % 2 == 0:  # Even positions
    color = MIST_BLUE
else:  # Odd positions
    color = MIST_ROSE
```

### Compound Conditions
Combine multiple checks:
```python
if i % 3 == 0 and i > 0:  # Every 3rd circle, but not the first
    # Make this circle special!
```

### Steps
1. Create a mandala loop (12 circles)
2. Use `if i % 2 == 0` to check even/odd
3. Assign different colors based on condition
4. Try adding size variations too!

### Pattern Ideas
- **Even/Odd colors**: Blue and rose alternating
- **Every 3rd special**: Bigger circles at positions 0, 3, 6, 9
- **Quadrant colors**: Different colors in different parts of the circle

### Challenge
- Make every 4th circle larger: `if i % 4 == 0: size = 100`
- Vary opacity: `if i % 3 == 0: opacity = 0.4`
- Create a half-mandala: `if i < 6:` only draw first 6
