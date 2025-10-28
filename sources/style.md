# Visual Style Guide for sketchpy Lessons
## Creating Simple, Sweet, Achievable Graphics

### Core Aesthetic Principles

**Simplicity**: Built from basic geometric shapes (circles, rectangles, ovals, lines)
**Delicacy**: Soft pastel colors with gentle contrast
**Sweetness**: Rounded shapes, organic arrangements, friendly proportions
**Achievability**: Students can recreate with 10-20 lines of code

---

## Color Palettes

### Recommended Palette Sets

**Soft Pastels** (like the flower example):
- ROSE_QUARTZ (#F4C2C2) - soft pink
- PEACH_WHISPER (#FFE5B4) - light peach
- BUTTER_YELLOW (#FFF8DC) - pale yellow
- LAVENDER_MIST (#E6E6FA) - light purple
- POWDER_BLUE (#B0E0E6) - soft blue
- MINT_FRESH (#98FB98) - pale green

**Nature Soft**:
- SKY_BLUE (#87CEEB) - gentle sky
- SAGE_GREEN (#9DC183) - muted green
- SAND (#F4E3D7) - warm neutral
- SUNSET_CORAL (#FF9E80) - soft coral

**Sweet Shop**:
- STRAWBERRY_CREAM (#FFB3C1)
- VANILLA (#F3E5AB)
- MINT_CHIP (#B4E7CE)
- BLUEBERRY_SWIRL (#C5D4E8)

---

## Shape Design Patterns

### Pattern 1: Petal/Leaf Arrangements

**Circle Clusters** (like the flower):
```
Center: Small circle (yellow)
Petals: 5-6 larger circles arranged in circle around center
Vary sizes slightly for organic feel
Use consistent spacing (angles: 0°, 60°, 120°, 180°, 240°, 300°)
```

**Oval Overlaps**:
```
Create depth by overlapping ovals
Front petals: full opacity
Back petals: slightly different shade
```

### Pattern 2: Simple Stems & Branches

**Straight Stem**:
```
Single rectangle or line
Width: 8-12 pixels
Color: Soft green
Add 1-2 simple leaves (ovals) at angles
```

**Curved Branch**:
```
Use multiple short lines at slight angles
Creates gentle curve
Add leaves along the curve
```

### Pattern 3: Geometric Harmony

**Concentric Shapes**:
```
Nested circles with increasing sizes
Use color gradation (light to dark or across palette)
Leave visible borders between layers
```

**Symmetrical Grids**:
```
Repeating shape patterns
Vary colors in checkboard or stripe patterns
Keep spacing consistent
```

---

## Three Example Graphics

### Example 1: Simple Potted Plant

**Visual Description**:
- Clay pot (rounded rectangle, terra cotta color)
- 3-5 stems (thin green lines)
- Small circles at stem tops (flower buds)
- Each bud a different pastel color

**Code Structure** (~15 lines):
```python
can = Canvas(800, 600)

# Pot
can.rounded_rect(325, 400, 150, 120, rx=10, 
                 fill='#C17854', stroke='#8B5A3C', stroke_width=2)

# Stems
for x_offset in [-40, -20, 0, 20, 40]:
    can.line(400 + x_offset, 400, 400 + x_offset, 280, 
             stroke='#6B8E23', stroke_width=4)
    # Bud
    can.circle(400 + x_offset, 270, 20, 
               fill=CreativeGardenPalette.ROSE_QUARTZ, 
               stroke='#000', stroke_width=1.5)
```

**Teachable Concepts**: Loops, coordinate math, method chaining

---

### Example 2: Butterfly (Symmetric Beauty)

**Visual Description**:
- Body (vertical oval, brown/gray)
- 4 wings (circles or ovals)
- Symmetric placement
- Antennae (curved lines)
- Optional: spots on wings (tiny circles)

**Code Structure** (~18 lines):
```python
can = Canvas(800, 600)

body_x, body_y = 400, 300

# Body
can.ellipse(body_x, body_y, 15, 60, 
            fill='#8B7355', stroke='#000', stroke_width=2)

# Top wings (larger)
can.circle(body_x - 35, body_y - 15, 40, 
           fill=CreativeGardenPalette.LAVENDER_MIST, 
           stroke='#000', stroke_width=2)
can.circle(body_x + 35, body_y - 15, 40, 
           fill=CreativeGardenPalette.LAVENDER_MIST, 
           stroke='#000', stroke_width=2)

# Bottom wings (smaller)
can.circle(body_x - 30, body_y + 20, 30, 
           fill=CreativeGardenPalette.PEACH_WHISPER, 
           stroke='#000', stroke_width=2)
can.circle(body_x + 30, body_y + 20, 30, 
           fill=CreativeGardenPalette.PEACH_WHISPER, 
           stroke='#000', stroke_width=2)

# Antennae (simple lines)
can.line(body_x, body_y - 30, body_x - 15, body_y - 50, 
         stroke='#000', stroke_width=2)
can.line(body_x, body_y - 30, body_x + 15, body_y - 50, 
         stroke='#000', stroke_width=2)
```

**Teachable Concepts**: Symmetry, coordinate offsets, layering

---

### Example 3: Simple House with Garden

**Visual Description**:
- House body (rectangle, soft cream)
- Triangular roof (polygon, coral/pink)
- Door (small rectangle, brown)
- 2 windows (squares, light blue)
- Ground (green rectangle)
- 3-4 small flowers in front (circles)

**Code Structure** (~20 lines):
```python
can = Canvas(800, 600)

# Sky background
can.rect(0, 0, 800, 600, fill='#E8F4F8')

# Ground
can.rect(0, 400, 800, 200, fill='#9DC183')

# House body
can.rect(250, 250, 300, 200, 
         fill='#FFF8DC', stroke='#8B7355', stroke_width=3)

# Roof
can.polygon([
    (250, 250), (400, 150), (550, 250)
], fill='#FF9E80', stroke='#8B4513', stroke_width=3)

# Door
can.rect(360, 350, 80, 100, 
         fill='#8B4513', stroke='#000', stroke_width=2)

# Windows
can.rect(290, 290, 60, 60, 
         fill='#B0E0E6', stroke='#000', stroke_width=2)
can.rect(450, 290, 60, 60, 
         fill='#B0E0E6', stroke='#000', stroke_width=2)

# Garden flowers
flower_colors = [
    CreativeGardenPalette.ROSE_QUARTZ,
    CreativeGardenPalette.BUTTER_YELLOW,
    CreativeGardenPalette.LAVENDER_MIST
]
for i, color in enumerate(flower_colors):
    x = 280 + i * 80
    # Stem
    can.line(x, 400, x, 480, stroke='#6B8E23', stroke_width=3)
    # Flower
    can.circle(x, 395, 15, fill=color, stroke='#000', stroke_width=1.5)
```

**Teachable Concepts**: Layering (sky→ground→house), lists, loops, polygons

---

## Framework for Creating More

### Step 1: Choose Theme

**Natural Elements**: flowers, trees, butterflies, birds, clouds, sun/moon
**Simple Objects**: houses, cups, books, balloons, kites
**Geometric Patterns**: mandalas, tessellations, abstract arrangements
**Scenes**: garden, park, sky, underwater

### Step 2: Decompose into Primitives

List the basic shapes needed:
- Circles (centers, petals, bubbles)
- Ovals (leaves, petals, bodies)
- Rectangles (stems, buildings, ground)
- Lines (branches, connections)
- Polygons (roofs, stars, complex shapes)

### Step 3: Apply Style Rules

1. **Use stroke**: Everything gets `stroke='#000'` with `stroke_width=1.5-3`
2. **Choose 3-4 colors max**: From palette sets above
3. **Add white space**: Don't crowd the canvas
4. **Make it symmetric or balanced**: Visual harmony
5. **Keep shapes large enough**: Minimum 20px circles, 50px rectangles

### Step 4: Write Incremental Code

Start with:
- Background (if needed)
- Main structure (body, pot, base)
- Details (petals, leaves, decorations)
- Fine touches (dots, borders, highlights)

### Step 5: Test Achievability

Can a student reproduce this with:
- ≤ 25 lines of code?
- Only basic shapes?
- Clear step-by-step logic?

If no, simplify further.

---

## Quick Templates

### Template A: Flower Variations

**Center + Petal Pattern**:
- Change petal count (4, 5, 6, 8)
- Vary petal colors (monochrome, rainbow, gradient)
- Adjust petal size (uniform, decreasing)
- Add multiple flower layers
- Change center size/color

### Template B: Stacked Objects

**Layered Pattern**:
- Background shape (circle, rectangle)
- Mid-layer (smaller shape, different color)
- Detail layer (smallest, accent color)
- Example: Cup (body + handle), Ice cream cone (cone + scoops), Tree (trunk + crown)

### Template C: Repeated Elements

**Grid/Array Pattern**:
- Choose unit shape
- Repeat in row/column
- Vary colors systematically
- Example: Row of trees, field of flowers, flock of birds

### Template D: Simple Scenes

**Background + Foreground**:
- Sky/background rectangle
- Ground/base element
- 1-2 main subjects
- 2-3 small details
- Example: Sunset over ocean, tree on hill, houses on street

---

## Color Selection Workflow

1. **Pick mood**: Happy/energetic → warm colors | Calm/serene → cool colors
2. **Choose 1 dominant color**: This will be most used
3. **Add 2 complementary colors**: Support the dominant
4. **Include 1 accent color**: For small details
5. **Test contrast**: Ensure shapes are distinguishable

**Example Mood Sets**:
- Happy Garden: BUTTER_YELLOW + ROSE_QUARTZ + MINT_FRESH + LAVENDER_MIST
- Ocean Calm: SKY_BLUE + POWDER_BLUE + MINT_FRESH + SAND
- Sunset Warm: PEACH_WHISPER + SUNSET_CORAL + BUTTER_YELLOW + LAVENDER_MIST

---

## Common Pitfalls to Avoid

❌ **Too many colors** (keep to 4-5 max)
❌ **Shapes too small** (hard for students to see coordinates)
❌ **No stroke/borders** (loses definition)
❌ **Complex overlapping** (hard to debug)
❌ **Asymmetric clutter** (visually unbalanced)
❌ **Harsh/bright colors** (not delicate)

✅ **Limited palette** (harmonious)
✅ **Generous sizing** (clear, visible)
✅ **Clear strokes** (defined edges)
✅ **Logical layering** (back to front)
✅ **Balanced composition** (centered or symmetrical)
✅ **Soft pastels** (sweet aesthetic)

---

## Usage in Lessons

### For Starter Code
Create simplified versions (3-5 shapes) that students can:
- Run immediately
- Understand quickly
- Modify easily

### For Challenge Code
Show complete versions (15-25 shapes) that demonstrate:
- Code organization
- Variable usage
- Loop applications
- Function potential

### For Gallery Examples
Generate polished pieces that inspire:
- What's possible
- Creative variations
- Personal expression

---

## Generation Checklist

Before finalizing a graphic:

- [ ] Uses only basic shapes (circles, rects, lines, polygons)
- [ ] 3-5 colors from soft palettes
- [ ] All shapes have strokes (visible borders)
- [ ] Total code ≤ 25 lines
- [ ] Centered or balanced composition
- [ ] No shape smaller than 15px
- [ ] Matches "sweet and delicate" aesthetic
- [ ] Demonstrates a programming concept
- [ ] Students can modify it easily

---

## Next Steps

1. **Test with students**: See which designs engage them most
2. **Build library**: Create 20-30 variations
3. **Categorize by difficulty**: Lesson 1-5 (simple), 6-10 (medium), 11-15 (complex)
4. **Create variants**: Same concept, different themes (flower → butterfly → sun)
5. **Document patterns**: What works well for teaching specific concepts