# Phase 0: Content Structure (Foundation)

**Status**: ⬜ Not Started

---

## Goal

Extract current lesson into reusable format without breaking existing system.

---

## What Gets Created

```
lessons/
├── lessons.yaml              # Lesson metadata
└── 01-first-flower/
    ├── lesson.md             # Instructions (extracted from HTML)
    ├── starter.py            # Current starter code
    └── help.md               # Additional help (optional)
```

---

## Tasks

### 1. Add Dependencies

```bash
uv add pyyaml markdown
```

### 2. Create Directory Structure

```bash
mkdir -p lessons/01-first-flower
```

### 3. Create `lessons/lessons.yaml`

Create file with this content:

```yaml
lessons:
  - id: 01-first-flower
    title: "Draw Your First Flower"
    description: "Learn circles, ellipses, and the CreativeGardenPalette"
    difficulty: beginner
    duration: 15
```

### 4. Create `lessons/01-first-flower/lesson.md`

Extract the instructions from `templates/index.html.jinja` (lines 167-218) and convert to Markdown:

```markdown
## 🌸 Project 1: Draw Your First Flower

### Goal
Draw a simple stylized flower using circles and ellipses.

### What you'll learn
- Creating a canvas
- Drawing circles and ellipses
- Using the CreativeGardenPalette
- Positioning shapes with coordinates

### Autocomplete Tip
Type `can.` to see Canvas methods! Press **Tab** or **Enter** to insert working example code with all parameters. Then customize the values!

### Steps
1. Create a canvas: `can = Canvas(800, 600)`
2. Draw petals using circles or ellipses
3. Add a center circle for the flower
4. Draw a stem and leaves

### Coordinate System
The canvas coordinates start at the top-left (0, 0). X increases to the right, Y increases downward.

### Available Methods
- `can.circle(x, y, radius, fill=...)`
- `can.ellipse(x, y, rx, ry, fill=...)`
- `can.rect(x, y, width, height, fill=...)`
- `can.line(x1, y1, x2, y2, stroke=...)`
- `can.grid(spacing=50)` - Show coordinate grid
- `can.show_palette(PaletteClass)` - Display palette colors

### Creative Garden Palette
`CreativeGardenPalette.ROSE_QUARTZ`, `BUTTER_YELLOW`, `MINT_CREAM`, `SKY_BREEZE`, `LILAC_DREAM`, `CORAL_BLUSH`

### Tip
Try `can.show_palette(CreativeGardenPalette)` to see all available colors! Also available: `CalmOasisPalette` and `Color` (basic colors).

### Challenge
Can you add more petals or change colors? Try experimenting with different positions and sizes!
```

### 5. Create `lessons/01-first-flower/starter.py`

Extract the starter code from `templates/index.html.jinja` (lines 231-263):

```python
# Draw your flower here!

can = Canvas(800, 600)

# Draw a coordinate grid to help with positioning
can.grid(spacing=50, show_coords=True)

# Flower center position
cx, cy = 400, 250

# Draw 5 petals around the center (like a simple flower)
petal_radius = 50
can.circle(cx, cy - 60, petal_radius, fill=CreativeGardenPalette.ROSE_QUARTZ)  # Top
can.circle(cx + 50, cy - 30, petal_radius, fill=CreativeGardenPalette.CORAL_BLUSH)  # Top right
can.circle(cx + 50, cy + 30, petal_radius, fill=CreativeGardenPalette.LILAC_DREAM)  # Bottom right
can.circle(cx - 50, cy + 30, petal_radius, fill=CreativeGardenPalette.SKY_BREEZE)  # Bottom left
can.circle(cx - 50, cy - 30, petal_radius, fill=CreativeGardenPalette.PEACH_WHISPER)  # Top left

# Flower center
can.circle(cx, cy, 35, fill=CreativeGardenPalette.BUTTER_YELLOW)

# Stem
can.rect(cx - 5, cy + 35, 10, 200, fill=CreativeGardenPalette.MINT_CREAM)

# Left leaf (ellipse)
can.ellipse(cx - 40, cy + 120, 30, 15, fill=CreativeGardenPalette.HONEYDEW)

# Right leaf (ellipse)
can.ellipse(cx + 40, cy + 180, 30, 15, fill=CreativeGardenPalette.MINT_CREAM)

# Your turn! Add more petals, change colors, or create your own garden!

can
```

### 6. Create `lessons/01-first-flower/help.md` (Optional)

```markdown
## Additional Help

### Common Issues

**Canvas not displaying?**
- Make sure your code ends with `can` on the last line
- Check that you created the canvas: `can = Canvas(800, 600)`

**Colors not working?**
- Use `CreativeGardenPalette.COLOR_NAME` or `Color.COLOR_NAME`
- Try `can.show_palette(CreativeGardenPalette)` to see all colors

**Shapes in wrong position?**
- Use `can.grid(spacing=50, show_coords=True)` to see coordinates
- Remember: (0, 0) is top-left corner

### Tips

- Start simple: draw one shape at a time
- Use variables for positions to make adjustments easier
- Experiment with different sizes and colors
- Build up complexity gradually
```

---

## Verification Commands

```bash
# 1. Verify dependencies installed
uv run python -c "import yaml; import markdown; print('✓ Dependencies OK')"

# 2. Validate YAML syntax
uv run python -c "import yaml; data = yaml.safe_load(open('lessons/lessons.yaml')); print(f'✓ Found {len(data[\"lessons\"])} lesson(s)')"

# 3. Verify lesson files exist
ls -la lessons/01-first-flower/
# Should show: lesson.md, starter.py, help.md

# 4. Test markdown conversion
uv run python -c "import markdown; md = markdown.Markdown(extensions=['fenced_code']); print(md.convert(open('lessons/01-first-flower/lesson.md').read())[:100])"

# 5. Verify old build still works (unchanged)
uv run build

# 6. Start server and test
uv run srv -f &
SERVER_PID=$!
sleep 2
curl -k https://localhost:8000/ | grep -q "Python Graphics" && echo "✓ Server responds"
kill $SERVER_PID

# 7. Run existing tests (should all pass, nothing changed)
uv run pytest -v
```

---

## Checklist

- [ ] Dependencies added (`pyyaml`, `markdown`)
- [ ] Directory structure created
- [ ] `lessons.yaml` created and validates
- [ ] `lesson.md` created with converted content
- [ ] `starter.py` created with extracted code
- [ ] `help.md` created (optional)
- [ ] YAML loads without errors
- [ ] Markdown converts without errors
- [ ] Old build still works
- [ ] All tests pass

---

## Expected Outcome

- ✅ New `lessons/` directory with structured content
- ✅ YAML and Markdown files validate
- ✅ Old system works identically (no changes to build yet)
- ✅ Ready for Phase 1 integration

---

## Rollback

```bash
rm -rf lessons/
git checkout HEAD -- pyproject.toml uv.lock
```

---

## Commit

```bash
git add lessons/ pyproject.toml uv.lock
git commit -m "Phase 0: Add lesson content structure"
```

---

## Next Steps

When this phase is complete, proceed to:
**[Phase 1 - Build + Alpine.js Setup](./alpine-phase-1.md)**
