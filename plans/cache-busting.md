# Cache Busting Implementation Plan

**⚠️ CRITICAL: This plan must be followed EXACTLY as written. Step order matters.**

## Problem Statement

GitHub Pages uses Varnish CDN which ignores query strings in cache keys. This means `script.js?v=123` and `script.js?v=456` are treated as the same file and cached indefinitely. Users see stale JavaScript after deployments.

**Previous attempt:** Content-based hashing (SHA256) failed due to cascade problem:
- `lessonState.js` imports `errorHandler.js`
- Changing `errorHandler.js` changes its hash → `errorHandler.abc123.js`
- But `lessonState.js` still references old name → import breaks
- Would need to rewrite imports inside files → circular dependency hell

**Solution:** Timestamp-based filename versioning with marker pattern.

## Solution Design

### Core Concept

Use a **build timestamp** (YYYYMMDDHHMMSS) as version marker. All files get the same timestamp, avoiding cascade problems.

**Marker pattern:** `.dev.js` in source, replaced with `.{timestamp}.js` in build output.

### File Structure

```
Source (unchanged for tests/dev):
  static/js/
    pyodide-worker.dev.js          ← actual filename
    errorHandler.dev.js
    core/
      lessonState.dev.js
      editorSetup.dev.js
      apiDefinitions.dev.js
    security/
      config.dev.js
      validator.dev.js
      executor.dev.js
    app.dev.js

Build output (timestamped):
  output/static/js/
    pyodide-worker.20231029143022.js
    errorHandler.20231029143022.js
    core/
      lessonState.20231029143022.js
      ...
```

### Import References

**In source files (for tests/dev):**
```js
// static/js/core/lessonState.dev.js
const workerPath = `${basePath}/static/js/pyodide-worker.dev.js`;
const { PyodideErrorHandler } = await import(`${basePath}/static/js/errorHandler.dev.js`);
```

**After build (string replacement):**
```js
// output/static/js/core/lessonState.20231029143022.js
const workerPath = `${basePath}/static/js/pyodide-worker.20231029143022.js`;
const { PyodideErrorHandler } = await import(`${basePath}/static/js/errorHandler.20231029143022.js`);
```

**In templates:**
```jinja
<!-- Before -->
await import(`${basePath}/static/js/core/lessonState.dev.js`)

<!-- After (with build_version var) -->
await import(`${basePath}/static/js/core/lessonState.{{ build_version }}.js`)
```

## File Inventory

### Files to Rename (9 total)

All files in `static/js/` that end with `.js`:

1. `static/js/pyodide-worker.js` → `pyodide-worker.dev.js`
2. `static/js/errorHandler.js` → `errorHandler.dev.js`
3. `static/js/app.js` → `app.dev.js`
4. `static/js/core/lessonState.js` → `lessonState.dev.js`
5. `static/js/core/editorSetup.js` → `editorSetup.dev.js`
6. `static/js/core/apiDefinitions.js` → `apiDefinitions.dev.js`
7. `static/js/security/config.js` → `config.dev.js`
8. `static/js/security/validator.js` → `validator.dev.js`
9. `static/js/security/executor.js` → `executor.dev.js`

### Import References to Update

**In static/js/app.dev.js:**
```js
import { PyodideErrorHandler } from './errorHandler.dev.js';
const workerPath = `${basePath}/static/js/pyodide-worker.dev.js`;
```

**In static/js/core/lessonState.dev.js:**
```js
const workerPath = `${basePath}/static/js/pyodide-worker.dev.js`;
const { PyodideErrorHandler } = await import(`${basePath}/static/js/errorHandler.dev.js`);
```

**In static/js/core/editorSetup.dev.js:**
```js
import { buildApiDefinitions, GENERAL_KEYWORDS } from './apiDefinitions.dev.js';
```

**In static/js/security/executor.dev.js:**
```js
import { SecurityConfig } from './config.dev.js';
```

**In static/js/security/validator.dev.js:**
```js
import { SecurityConfig } from './config.dev.js';
```

**In templates/lesson.html.jinja:**
```js
// Line 33
const { createAppState } = await import(`${basePath}/static/js/core/lessonState.dev.js`);

// Line 143 (DEPRECATED section - keep for reference)
const { PyodideErrorHandler } = await import(`${basePath}/static/js/errorHandler.dev.js`);

// Line 1241
const { initEditor } = await import(`${basePath}/static/js/core/editorSetup.dev.js`);
```

### Template Variables

**In templates/lesson.html.jinja:**
After renaming to `.dev.js`, change dynamic imports:
```jinja
const { createAppState } = await import(`${basePath}/static/js/core/lessonState.{{ build_version }}.js`);
const { initEditor } = await import(`${basePath}/static/js/core/editorSetup.{{ build_version }}.js`);
```

**templates/index.html.jinja:**
- Does NOT import any local JS modules (only Alpine.js from CDN)
- No changes needed

## Implementation Steps

### PHASE 1: Rename Source Files

**Step 1.1:** Rename all 9 JS files to `.dev.js` extension
```bash
cd static/js
mv pyodide-worker.js pyodide-worker.dev.js
mv errorHandler.js errorHandler.dev.js
mv app.js app.dev.js
cd core
mv lessonState.js lessonState.dev.js
mv editorSetup.js editorSetup.dev.js
mv apiDefinitions.js apiDefinitions.dev.js
cd ../security
mv config.js config.dev.js
mv validator.js validator.dev.js
mv executor.js executor.dev.js
```

**Step 1.2:** Update all import statements in source files

In `static/js/app.dev.js`:
```js
// OLD
import { PyodideErrorHandler } from './errorHandler.js';
const workerPath = `${basePath}/static/js/pyodide-worker.js`;

// NEW
import { PyodideErrorHandler } from './errorHandler.dev.js';
const workerPath = `${basePath}/static/js/pyodide-worker.dev.js`;
```

In `static/js/core/lessonState.dev.js`:
```js
// OLD (line 96-97)
? `${basePath}/static/js/pyodide-worker.js`
: `${basePath}/static/js/pyodide-worker.js`;

// NEW
? `${basePath}/static/js/pyodide-worker.dev.js`
: `${basePath}/static/js/pyodide-worker.dev.js`;

// OLD (line 129)
const { PyodideErrorHandler } = await import(`${basePath}/static/js/errorHandler.js`);

// NEW
const { PyodideErrorHandler } = await import(`${basePath}/static/js/errorHandler.dev.js`);
```

In `static/js/core/editorSetup.dev.js`:
```js
// OLD
import { buildApiDefinitions, GENERAL_KEYWORDS } from './apiDefinitions.js';

// NEW
import { buildApiDefinitions, GENERAL_KEYWORDS } from './apiDefinitions.dev.js';
```

In `static/js/security/executor.dev.js` and `static/js/security/validator.dev.js`:
```js
// OLD
import { SecurityConfig } from './config.js';

// NEW
import { SecurityConfig } from './config.dev.js';
```

**Step 1.3:** Verify tests still pass
```bash
npm test
```

### PHASE 2: Update Build Script

**Step 2.1:** Add timestamp generation to `scripts/build.py`

```python
# At top with other imports
from datetime import datetime

# After BASE_PATH constant (around line 16)
BUILD_VERSION = datetime.now().strftime('%Y%m%d%H%M%S')
```

**Step 2.2:** Create function to copy and rename JS files

Add this function before `build_lessons()` (around line 369):

```python
def copy_js_with_timestamp(static_dir: Path, output_dir: Path, timestamp: str):
    """
    Copy JavaScript files from static/js/ to output/static/js/ with timestamp.

    Replaces .dev.js with .{timestamp}.js in:
    - Filenames
    - Import statements inside files

    Returns mapping of original to timestamped filenames for logging.
    """
    js_source = static_dir / 'js'
    js_output = output_dir / 'js'

    if not js_source.exists():
        logger.warning("No static/js directory found")
        return {}

    # Clean old timestamped JS files to prevent accumulation
    if js_output.exists():
        logger.info(f"  Cleaning old JavaScript files from output/static/js/")
        shutil.rmtree(js_output)
    js_output.mkdir(parents=True, exist_ok=True)

    mapping = {}

    # Find all .dev.js files
    for js_file in js_source.rglob('*.dev.js'):
        # Calculate relative path from js_source
        rel_path = js_file.relative_to(js_source)

        # Create timestamped filename
        new_name = js_file.name.replace('.dev.js', f'.{timestamp}.js')
        dest_file = js_output / rel_path.parent / new_name

        # Ensure destination directory exists
        dest_file.parent.mkdir(parents=True, exist_ok=True)

        # Read file content
        content = js_file.read_text()

        # Replace all .dev.js references with timestamped version
        content = content.replace('.dev.js', f'.{timestamp}.js')

        # Write to destination
        dest_file.write_text(content)

        # Track mapping for logging
        mapping[str(rel_path)] = new_name

    return mapping
```

**Step 2.3:** Call the function in build process

In `build_lessons()` function, after copying static files (around line 436-448), ADD:

```python
    # Copy static files (js, css, etc.) to output
    static_src = project_root / 'static'
    static_dest = output_dir / 'static'
    if static_src.exists():
        # Copy static files, but skip the data directory (we just created it)
        # and skip js directory (we'll handle that separately with timestamps)
        for item in static_src.iterdir():
            if item.name not in ('data', 'js'):
                dest = static_dest / item.name
                if item.is_dir():
                    shutil.copytree(item, dest, dirs_exist_ok=True)
                else:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest)
        logger.info(f"  → static/ files copied")

        # Copy JS files with timestamp
        logger.info(f"  Copying JavaScript with timestamp: {BUILD_VERSION}")
        js_mapping = copy_js_with_timestamp(static_src, static_dest, BUILD_VERSION)
        for orig, timestamped in js_mapping.items():
            logger.info(f"    {orig} → {timestamped}")
```

**Step 2.4:** Pass `build_version` to templates

In `build_lessons()`, update template rendering (around line 408-415):

```python
# Render lesson page
template = env.get_template('lesson.html.jinja')
html = template.render(
    lesson=lesson_data,
    current_theme=theme,
    all_themes=themes_config['themes'],
    shapes_code=shapes_code,
    base_path=BASE_PATH,
    build_version=BUILD_VERSION  # ADD THIS LINE
)
```

In `main()`, update index page rendering (around line 488-492):

```python
# Build landing page
logger.info("Building landing page...")
index_template = env.get_template('index.html.jinja')
index_html = index_template.render(
    all_themes=themes_config['themes'],
    snippets=snippets,
    base_path=BASE_PATH,
    build_version=BUILD_VERSION  # ADD THIS LINE
)
```

### PHASE 3: Update Templates

**Step 3.1:** Update `templates/lesson.html.jinja`

Find the module import script (line 33):
```jinja
<!-- OLD -->
const { createAppState } = await import(`${basePath}/static/js/core/lessonState.dev.js`);

<!-- NEW -->
const { createAppState } = await import(`${basePath}/static/js/core/lessonState.{{ build_version }}.js`);
```

Find the editor setup script (line 1241):
```jinja
<!-- OLD -->
const { initEditor } = await import(`${basePath}/static/js/core/editorSetup.dev.js`);

<!-- NEW -->
const { initEditor } = await import(`${basePath}/static/js/core/editorSetup.{{ build_version }}.js`);
```

**Step 3.2:** Check deprecated section

Line 143 has a reference in DEPRECATED comment section - update for consistency:
```jinja
<!-- OLD -->
const { PyodideErrorHandler } = await import(`${basePath}/static/js/errorHandler.js`);

<!-- NEW (inside DEPRECATED comment) -->
const { PyodideErrorHandler } = await import(`${basePath}/static/js/errorHandler.dev.js`);
```

Note: This is in a `<script style="display: none;">` block marked DEPRECATED. It's dead code but update for consistency.

### PHASE 4: Testing

**Step 4.1:** Verify unit tests pass
```bash
npm test
# All 47 tests should pass (36 unit + 11 browser E2E)
```

**Step 4.2:** Build and check output
```bash
uv run build
```

Expected log output:
```
  Copying JavaScript with timestamp: 20231029143022
    pyodide-worker.dev.js → pyodide-worker.20231029143022.js
    errorHandler.dev.js → errorHandler.20231029143022.js
    app.dev.js → app.20231029143022.js
    core/lessonState.dev.js → lessonState.20231029143022.js
    core/editorSetup.dev.js → editorSetup.20231029143022.js
    core/apiDefinitions.dev.js → apiDefinitions.20231029143022.js
    security/config.dev.js → config.20231029143022.js
    security/validator.dev.js → validator.20231029143022.js
    security/executor.dev.js → executor.20231029143022.js
```

**Step 4.3:** Verify output structure
```bash
ls output/static/js/*.js
ls output/static/js/core/*.js
ls output/static/js/security/*.js
```

Should see ONLY `.{timestamp}.js` files (no `.dev.js` files).

**Step 4.4:** Check rendered HTML
```bash
grep -r "lessonState\\..*\\.js" output/lessons/theme-1/01-first-flower.html
```

Should show: `lessonState.20231029143022.js` (with actual timestamp)

**Step 4.5:** Run local server and test
```bash
uv run srv
```

Visit https://localhost:8007/sketchpy/lessons/theme-1/01-first-flower.html

- Check browser console for errors
- Verify code runs
- Check Network tab: files load from timestamped URLs

**Step 4.6:** Run Python tests
```bash
uv run pytest
```

All tests should pass (build tests, browser tests, server tests).

### PHASE 5: Deployment Verification

**Step 5.1:** Deploy to GitHub Pages
```bash
git add .
git commit -m "Add timestamp-based cache busting for JavaScript files"
git push
```

**Step 5.2:** Wait for GitHub Pages deploy (~2 minutes)

**Step 5.3:** Test on production
1. Open https://mojzis.github.io/sketchpy/ in browser
2. Open DevTools → Network tab
3. Visit a lesson page
4. Verify JS files load with timestamp: `lessonState.20231029143022.js`
5. Make a trivial change to `static/js/core/lessonState.dev.js`
6. Rebuild and redeploy
7. Hard refresh browser (Ctrl+Shift+R)
8. Verify new timestamp in Network tab

## Edge Cases and Notes

### Why .dev.js and not .vXXXXX.js in source?

- `.dev.js` clearly indicates "development version"
- Easy to distinguish from built versions
- Won't be confused with version numbers (v1.0.0)
- Convention similar to `.development.js` / `.production.js` pattern

### What about CSS files?

Currently no CSS files in `static/css/`. All styles are inline in templates. If CSS is added later, apply same pattern:
- `styles.dev.css` in source
- `styles.20231029143022.css` in build

### What about pyodide-worker.js?

It's a Web Worker, not an ES6 module. It's loaded via `new Worker(path)`, not `import()`. The timestamp pattern works the same way:
- Source: `pyodide-worker.dev.js`
- Build: `pyodide-worker.20231029143022.js`
- lessonState.dev.js references it dynamically and will be rewritten in build

### What if build takes >1 second?

Timestamp is generated once at start of build script. All files get the same timestamp even if build takes minutes. This is intentional and correct.

### Testing with .dev.js files

Tests import directly from `static/js/`:
```js
import { createAppState } from '../../static/js/core/lessonState.dev.js';
```

This works because:
1. Files are actually named `.dev.js` in source
2. Tests run against source, not build output
3. Build output is in `output/` (ignored by tests)

### Backward compatibility

Old deployed versions will still reference old filenames (without timestamps). This is fine:
- GitHub Pages serves both old and new files
- Old HTML loads old JS (cached but functional)
- New HTML loads new JS (timestamped, not cached)
- No breaking changes for users

### CDN cache TTL

GitHub Pages default cache TTL is 10 minutes for HTML, longer for assets. Filename change bypasses cache entirely - no waiting for TTL expiration.

## Success Criteria

- [ ] All 9 JS files renamed to `.dev.js` in source
- [ ] All imports updated in source files
- [ ] npm test passes (36 unit tests + 11 browser tests)
- [ ] Build script generates timestamp
- [ ] Build script copies files with timestamp in name
- [ ] Build script replaces `.dev.js` → `.{timestamp}.js` in file contents
- [ ] Templates use `{{ build_version }}` variable
- [ ] uv run build succeeds
- [ ] output/ contains only timestamped JS files
- [ ] Local server works (uv run srv)
- [ ] uv run pytest passes
- [ ] Deployed site loads new JS after changes
- [ ] Browser Network tab shows timestamped filenames

## Rollback Plan

If anything breaks:

```bash
# Undo file renames
cd static/js
for f in *.dev.js; do mv "$f" "${f%.dev.js}.js"; done
cd core
for f in *.dev.js; do mv "$f" "${f%.dev.js}.js"; done
cd ../security
for f in *.dev.js; do mv "$f" "${f%.dev.js}.js"; done

# Revert build script changes
git checkout scripts/build.py

# Revert template changes
git checkout templates/lesson.html.jinja

# Revert import statements in source files
git checkout static/js/
```

Then run tests to verify:
```bash
npm test
uv run pytest
```
