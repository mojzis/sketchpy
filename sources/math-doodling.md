# Math Doodling Theme

## Visual Style

Abstract geometric patterns inspired by compass doodling in school notebooks. Focuses on overlapping circles with transparent fills creating hypnotic color mixing effects. Meditative, mathematical, and endlessly explorable.

## Core Aesthetic Principles

**Mathematical Precision**: Circle-based geometry with calculated positions
**Transparency Magic**: Low opacity (0.15-0.4) creates unexpected color mixing
**Minimalism**: 1-3 colors maximum, complexity through overlap
**No Strokes**: Pure gradient blending without hard edges (stroke='none')
**Meditative Quality**: Repetitive patterns encourage calm focus

---

## Color Palette

### MathDoodlingPalette (Triadic)

**Core Colors** (use these primarily):
- MIST_BLUE (#93C5FD) - Soft blue, mathematical calm
- MIST_ROSE (#FCA5A5) - Gentle rose, creative warmth
- MIST_MINT (#86EFAC) - Light mint, harmonious growth

**Extended Shades** (for contrast/variety):
- DEEP_BLUE (#3B82F6) - Deeper blue for emphasis
- WARM_CORAL (#F87171) - Warmer rose for focal points
- FRESH_GREEN (#4ADE80) - Brighter mint for accents

**Backgrounds**:
- PAPER_WHITE (#FAFAFA) - Like notebook paper
- PENCIL_GREY (#E5E7EB) - Subtle guidelines

### Recommended Opacity Levels

- **Subtle layering**: 0.15-0.2 (many overlaps create complexity)
- **Balanced visibility**: 0.25-0.35 (standard for most patterns)
- **Bold emphasis**: 0.4-0.5 (focal points, fewer overlaps)
- **Solid accents**: 1.0 (rare, only for centers or highlights)

---

## Core Pattern Techniques

### Technique 1: Spirograph Circles

Circles arranged in a rotational pattern around a center point.

```python
import math
from sketchpy.shapes import Canvas, MathDoodlingPalette

can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

center_x, center_y = 400, 300
num_circles = 12
orbit_radius = 150
circle_size = 80

for i in range(num_circles):
    angle = (i / num_circles) * 2 * math.pi
    x = center_x + orbit_radius * math.cos(angle)
    y = center_y + orbit_radius * math.sin(angle)

    can.circle(x, y, circle_size,
               fill=MathDoodlingPalette.MIST_BLUE,
               opacity=0.25,
               stroke='none')
```

**Creates**: Flower-like mandala with darker blue in overlaps

**Variations**:
- Change `num_circles` (6, 8, 12, 16, 24)
- Vary `circle_size` relative to `orbit_radius`
- Use two colors alternating (`i % 2`)
- Add inner and outer rings at different radii

---

### Technique 2: Concentric Drift

Nested circles with gradual offset creating ripple effects.

```python
can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

num_rings = 15
start_radius = 280

for i in range(num_rings):
    # Drift increases with each ring
    offset_x = i * 6
    offset_y = i * 4

    radius = start_radius - (i * 18)

    can.circle(400 + offset_x, 300 + offset_y, radius,
               fill=MathDoodlingPalette.MIST_ROSE,
               opacity=0.2,
               stroke='none')
```

**Creates**: Cascading circles like water ripples

**Variations**:
- Change drift direction (negative offsets)
- Vary opacity with radius (fade in or out)
- Use sine wave for offset: `offset_x = math.sin(i * 0.5) * 30`
- Alternate colors on even/odd rings

---

### Technique 3: Vesica Piscis (Overlapping Pairs)

Two circles creating lens-shaped intersections.

```python
can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

# Grid of overlapping pairs
for row in range(3):
    for col in range(4):
        x = 150 + col * 160
        y = 150 + row * 160

        # Left circle
        can.circle(x, y, 80,
                   fill=MathDoodlingPalette.MIST_BLUE,
                   opacity=0.3,
                   stroke='none')

        # Right circle (overlaps by half)
        can.circle(x + 80, y, 80,
                   fill=MathDoodlingPalette.MIST_MINT,
                   opacity=0.3,
                   stroke='none')
```

**Creates**: Grid of lens shapes with teal intersections

**Variations**:
- Vertical pairs instead of horizontal
- Three circles in triangle formation
- Vary spacing (partial vs full overlap)
- Use three different colors for RGB mixing

---

### Technique 4: Fibonacci Spiral

Circles sized by Fibonacci sequence.

```python
import math
can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
x, y = 400, 300

for i, size in enumerate(fib):
    radius = size * 3

    # Spiral outward
    angle = i * 0.6
    x_offset = i * 12 * math.cos(angle)
    y_offset = i * 12 * math.sin(angle)

    # Fade as spiral grows
    opacity = 0.35 - (i * 0.02)

    can.circle(x + x_offset, y + y_offset, radius,
               fill=MathDoodlingPalette.MIST_ROSE,
               opacity=max(0.1, opacity),
               stroke='none')
```

**Creates**: Natural spiral following golden ratio

**Variations**:
- Different sequences (powers of 2, triangular numbers)
- Reverse fade (darker outward)
- Alternate colors in sequence
- Tighter or looser spiral (adjust angle increment)

---

### Technique 5: Symmetrical Mandala

Perfect radial symmetry with multiple layers.

```python
import math
can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

center_x, center_y = 400, 300

# Three layers at different radii
radii = [80, 140, 200]
colors = [
    MathDoodlingPalette.MIST_BLUE,
    MathDoodlingPalette.MIST_ROSE,
    MathDoodlingPalette.MIST_MINT
]

for layer, (orbit, color) in enumerate(zip(radii, colors)):
    num_circles = 8 + (layer * 4)  # More circles in outer layers

    for i in range(num_circles):
        angle = (i / num_circles) * 2 * math.pi
        x = center_x + orbit * math.cos(angle)
        y = center_y + orbit * math.sin(angle)

        can.circle(x, y, 50,
                   fill=color,
                   opacity=0.25,
                   stroke='none')
```

**Creates**: Multi-layered mandala with rainbow intersections

---

## Progression (15 Lessons)

### Level 1: Foundations (Lessons 1-5)

**Lesson 1: First Overlap**
- Concepts: Canvas, circle method, opacity parameter
- Visual: Two overlapping circles showing color mixing
- Code: 5-7 lines

**Lesson 2: Triple Blend**
- Concepts: Multiple statements, three colors
- Visual: Three circles in triangle creating central mix
- Code: 8-10 lines

**Lesson 3: Circle Row**
- Concepts: `for` loop with `range()`
- Visual: Row of overlapping circles (train-like)
- Code: 10-12 lines

**Lesson 4: Opacity Gradient**
- Concepts: Loop variable for calculations
- Visual: Row of circles fading from solid to invisible
- Code: 12-15 lines

**Lesson 5: First Mandala**
- Concepts: Math module, `math.pi`, `math.cos()`, `math.sin()`
- Visual: 8-circle spirograph
- Code: 15-18 lines

---

### Level 2: Mathematical Patterns (Lessons 6-10)

**Lesson 6: Nested Rings**
- Concepts: Loop for concentric circles
- Visual: Bullseye pattern with drift
- Code: 12-15 lines

**Lesson 7: Color Lists**
- Concepts: Lists, indexing with modulo `%`
- Visual: Multi-colored spirograph
- Code: 15-18 lines

**Lesson 8: Grid of Mandalas**
- Concepts: Nested loops for 2D grid
- Visual: 3x3 grid of small spirographs
- Code: 18-22 lines

**Lesson 9: Growing Spiral**
- Concepts: `while` loop, incrementing radius
- Visual: Expanding spiral outward
- Code: 15-20 lines

**Lesson 10: Conditional Symmetry**
- Concepts: `if/else`, boolean conditions
- Visual: Pattern that changes based on position
- Code: 20-25 lines

---

### Level 3: Advanced Compositions (Lessons 11-15)

**Lesson 11: Pattern Functions**
- Concepts: Function definition, parameters
- Visual: Reusable spirograph function
- Code: 25-30 lines

**Lesson 12: Customizable Mandala**
- Concepts: Multiple function parameters
- Visual: Different mandalas with size/color/count params
- Code: 25-30 lines

**Lesson 13: Calculated Layouts**
- Concepts: Functions returning values
- Visual: Automatically positioned mandalas
- Code: 30-35 lines

**Lesson 14: Data-Driven Art**
- Concepts: Dictionaries, list of configs
- Visual: Gallery of patterns from data
- Code: 35-40 lines

**Lesson 15: Meditative Masterpiece**
- Concepts: Integration of all techniques
- Visual: Complex multi-layer composition
- Code: 40-50 lines

---

## Example Starter Code (Lesson 1)

```python
from sketchpy.shapes import Canvas, MathDoodlingPalette

can = Canvas(800, 600, background=MathDoodlingPalette.PAPER_WHITE)

# First circle
can.circle(350, 300, 100,
           fill=MathDoodlingPalette.MIST_BLUE,
           opacity=0.3,
           stroke='none')

# Second circle overlaps
can.circle(450, 300, 100,
           fill=MathDoodlingPalette.MIST_ROSE,
           opacity=0.3,
           stroke='none')

can
```

**Visual Result**: Two translucent circles - blue on left, rose on right, purple-ish blend in middle.

**Learning Moment**: "See how the overlap creates a new color? That's the magic of transparency!"

---

## Teaching Notes

### Why This Theme Works

1. **Instant Gratification**: Even 2 circles create something beautiful
2. **Mathematical Intuition**: Students see geometry come alive
3. **Forgiving**: No "wrong" results - all patterns are valid art
4. **Scalable**: Same concepts work from beginner to advanced
5. **Meditative**: Repetitive patterns encourage calm, focused learning
6. **Universal**: Abstract art transcends cultural/age boundaries

### Key Differences from Flower Theme

| Aspect | Flowers | Math Doodling |
|--------|---------|---------------|
| **Shapes** | Varied (circles, ovals, rectangles) | Circles only |
| **Colors** | 3-5 pastels, opaque | 1-3 colors, transparent |
| **Strokes** | Always visible | Always 'none' |
| **Subject** | Real-world objects | Pure abstraction |
| **Math** | Minimal (positions) | Heavy (trig, sequences) |
| **Mood** | Sweet, cheerful | Calm, meditative |

### Progression Strategy

- **Early lessons (1-5)**: Focus on opacity and overlap magic
- **Middle lessons (6-10)**: Introduce math concepts through patterns
- **Late lessons (11-15)**: Emphasize functions and data structures

### Common Student Discoveries

- "If I overlap 3 circles, I get 7 different color regions!"
- "The Fibonacci spiral looks like a nautilus shell"
- "I can make a rainbow by rotating through the color list"
- "Lower opacity = more layers needed for rich color"

---

## Anti-Patterns to Avoid

❌ **Using strokes** (breaks the gradient aesthetic)
❌ **Too many colors** (muddy mixing, loses clarity)
❌ **Opacity too high** (>0.5, doesn't blend well)
❌ **Opacity too low** (<0.1, invisible even with many layers)
❌ **No background** (white default doesn't show PAPER_WHITE intent)
❌ **Complex shapes** (stick to circles for purity)

✅ **Stroke-free** (pure color blending)
✅ **1-3 colors** (clean, intentional mixes)
✅ **0.15-0.4 opacity** (sweet spot for layering)
✅ **Explicit background** (shows intentionality)
✅ **Pure circles** (geometric perfection)

---

## Quick Reference: Pattern Formulas

### Circular Arrangement
```python
# Points evenly spaced around circle
for i in range(n):
    angle = (i / n) * 2 * math.pi
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
```

### Concentric Rings
```python
# Circles getting smaller inward
for i in range(n):
    radius = max_radius - (i * step)
    can.circle(center_x, center_y, radius, ...)
```

### Spiral
```python
# Growing outward in spiral
for i in range(n):
    angle = i * angle_increment
    distance = i * distance_increment
    x = center_x + distance * math.cos(angle)
    y = center_y + distance * math.sin(angle)
```

### Grid
```python
# 2D array of shapes
for row in range(rows):
    for col in range(cols):
        x = start_x + col * spacing_x
        y = start_y + row * spacing_y
```

---

## Color Mixing Guide

When overlapping at 0.25 opacity:

**Blue + Rose = Purple tones**
- MIST_BLUE + MIST_ROSE → Soft lavender

**Blue + Mint = Cyan/Teal**
- MIST_BLUE + MIST_MINT → Aqua green

**Rose + Mint = Peachy/Coral**
- MIST_ROSE + MIST_MINT → Warm peach

**All Three = Neutral Grey-Brown**
- MIST_BLUE + MIST_ROSE + MIST_MINT → Subtle taupe

*Experiment to discover more combinations!*

---

## Inspiration Sources

- Islamic geometric art (circles in symmetry)
- Spirograph toy patterns
- Venn diagrams (set theory visualization)
- Sacred geometry (vesica piscis, flower of life)
- Classroom notebook margins
- Kaleidoscope patterns
- Mathematical rose curves
- Atomic orbital visualizations

---

## Next Steps for Lesson Development

1. **Create 15 lesson files** following progression above
2. **Screenshot examples** for each pattern type
3. **Challenge variations** for each lesson
4. **Gallery of student work** (once tested)
5. **Advanced techniques** (gradients within circles, animations)

---

## Terminology

- **Opacity**: How see-through a shape is (0.0 = invisible, 1.0 = solid)
- **Overlap**: When circles are drawn on top of each other
- **Blend**: The mixed color created where transparent circles overlap
- **Spirograph**: Pattern made by circles arranged around a center
- **Mandala**: Radially symmetric pattern (like a flower)
- **Concentric**: Circles sharing the same center but different sizes
- **Vesica Piscis**: Almond shape formed by two overlapping circles
- **Triadic**: Three colors evenly spaced on the color wheel

---

## Generation Checklist

Before finalizing a Math Doodling graphic:

- [ ] Uses only circles (no other shapes except background)
- [ ] 1-3 colors from MathDoodlingPalette
- [ ] All circles use `stroke='none'`
- [ ] Opacity between 0.15-0.4 for most shapes
- [ ] Background explicitly set (PAPER_WHITE or PENCIL_GREY)
- [ ] Pattern has mathematical basis (symmetry, sequence, formula)
- [ ] Code ≤ 50 lines
- [ ] Students can modify easily (clear parameters)
- [ ] Creates interesting overlaps (not just isolated circles)

---

*Math Doodling: Where precision meets meditation.*
