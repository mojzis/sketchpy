## ⭕ Project 1: First Overlap

### Goal
Draw two overlapping transparent circles and discover the magic of color mixing.

### What you'll learn
- Creating a canvas with a background color
- Drawing circles with the `opacity` parameter
- How transparent shapes blend to create new colors
- Using `stroke='none'` for soft, gradient-like effects

### The Magic of Transparency
When you set `opacity=0.3`, the circle becomes 30% visible. Where two transparent circles overlap, their colors blend together creating a third color! This is the foundation of all Math Doodling patterns.

### Steps
1. Create a canvas with `PAPER_WHITE` background
2. Draw a blue circle on the left
3. Draw a rose circle on the right, overlapping the first
4. Watch the purple blend appear in the middle!

### Key Parameters
- `opacity`: How see-through the shape is (0.0 = invisible, 1.0 = solid)
- `stroke='none'`: No border, creates soft blending
- `fill`: The color of the shape

### Math Doodling Palette
`MathDoodlingPalette.MIST_BLUE`, `MIST_ROSE`, `MIST_MINT` (use with opacity 0.15-0.4)

Backgrounds: `PAPER_WHITE`, `PENCIL_GREY`

### Tip
Start with `opacity=0.3` - it's the sweet spot for beautiful blending!

### Challenge
Try changing the opacity values. What happens at 0.1? At 0.5? Can you make three circles overlap?
