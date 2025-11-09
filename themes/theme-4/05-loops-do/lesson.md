## 🎯 Your Turn: Jellyfish Swarm

### Goal
Use loops to create a swarm of jellyfish swimming together.

### Your Mission
Use a `for` loop to draw 6 jellyfish in a row across the canvas.

### Steps
1. Create a loop: `for i in range(6):`
2. Calculate x position: `x = 50 + i * 120`
3. Draw jellyfish at that position
4. Experiment with different spacings and sizes!

### Pattern to Follow
```python
for i in range(???):  # How many jellyfish?
    x = ??? + i * ???  # Starting position + spacing
    ocean.jellyfish(x, y, size=???)
```

### Tips
- Start your jellyfish at x=50 so they don't go off the edge
- Space them about 120 pixels apart (`i * 120`)
- Keep y around 200-300 so they're visible
- Jellyfish sizes look good between 60-100

### Challenge
- Make jellyfish get bigger as they go across (use `i` in the size!)
- Add a second row of jellyfish at a different y position
- Try alternating colors using `if i % 2 == 0:`
