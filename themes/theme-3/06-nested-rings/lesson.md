## ⭕ Project 6: Nested Rings

### Goal
Create concentric circles (like a bullseye) with a gradual drift to one side, creating a mesmerizing ripple effect.

### What you'll learn
- Drawing concentric circles (same center, different sizes)
- Using loop variables to calculate both size and position
- Creating drift effects with incremental offsets
- How nested patterns create depth

### Concentric with Drift
Regular concentric circles all share the same center. But by adding a small offset that increases with each ring, we create a "drifting" effect:

```python
offset_x = i * 6  # Drift increases with each ring
offset_y = i * 4
```

### Steps
1. Set the number of rings (try 12)
2. Set starting radius (largest circle)
3. Loop through rings
4. Calculate drift offset (increases with `i`)
5. Calculate radius (decreases with `i`)
6. Draw circle with offset center

### The Math
- Radius: `280 - (i * 20)` - Gets smaller
- Offset: `i * 6` - Gets bigger
- Result: Circles drift away as they shrink

### Challenge
- Change drift direction: Use negative offsets
- Make it drift in a circle: Use `math.cos(i)` and `math.sin(i)`!
- Try different opacity for each ring
