# Phase 3: Multi-Lesson Support

**Status**: ⬜ Not Started

**Prerequisites**: Phase 2 complete

---

## Goal

Enable navigation between multiple lessons with progress tracking.

---

## What Gets Created

```
lessons/
├── 01-first-flower/
├── 02-colorful-garden/      # New lesson
└── 03-geometric-patterns/   # New lesson

templates/index.html          # Landing page
templates/components/sidebar.html  # Dynamic lesson list
static/js/app.js              # Progress tracking
```

---

## Tasks

### 1. Create Additional Lessons

**Lesson 2: Colorful Garden**

```bash
mkdir -p lessons/02-colorful-garden
```

`lessons/02-colorful-garden/lesson.md`:
```markdown
## 🌻 Project 2: Colorful Garden

### Goal
Draw multiple flowers using loops and create a garden scene.

### What you'll learn
- Using `for` loops to draw multiple shapes
- Creating variations with randomness (or patterns)
- Composing complex scenes from simple shapes
- Working with both color palettes

### Steps
1. Create a canvas: `can = Canvas(800, 600)`
2. Draw a background (sky and grass)
3. Use a loop to draw multiple flowers at different positions
4. Experiment with different flower colors and sizes
5. Add details (sun, clouds, butterflies)

### Tips
- Use a `for` loop: `for i in range(5):`
- Vary positions: `x = 100 + i * 150`
- Mix colors from `CreativeGardenPalette` and `CalmOasisPalette`
- Layer elements (draw background first, then flowers)

### Challenge
Can you create a garden with 5-10 flowers? Try adding a sun in the corner and some grass at the bottom!
```

`lessons/02-colorful-garden/starter.py`:
```python
# Create a colorful garden!

can = Canvas(800, 600)

# Background: Sky (top half)
can.rect(0, 0, 800, 300, fill=CalmOasisPalette.SKY_BLUE)

# Background: Grass (bottom half)
can.rect(0, 300, 800, 300, fill=CreativeGardenPalette.MINT_CREAM)

# Draw multiple flowers using a loop
# TODO: Use a for loop to draw 5 flowers

# Example: Draw ONE flower first, then put it in a loop
cx, cy = 150, 250
can.circle(cx, cy, 30, fill=CreativeGardenPalette.ROSE_QUARTZ)
can.circle(cx, cy, 15, fill=CreativeGardenPalette.BUTTER_YELLOW)

# Your turn! Add more flowers with a loop
# for i in range(5):
#     x = 150 + i * 150
#     y = 250
#     # Draw flower at (x, y)

can
```

`lessons/02-colorful-garden/help.md`:
```markdown
## Loop Examples

### Drawing Multiple Shapes
```python
# Draw 5 circles in a row
for i in range(5):
    x = 100 + i * 100
    can.circle(x, 200, 30, fill=Color.RED)
```

### Varying Colors
```python
colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE]
for i, color in enumerate(colors):
    x = 100 + i * 100
    can.circle(x, 200, 30, fill=color)
```

### Creating a Grid
```python
for row in range(3):
    for col in range(4):
        x = 100 + col * 150
        y = 100 + row * 150
        can.circle(x, y, 30, fill=Color.BLUE)
```
```

**Lesson 3: Geometric Patterns**

```bash
mkdir -p lessons/03-geometric-patterns
```

`lessons/03-geometric-patterns/lesson.md`:
```markdown
## 🔷 Project 3: Geometric Patterns

### Goal
Create repeating patterns using shapes and grids.

### What you'll learn
- Nested loops for grid patterns
- Drawing polygons and lines
- Creating symmetry and repetition
- Using the grid helper for alignment

### Steps
1. Enable grid to help with alignment: `can.grid()`
2. Draw a repeating pattern using nested loops
3. Experiment with shapes: circles, rectangles, polygons
4. Try different spacing and colors
5. Create your own unique pattern

### Pattern Ideas
- Checkerboard (alternating colors)
- Concentric circles
- Diagonal lines
- Repeating triangles
- Honeycomb pattern

### Challenge
Can you create a pattern that uses at least 2 different shapes? Try making it symmetrical!
```

`lessons/03-geometric-patterns/starter.py`:
```python
# Create geometric patterns!

can = Canvas(800, 600)

# Show grid for alignment
can.grid(spacing=50, show_coords=True)

# Example: Simple grid of circles
spacing = 80
for row in range(6):
    for col in range(8):
        x = 50 + col * spacing
        y = 50 + row * spacing
        # Alternate colors
        if (row + col) % 2 == 0:
            fill = CalmOasisPalette.OCEAN_DEEP
        else:
            fill = CreativeGardenPalette.LILAC_DREAM
        can.circle(x, y, 20, fill=fill)

# Your turn! Create your own pattern below

can
```

`lessons/03-geometric-patterns/help.md`:
```markdown
## Pattern Recipes

### Checkerboard
```python
size = 50
for row in range(8):
    for col in range(8):
        if (row + col) % 2 == 0:
            x, y = col * size, row * size
            can.rect(x, y, size, size, fill=Color.BLACK)
```

### Concentric Circles
```python
cx, cy = 400, 300
for i in range(10):
    radius = 20 + i * 20
    can.circle(cx, cy, radius, outline=Color.BLUE)
```

### Triangle Pattern
```python
# Use polygon to draw triangles
for i in range(5):
    x = 100 + i * 100
    points = [(x, 100), (x+40, 150), (x-40, 150)]
    can.polygon(points, fill=Color.GREEN)
```
```

### 2. Update `lessons/lessons.yaml`

```yaml
lessons:
  - id: 01-first-flower
    title: "Draw Your First Flower"
    description: "Learn circles, ellipses, and the CreativeGardenPalette"
    difficulty: beginner
    duration: 15

  - id: 02-colorful-garden
    title: "Create a Colorful Garden"
    description: "Draw multiple flowers with loops and create a scene"
    difficulty: beginner
    duration: 20

  - id: 03-geometric-patterns
    title: "Geometric Patterns"
    description: "Use nested loops to create repeating patterns"
    difficulty: intermediate
    duration: 25
```

### 3. Update `templates/components/sidebar.html`

Replace hardcoded content with dynamic Alpine loop:

```html
<div class="lesson-list">
    <h3>Lessons</h3>

    <template x-for="(lessonItem, index) in lessons" :key="lessonItem.id">
        <div class="lesson-item"
             :class="{
                 'active': currentLessonId === lessonItem.id,
                 'completed': isCompleted(lessonItem.id)
             }">
            <a :href="`/lessons/${lessonItem.id}.html`"
               class="lesson-link">
                <span class="lesson-icon"
                      x-text="isCompleted(lessonItem.id) ? '✓' : index + 1"></span>
                <div class="lesson-info">
                    <div class="lesson-title" x-text="lessonItem.title"></div>
                    <div class="lesson-meta">
                        <span class="difficulty" x-text="lessonItem.difficulty"></span>
                        <span class="duration" x-text="`${lessonItem.duration}min`"></span>
                    </div>
                </div>
            </a>
        </div>
    </template>
</div>

<!-- Reset Progress Button -->
<button @click="resetProgress()"
        class="btn-secondary btn-block"
        style="margin-top: 20px; width: 100%;">
    🔄 Reset All Progress
</button>
```

Add CSS for lesson items:

```css
/* In template style section */
.lesson-item {
    margin: 10px 0;
    border-radius: 8px;
    overflow: hidden;
    background: white;
    transition: all 0.2s;
}

.lesson-item:hover {
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.lesson-item.active {
    background: #e3f2fd;
    border-left: 4px solid #2196F3;
}

.lesson-item.completed {
    border-left: 4px solid #4CAF50;
}

.lesson-link {
    display: flex;
    align-items: center;
    padding: 12px;
    text-decoration: none;
    color: inherit;
}

.lesson-icon {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #ddd;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin-right: 12px;
    flex-shrink: 0;
}

.lesson-item.completed .lesson-icon {
    background: #4CAF50;
    color: white;
}

.lesson-item.active .lesson-icon {
    background: #2196F3;
    color: white;
}

.lesson-info {
    flex: 1;
    min-width: 0;
}

.lesson-title {
    font-weight: 500;
    margin-bottom: 4px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.lesson-meta {
    display: flex;
    gap: 8px;
    font-size: 12px;
    color: #666;
}

.difficulty {
    background: #e0e0e0;
    padding: 2px 8px;
    border-radius: 3px;
}

.btn-block {
    display: block;
    width: 100%;
}
```

### 4. Update `static/js/app.js` with Progress Tracking

Add to the `appState()` function:

```javascript
// Add at top of return object:
lessons: window.ALL_LESSONS || [],
currentLessonId: window.CURRENT_LESSON?.id,

// Add these methods:

// Progress Tracking
isCompleted(lessonId) {
    const progress = JSON.parse(localStorage.getItem('lessonProgress') || '{}');
    return !!progress[lessonId];
},

markComplete(lessonId) {
    const progress = JSON.parse(localStorage.getItem('lessonProgress') || '{}');
    progress[lessonId] = {
        completed: true,
        timestamp: new Date().toISOString()
    };
    localStorage.setItem('lessonProgress', JSON.stringify(progress));
    console.log(`Marked lesson ${lessonId} as complete`);
},

resetProgress() {
    if (confirm('Reset all progress? This cannot be undone.')) {
        localStorage.removeItem('lessonProgress');
        location.reload();
    }
},

// Update runCode() to auto-mark complete:
async runCode() {
    if (this.isRunning) return;

    this.isRunning = true;
    this.output = '';
    this.error = '';
    this.activeTab = 'canvas';

    // ... existing code ...

    try {
        await window.pyodide.runPythonAsync(code);
        const result = window.pyodide.globals.get('can');

        if (result && typeof result.to_svg === 'function') {
            const svg = result.to_svg();
            canvasDiv.innerHTML = svg;
            statusSpan.textContent = 'Success! ✓';
            statusSpan.style.color = '#4CAF50';

            // Mark lesson complete on successful run
            this.markComplete(this.currentLessonId);
        } else {
            // ... existing else ...
        }
    } catch (err) {
        // ... existing error handling ...
    } finally {
        this.isRunning = false;
    }
},
```

### 5. Create Landing Page `templates/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Graphics Learning</title>

    <!-- Alpine.js -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            color: white;
            margin-bottom: 60px;
        }

        h1 {
            font-size: 48px;
            margin-bottom: 16px;
        }

        .subtitle {
            font-size: 20px;
            opacity: 0.9;
        }

        .lessons-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }

        .lesson-card {
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .lesson-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }

        .lesson-card.completed {
            border-left: 6px solid #4CAF50;
        }

        .lesson-number {
            display: inline-block;
            width: 40px;
            height: 40px;
            background: #667eea;
            color: white;
            border-radius: 50%;
            text-align: center;
            line-height: 40px;
            font-weight: bold;
            margin-bottom: 16px;
        }

        .lesson-card.completed .lesson-number {
            background: #4CAF50;
        }

        .lesson-card.completed .lesson-number::before {
            content: '✓';
        }

        .lesson-title {
            font-size: 24px;
            margin-bottom: 12px;
            color: #333;
        }

        .lesson-description {
            color: #666;
            margin-bottom: 20px;
            line-height: 1.6;
        }

        .lesson-meta {
            display: flex;
            gap: 12px;
            margin-bottom: 20px;
            font-size: 14px;
        }

        .badge {
            padding: 4px 12px;
            border-radius: 12px;
            background: #e0e0e0;
            color: #666;
        }

        .btn {
            display: inline-block;
            padding: 12px 24px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 500;
            transition: background 0.2s;
        }

        .btn:hover {
            background: #5568d3;
        }

        .btn-success {
            background: #4CAF50;
        }

        .btn-success:hover {
            background: #45a049;
        }

        .reset-section {
            text-align: center;
            margin-top: 40px;
        }

        .reset-btn {
            background: rgba(255,255,255,0.2);
            color: white;
            border: 2px solid white;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
        }

        .reset-btn:hover {
            background: rgba(255,255,255,0.3);
        }
    </style>
</head>
<body x-data="landingState()">
    <div class="container">
        <header>
            <h1>🐍 Python Graphics Learning</h1>
            <p class="subtitle">Learn Python by drawing with code</p>
        </header>

        <div class="lessons-grid">
            <template x-for="(lesson, index) in lessons" :key="lesson.id">
                <div class="lesson-card" :class="{ completed: isCompleted(lesson.id) }">
                    <div class="lesson-number" x-text="isCompleted(lesson.id) ? '' : index + 1"></div>
                    <h2 class="lesson-title" x-text="lesson.title"></h2>
                    <p class="lesson-description" x-text="lesson.description"></p>
                    <div class="lesson-meta">
                        <span class="badge" x-text="lesson.difficulty"></span>
                        <span class="badge" x-text="`${lesson.duration} minutes`"></span>
                    </div>
                    <a :href="`/lessons/${lesson.id}.html`"
                       class="btn"
                       :class="{ 'btn-success': isCompleted(lesson.id) }"
                       x-text="isCompleted(lesson.id) ? 'Continue ✓' : 'Start'">
                    </a>
                </div>
            </template>
        </div>

        <div class="reset-section">
            <button @click="resetProgress()" class="reset-btn">
                🔄 Reset All Progress
            </button>
        </div>
    </div>

    <script>
        window.LESSONS = {{ all_lessons | tojson }};

        function landingState() {
            return {
                lessons: window.LESSONS || [],

                isCompleted(lessonId) {
                    const progress = JSON.parse(localStorage.getItem('lessonProgress') || '{}');
                    return !!progress[lessonId];
                },

                resetProgress() {
                    if (confirm('Reset all progress? This cannot be undone.')) {
                        localStorage.removeItem('lessonProgress');
                        location.reload();
                    }
                }
            }
        }
    </script>
</body>
</html>
```

### 6. Update `scripts/build.py` to Generate Landing Page

Add after building lessons:

```python
# In main() function, after build_lessons():

# Build landing page
logger.info("Building landing page...")
index_template = env.get_template('index.html')
index_html = index_template.render(
    all_lessons=lessons_config['lessons']
)
index_path = output_dir / 'index.html'
index_path.write_text(index_html)
logger.info(f"  → index.html ({len(index_html)} bytes)")
```

---

## Verification Commands

```bash
# 1. Verify lesson structure
ls -la lessons/
# Should show: 01-first-flower/, 02-colorful-garden/, 03-geometric-patterns/

# 2. Validate YAML
uv run python -c "import yaml; lessons = yaml.safe_load(open('lessons/lessons.yaml'))['lessons']; print(f'✓ {len(lessons)} lessons'); assert len(lessons) >= 3"

# 3. Build
uv run build

# 4. Verify all outputs
ls -la output/lessons/
# Should show all lesson HTML files

ls -la output/index.html
# Landing page should exist

# 5. Start server
uv run srv -f &
SERVER_PID=$!
sleep 3
```

### Manual Browser Testing

**Landing Page (`/`):**
- [ ] All 3 lessons displayed in grid
- [ ] Each shows title, description, difficulty, duration
- [ ] "Start" buttons visible
- [ ] Click lesson - navigates to lesson page

**Sidebar Navigation:**
- [ ] Open `/lessons/01-first-flower.html`
- [ ] Sidebar shows all 3 lessons
- [ ] Current lesson (01) highlighted
- [ ] Click lesson 2 - navigates correctly
- [ ] Click lesson 3 - navigates correctly

**Progress Tracking:**
- [ ] Run code in lesson 1 successfully
- [ ] Reload page - checkmark (✓) appears in sidebar
- [ ] Go to landing page - lesson 1 shows checkmark
- [ ] Button changes to "Continue ✓"
- [ ] Run code in lesson 2
- [ ] Both lessons show checkmarks

**Reset Progress:**
- [ ] Click "Reset Progress" in sidebar
- [ ] Confirm dialog appears
- [ ] Accept - page reloads
- [ ] All checkmarks gone
- [ ] localStorage cleared

**Test localStorage:**
```javascript
// Browser console
let progress = JSON.parse(localStorage.getItem('lessonProgress'))
console.log(progress)
// Should show: {
//   "01-first-flower": { completed: true, timestamp: "..." },
//   "02-colorful-garden": { completed: true, timestamp: "..." }
// }
```

**Test All Lessons Load:**
```bash
for lesson in 01-first-flower 02-colorful-garden 03-geometric-patterns; do
  curl -k "https://localhost:8000/lessons/$lesson.html" | grep -q "x-data" && echo "✓ $lesson"
done
```

```bash
# Stop server
kill $SERVER_PID

# Run tests
uv run pytest -v
```

---

## Checklist

- [ ] 2-3 additional lessons created
- [ ] `lessons.yaml` updated
- [ ] Sidebar component made dynamic with `x-for`
- [ ] Progress tracking methods added to `app.js`
- [ ] Auto-mark complete on successful run
- [ ] Landing page created
- [ ] Build generates all lesson pages
- [ ] Build generates landing page
- [ ] All lessons navigate correctly
- [ ] Progress persists across reloads
- [ ] Checkmarks appear after running code
- [ ] Reset progress works
- [ ] All tests pass

---

## Expected Outcome

- ✅ 3+ lessons accessible via navigation
- ✅ Progress persists across sessions
- ✅ Sidebar dynamically shows all lessons
- ✅ Landing page provides lesson overview
- ✅ All lessons load and run independently
- ✅ Completion tracking works
- ✅ Reset progress functional

---

## Troubleshooting

**Sidebar not showing lessons:**
- Check `window.ALL_LESSONS` defined in template
- Verify `lessons` in Alpine state
- Check `x-for` syntax correct

**Progress not persisting:**
- Check `markComplete()` called in `runCode()`
- Verify `localStorage.setItem()` works
- Check browser localStorage not disabled

**Landing page not loading lessons:**
- Verify `{{ all_lessons | tojson }}` in template
- Check `window.LESSONS` defined
- Verify build copies data correctly

---

## Rollback

```bash
# Keep lesson content, revert code if needed
git checkout HEAD -- templates/ static/ scripts/ tests/
```

---

## Commit

```bash
git add lessons/ templates/ static/ scripts/ tests/
git commit -m "Phase 3: Add multi-lesson support with progress tracking"
```

---

## Next Steps

When this phase is complete, optionally proceed to:
**[Phase 4 - Web Worker (Optional)](./alpine-phase-4.md)**

Or stop here - you have a fully functional multi-lesson platform!
