# Phase 1: Enhanced Build + Alpine.js Setup

**Status**: ⬜ Not Started

**Prerequisites**: Phase 0 complete

---

## Goal

Upgrade build system to support multi-lesson generation and add Alpine.js framework (minimal functionality).

---

## What Gets Created

```
scripts/build.py              # Updated with lesson loader
templates/lesson.html.jinja   # New Alpine-powered template
static/js/app.js              # Minimal Alpine state
output/
├── index.html                # Old version (unchanged, fallback)
├── lessons/
│   └── 01-first-flower.html  # New Alpine version
└── static/data/
    └── lessons.json          # Lesson metadata
```

---

## Tasks

### 1. Update `scripts/build.py`

Add these imports at the top:
```python
import yaml
import markdown
import json
```

Add these classes/functions before `main()`:

```python
class LessonLoader:
    """Load and process lesson content from YAML and Markdown."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.lessons_dir = project_root / 'lessons'
        self.md = markdown.Markdown(extensions=['fenced_code', 'tables'])

    def load_lessons_config(self):
        """Load lessons.yaml"""
        yaml_path = self.lessons_dir / 'lessons.yaml'
        with open(yaml_path, 'r') as f:
            return yaml.safe_load(f)

    def load_lesson_content(self, lesson_id: str):
        """Load lesson markdown, starter code, and optional help."""
        lesson_dir = self.lessons_dir / lesson_id

        content = {}

        # Required files
        content['instructions_html'] = self.md.convert(
            (lesson_dir / 'lesson.md').read_text()
        )
        content['starter_code'] = (lesson_dir / 'starter.py').read_text()

        # Optional files
        help_file = lesson_dir / 'help.md'
        if help_file.exists():
            content['help_html'] = self.md.convert(help_file.read_text())
        else:
            content['help_html'] = '<p>No additional help available.</p>'

        return content


def build_lessons(project_root: Path, shapes_code: str):
    """Build individual lesson pages."""
    loader = LessonLoader(project_root)
    lessons_config = loader.load_lessons_config()

    templates_dir = project_root / 'templates'
    output_dir = project_root / 'output'

    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(templates_dir))

    # Build each lesson
    all_lessons = []
    for lesson_meta in lessons_config['lessons']:
        lesson_id = lesson_meta['id']
        logger.info(f"  Building lesson: {lesson_id}")

        # Load lesson content
        content = loader.load_lesson_content(lesson_id)

        # Merge metadata and content
        lesson_data = {**lesson_meta, **content}
        all_lessons.append(lesson_data)

        # Render lesson page
        template = env.get_template('lesson.html.jinja')
        html = template.render(
            lesson=lesson_data,
            all_lessons=lessons_config['lessons'],
            shapes_code=shapes_code
        )

        # Write output
        lesson_path = output_dir / 'lessons' / f"{lesson_id}.html"
        lesson_path.parent.mkdir(parents=True, exist_ok=True)
        lesson_path.write_text(html)
        logger.info(f"    → lessons/{lesson_id}.html ({len(html)} bytes)")

    # Write lessons.json for client-side use
    lessons_json_path = output_dir / 'static' / 'data' / 'lessons.json'
    lessons_json_path.parent.mkdir(parents=True, exist_ok=True)
    lessons_json_path.write_text(json.dumps(all_lessons, indent=2))
    logger.info(f"  → static/data/lessons.json")
```

Update the `main()` function to call both builders:

```python
def main():
    """Generate index.html from template."""
    # Setup paths
    project_root = Path(__file__).parent.parent
    shapes_path = project_root / 'sketchpy' / 'shapes.py'
    templates_dir = project_root / 'templates'
    output_dir = project_root / 'output'

    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)

    # Process shapes.py code
    shapes_code = process_shapes_code(shapes_path)

    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(templates_dir))

    # Build old single-page version (keep as fallback)
    template = env.get_template('index.html.jinja')
    html_content = template.render(shapes_code=shapes_code)
    output_file = output_dir / 'index.html'
    output_file.write_text(html_content)
    logger.info(f"🔨 Built output/index.html ({len(html_content)} bytes)")

    # Build new multi-lesson version
    build_lessons(project_root, shapes_code)

    logger.info("✅ Build complete!")
```

### 2. Create `templates/lesson.html.jinja`

Copy `templates/index.html.jinja` and make these modifications:

At the top of `<head>`, add Alpine.js:
```html
<!-- Alpine.js -->
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
```

Wrap the `<body>` content in Alpine wrapper:
```html
<body>
    <div x-data="appState()" class="app-container">
        <!-- existing content here -->
    </div>

    <!-- existing scripts... -->

    <!-- Alpine app state -->
    <script src="/static/js/app.js"></script>

    <!-- Inject lesson data -->
    <script>
        window.CURRENT_LESSON = {{ lesson | tojson }};
        window.ALL_LESSONS = {{ all_lessons | tojson }};
    </script>
</body>
```

Replace hardcoded instructions (lines 166-219) with:
```html
<div class="instructions">
    {{ lesson.instructions_html | safe }}
</div>
```

Replace hardcoded starter code (lines 231-263) with:
```html
<textarea id="editor" spellcheck="false">{{ lesson.starter_code }}</textarea>
```

### 3. Create `static/js/app.js`

```javascript
/**
 * Alpine.js app state for sketchpy learning platform
 */

function appState() {
    return {
        // Execution state
        isRunning: false,

        // Current lesson
        lesson: window.CURRENT_LESSON || null,

        // Initialization
        init() {
            console.log('Alpine initialized');
            console.log('Current lesson:', this.lesson?.id);
        }
    }
}

// Make globally available
window.appState = appState;
```

### 4. Create `static/` directory if needed

```bash
mkdir -p static/js
```

---

## Verification Commands

```bash
# 1. Run new build
uv run build

# 2. Verify both outputs generated
ls -la output/index.html output/lessons/01-first-flower.html output/static/data/lessons.json
# All three should exist

# 3. Check file sizes are reasonable
du -h output/index.html output/lessons/01-first-flower.html
# Both should be ~20-30KB

# 4. Verify lessons.json content
cat output/static/data/lessons.json | python -m json.tool | head -20

# 5. Verify static files copied
ls -la output/static/js/app.js

# 6. Start server
uv run srv -f &
SERVER_PID=$!
sleep 3

# 7. Test OLD version still works (unchanged)
curl -k https://localhost:8000/ | grep -q "Python Graphics" && echo "✓ Old version OK"

# 8. Test NEW version loads
curl -k https://localhost:8000/lessons/01-first-flower.html | grep -q "x-data" && echo "✓ Alpine.js present"
curl -k https://localhost:8000/lessons/01-first-flower.html | grep -q "alpinejs" && echo "✓ Alpine CDN linked"

# 9. Test static JS loads
curl -k https://localhost:8000/static/js/app.js | grep -q "appState" && echo "✓ app.js accessible"
```

### Manual Browser Testing

Open: `https://localhost:8000/lessons/01-first-flower.html`

**Browser Console Checks:**
- [ ] "Alpine initialized" appears
- [ ] "Current lesson: 01-first-flower" appears
- [ ] No errors
- [ ] `Alpine.version` returns version like "3.x.x"
- [ ] `Alpine.$data(document.querySelector('[x-data]'))` shows state object

**Functionality Checks:**
- [ ] Page loads and renders
- [ ] Instructions appear (converted from Markdown)
- [ ] CodeMirror editor appears with starter code
- [ ] Pyodide loads (loading message disappears)
- [ ] Run button works
- [ ] Code executes successfully
- [ ] Canvas displays SVG
- [ ] Autocomplete works (type "can." and check dropdown)

```bash
# 10. Run automated tests
uv run pytest tests/test_build.py -v
# May need to update expectations

# 11. Stop server
kill $SERVER_PID
```

---

## Checklist

- [ ] `scripts/build.py` updated with `LessonLoader`
- [ ] `templates/lesson.html.jinja` created with Alpine wrapper
- [ ] `static/js/app.js` created with minimal state
- [ ] Build generates both old and new outputs
- [ ] `lessons.json` generated correctly
- [ ] Alpine.js CDN loads
- [ ] Alpine initializes in browser
- [ ] Old version (`/`) still works
- [ ] New version (`/lessons/01-first-flower.html`) works
- [ ] All existing functionality preserved
- [ ] Tests updated and passing

---

## Expected Outcome

- ✅ Old URL (`/`) works identically
- ✅ New URL (`/lessons/01-first-flower.html`) loads with Alpine.js
- ✅ Alpine.js initializes but doesn't control much yet
- ✅ All existing functionality preserved (editor, Pyodide, autocomplete)
- ✅ Build system supports multi-lesson architecture

---

## Troubleshooting

**Build fails with YAML error:**
- Check `lessons/lessons.yaml` syntax
- Verify indentation (use spaces, not tabs)

**Alpine not initializing:**
- Check browser console for CDN loading errors
- Verify `x-data="appState()"` attribute present
- Check `app.js` loads before Alpine

**Lesson content not appearing:**
- Check Markdown conversion in Python
- Verify `{{ lesson.instructions_html | safe }}` in template
- Check lesson files exist in `lessons/01-first-flower/`

---

## Rollback

```bash
git checkout HEAD -- scripts/build.py templates/ static/ tests/
rm -rf output/lessons/ output/static/data/
```

---

## Document and Commit
use the skills for documenting the changes and commiting them
```bash
git add scripts/build.py templates/lesson.html.jinja static/js/app.js tests/
git commit -m "Phase 1: Add Alpine.js and multi-lesson build system"
```

---

## Next Steps

When this phase is complete, proceed to:
**[Phase 2 - Multi-Panel Alpine UI](./alpine-phase-2.md)**
