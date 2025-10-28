# Flower Theme

## Visual Style

Simple, sweet, and delicate flower graphics using basic geometric shapes. Focus on soft pastel colors, organic circular arrangements, and achievable drawings that students can create with 10-20 lines of code.

## Core Elements

### Simple Flower (Lessons 1-5)
Circle-based petals arranged around a center:
```python
# Center
can.circle(400, 300, 30, fill=CreativeGardenPalette.BUTTER_YELLOW)

# Petals (6 circles arranged around center)
petal_positions = [(400, 230), (450, 265), (450, 335), (400, 370), (350, 335), (350, 265)]
for x, y in petal_positions:
    can.circle(x, y, 40, fill=CreativeGardenPalette.ROSE_QUARTZ, stroke='#000', stroke_width=2)
```

### Stem and Leaves
Simple vertical lines with oval leaves:
```python
# Stem
can.line(400, 400, 400, 500, stroke=CreativeGardenPalette.SAGE_GREEN, stroke_width=8)

# Leaves (angled ovals)
can.ellipse(370, 450, 30, 15, fill=CreativeGardenPalette.MINT_FRESH)
can.ellipse(430, 470, 30, 15, fill=CreativeGardenPalette.MINT_FRESH)
```

### Butterfly (Advanced)
Symmetric body with circular/oval wings:
```python
# Body
can.ellipse(400, 300, 15, 60, fill='#8B7355')

# Wings (4 circles)
can.circle(365, 285, 40, fill=CreativeGardenPalette.LAVENDER_MIST, stroke='#000', stroke_width=2)
can.circle(435, 285, 40, fill=CreativeGardenPalette.LAVENDER_MIST, stroke='#000', stroke_width=2)
can.circle(370, 320, 30, fill=CreativeGardenPalette.PEACH_WHISPER, stroke='#000', stroke_width=2)
can.circle(430, 320, 30, fill=CreativeGardenPalette.PEACH_WHISPER, stroke='#000', stroke_width=2)
```

## Recommended Colors

**Primary Palette: CreativeGardenPalette**
- ROSE_QUARTZ (#F4C2C2) - soft pink petals
- PEACH_WHISPER (#FFE5B4) - light peach flowers
- BUTTER_YELLOW (#FFF8DC) - flower centers
- LAVENDER_MIST (#E6E6FA) - light purple petals
- POWDER_BLUE (#B0E0E6) - sky/accent
- MINT_FRESH (#98FB98) - leaves
- SAGE_GREEN (#9DC183) - stems/ground

**Secondary Palette: CalmOasisPalette**
- SKY_BLUE (#87CEEB) - backgrounds
- OCEAN_MIST (#B0C4DE) - soft blues
- CORAL_PINK (#F08080) - accent flowers

## Progression

### Level 1 (Lessons 1-5): Foundations
- **L1**: Single simple flower (center + 5-6 petal circles)
- **L2**: Multiple flowers using for loops
- **L3**: Geometric flower patterns (nested loops, grids)
- **L4**: Adding text labels (flower names, garden signs)
- **L5**: Day/night garden scene (conditionals change colors)

### Level 2 (Lessons 6-10): Control Flow
- **L6**: Row of flowers with for loops (spacing calculations)
- **L7**: Multi-colored flower garden (lists of colors)
- **L8**: Flower field grid (nested loops, rows and columns)
- **L9**: Growing garden (while loop adds flowers until canvas full)
- **L10**: Smart garden (compound conditions for flower placement)

### Level 3 (Lessons 11-15): Functions
- **L11**: Flower drawing functions (reusable flower shapes)
- **L12**: Customizable flowers (parameters for size, position, color)
- **L13**: Flower functions with return values (calculate positions, heights)
- **L14**: Garden from data (list of flower dictionaries)
- **L15**: Complete garden scene (flowers, butterflies, sun, grass, paths)

## Example Code Patterns

### Pattern 1: Petal Arrangement (Loop)
```python
import math

center_x, center_y = 400, 300
petal_count = 6
petal_distance = 70

for i in range(petal_count):
    angle = (i / petal_count) * 2 * math.pi
    petal_x = center_x + petal_distance * math.cos(angle)
    petal_y = center_y + petal_distance * math.sin(angle)
    can.circle(petal_x, petal_y, 40, fill=CreativeGardenPalette.ROSE_QUARTZ)
```

### Pattern 2: Simple Flower Function
```python
def draw_flower(can, x, y, petal_color, center_color):
    """Draw a simple flower at position (x, y)"""
    # Center
    can.circle(x, y, 30, fill=center_color, stroke='#000', stroke_width=2)

    # 6 petals
    for i in range(6):
        angle = (i / 6) * 2 * math.pi
        px = x + 60 * math.cos(angle)
        py = y + 60 * math.sin(angle)
        can.circle(px, py, 35, fill=petal_color, stroke='#000', stroke_width=2)
```

### Pattern 3: Garden Ground and Sky
```python
# Sky background
can.rect(0, 0, 800, 400, fill=CreativeGardenPalette.SKY_BLUE)

# Ground
can.rect(0, 400, 800, 200, fill=CreativeGardenPalette.SAGE_GREEN)
```

## Terminology

- **Petal**: The colored circles/ovals around the flower center
- **Center**: The middle circle (usually yellow/brown)
- **Stem**: Vertical line connecting flower to ground
- **Leaves**: Small ovals attached to stem
- **Garden**: Collection of multiple flowers
- **Field**: Grid/pattern of many flowers
- **Butterfly**: Decorative insect with wings
- **Ground level**: Y-coordinate where flowers "sit" (typically y=400-500)

## Teaching Notes

- Start with static coordinates, progress to calculations
- Use `math.pi` and trig functions only in advanced lessons (L8+)
- Keep early flowers axis-aligned (no rotation needed)
- Introduce symmetry concepts through petal arrangement
- Use color variety to make gardens visually interesting
- Grid method is essential for early positioning
- Encourage experimentation with petal counts and sizes
