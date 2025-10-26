# Phase 4: Pyodide Web Worker (Optional Performance)

**Status**: ⬜ Not Started

**Prerequisites**: Phase 3 complete

**Note**: This phase is optional. It provides performance improvements but Phase 3 is already fully functional.

---

## Goal

Move Python execution to background thread for non-blocking UI and better responsiveness.

---

## Benefits

- UI stays responsive during code execution
- Main thread not blocked
- Better performance on slower devices
- Buttons/panels remain interactive during Python execution
- No UI freezing on long-running code

---

## What Gets Created

```
static/js/pyodide-worker.js  # New Web Worker
static/js/app.js              # Updated for worker communication
templates/lesson.html.jinja   # Updated Pyodide loading
```

---

## Architecture

```
Before (Current):
┌─────────────────────────┐
│ Main Thread             │
│  - UI (Alpine.js)       │
│  - CodeMirror           │
│  - Pyodide ← BLOCKS UI  │
└─────────────────────────┘

After (Worker):
┌─────────────────────────┐
│ Main Thread             │
│  - UI (Alpine.js)       │
│  - CodeMirror           │
│  - Message to Worker    │
└──────────┬──────────────┘
           │
           ↓ postMessage
┌──────────┴──────────────┐
│ Web Worker              │
│  - Pyodide              │
│  - Python execution     │
│  - Message back results │
└─────────────────────────┘
```

---

## Tasks

### 1. Create `static/js/pyodide-worker.js`

```javascript
/**
 * Web Worker for running Python code with Pyodide
 * Keeps UI thread responsive during code execution
 */

importScripts('https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js');

let pyodide = null;
let shapesCode = null;

// Initialize Pyodide
async function loadPyodideAndPackages() {
    console.log('[Worker] Loading Pyodide...');
    pyodide = await loadPyodide();
    console.log('[Worker] Pyodide loaded');

    // Load shapes library if available
    if (shapesCode) {
        await pyodide.runPythonAsync(shapesCode);
        console.log('[Worker] Shapes library loaded');
    }

    self.postMessage({ type: 'ready' });
}

// Handle messages from main thread
self.onmessage = async (event) => {
    const { type, code, shapes } = event.data;

    // Initialize Pyodide if needed
    if (!pyodide) {
        if (shapes) {
            shapesCode = shapes;
        }
        await loadPyodideAndPackages();
    }

    if (type === 'init') {
        // Already initialized above
        return;
    }

    if (type === 'run') {
        try {
            // Capture stdout
            let output = '';
            pyodide.setStdout({
                batched: (msg) => {
                    output += msg + '\n';
                }
            });

            // Run the code
            await pyodide.runPythonAsync(code);

            // Get canvas result
            const can = pyodide.globals.get('can');
            const svg = can && typeof can.to_svg === 'function' ? can.to_svg() : null;

            self.postMessage({
                type: 'result',
                output: output,
                svg: svg,
                error: null
            });
        } catch (error) {
            self.postMessage({
                type: 'result',
                output: '',
                svg: null,
                error: error.message
            });
        }
    }
};

// Start loading immediately
loadPyodideAndPackages();
```

### 2. Update `static/js/app.js` for Worker Communication

Replace the Pyodide initialization and runCode sections:

```javascript
function appState() {
    return {
        // ... existing state ...

        pyodideWorker: null,
        pyodideReady: false,

        // Initialization
        init() {
            console.log('Alpine initialized');
            console.log('Current lesson:', this.lesson?.id);
            this.loadPanelState();
            this.initPyodideWorker();  // Changed from initPyodide
        },

        // Initialize Pyodide Worker
        initPyodideWorker() {
            console.log('Initializing Pyodide worker...');

            this.pyodideWorker = new Worker('/static/js/pyodide-worker.js');

            this.pyodideWorker.onmessage = (event) => {
                this.handleWorkerMessage(event);
            };

            this.pyodideWorker.onerror = (error) => {
                console.error('Worker error:', error);
                this.error = 'Worker initialization failed: ' + error.message;
            };

            // Send shapes code to worker
            // Note: shapes_code is injected via template
            this.pyodideWorker.postMessage({
                type: 'init',
                shapes: window.SHAPES_CODE
            });
        },

        // Handle messages from worker
        handleWorkerMessage(event) {
            const { type, output, svg, error } = event.data;

            if (type === 'ready') {
                console.log('Pyodide worker ready!');
                this.pyodideReady = true;
                document.getElementById('loading').style.display = 'none';
                document.getElementById('runBtn').disabled = false;
                document.getElementById('status').textContent = 'Ready! ✓';
            } else if (type === 'result') {
                this.isRunning = false;

                const canvasDiv = document.getElementById('canvas');
                const errorDiv = document.getElementById('error');
                const statusSpan = document.getElementById('status');

                if (error) {
                    // Error occurred
                    this.error = error;
                    this.activeTab = 'output';
                    errorDiv.textContent = '❌ Error: ' + error;
                    errorDiv.style.display = 'block';
                    statusSpan.textContent = 'Error';
                    statusSpan.style.color = '#f44336';
                } else if (svg) {
                    // Success - got SVG
                    canvasDiv.innerHTML = svg;
                    this.activeTab = 'canvas';
                    statusSpan.textContent = 'Success! ✓';
                    statusSpan.style.color = '#4CAF50';
                    this.markComplete(this.currentLessonId);
                } else {
                    // No SVG returned
                    canvasDiv.innerHTML = '<div style="color: #999;">Make sure your code ends with "can" to display the canvas.</div>';
                    statusSpan.textContent = '';
                }

                // Store output
                this.output = output || '';
            }
        },

        // Run code (updated to use worker)
        async runCode() {
            if (this.isRunning || !this.pyodideReady) return;

            this.isRunning = true;
            this.output = '';
            this.error = '';
            this.activeTab = 'canvas';

            const code = window.editorView.state.doc.toString();
            const errorDiv = document.getElementById('error');
            const statusSpan = document.getElementById('status');

            errorDiv.style.display = 'none';
            statusSpan.textContent = 'Running...';

            // Send code to worker
            this.pyodideWorker.postMessage({
                type: 'run',
                code: code
            });
        },

        // ... rest of existing methods ...
    }
}
```

### 3. Update `templates/lesson.html.jinja`

Remove direct Pyodide loading and move initialization to worker:

**Remove these lines** (around line 284):
```html
<!-- OLD - Remove this -->
<script src="https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js"></script>
```

**Update the inline script** that initializes Pyodide:

Find the CodeMirror initialization script and remove the `initPyodide()` function and its call. The worker will handle this now.

**Add shapes code injection** in the data injection script:

```html
<!-- Inject lesson data and shapes code -->
<script>
    window.CURRENT_LESSON = {{ lesson | tojson }};
    window.ALL_LESSONS = {{ all_lessons | tojson }};
    window.SHAPES_CODE = `{{ shapes_code }}`;  // Add this line
</script>
```

**Update initial state** of Run button:

```html
<!-- Remove: document.getElementById('runBtn').disabled = true; -->
<!-- Worker will enable it when ready -->
```

### 4. Update Build to Handle Worker Path

Ensure `scripts/build.py` copies static files:

```python
# In main() or build_lessons(), after generating HTML:

# Copy static files to output
static_src = project_root / 'static'
static_dst = output_dir / 'static'
if static_src.exists():
    import shutil
    shutil.copytree(static_src, static_dst, dirs_exist_ok=True)
    logger.info(f"  → static/ files copied")
```

---

## Verification Commands

```bash
# 1. Build
uv run build

# 2. Verify worker file exists
ls -la output/static/js/pyodide-worker.js

# 3. Start server
uv run srv -f &
SERVER_PID=$!
sleep 3

# 4. Open browser
# https://localhost:8000/lessons/01-first-flower.html
```

### Manual Browser Testing

**Worker Initialization:**
- [ ] Open browser console
- [ ] Should see: "[Worker] Loading Pyodide..."
- [ ] Should see: "[Worker] Pyodide loaded"
- [ ] Should see: "[Worker] Shapes library loaded"
- [ ] Should see: "Pyodide worker ready!"
- [ ] Loading spinner disappears
- [ ] Run button enabled

**Code Execution:**
- [ ] Click "Run Code"
- [ ] UI remains responsive (can click other buttons)
- [ ] Can toggle panels during execution
- [ ] Canvas displays SVG after execution
- [ ] Status shows "Success! ✓"

**Error Handling:**
- [ ] Type invalid Python: `print(`
- [ ] Click "Run Code"
- [ ] Error displays correctly
- [ ] UI never freezes

**Long-Running Code Test:**

Add a test with a loop to verify non-blocking:

```python
can = Canvas(800, 600)

# Draw many circles (simulates long-running code)
for i in range(1000):
    x = (i * 7) % 800
    y = (i * 11) % 600
    can.circle(x, y, 5, fill=Color.BLUE)

can
```

- [ ] Click "Run Code"
- [ ] During execution, try to:
  - [ ] Toggle left panel - should work
  - [ ] Toggle right panel - should work
  - [ ] Switch tabs - should work
  - [ ] Type in editor - should work (but don't run)
- [ ] After ~2-3 seconds, circles appear

**Worker in DevTools:**
```javascript
// Browser console checks

// Verify worker exists
console.log(Alpine.$data(document.querySelector('[x-data]')).pyodideWorker)
// Should show Worker object

// Check ready state
console.log(Alpine.$data(document.querySelector('[x-data]')).pyodideReady)
// Should be true
```

**Performance Comparison:**

Open DevTools > Performance tab:
- [ ] Click record
- [ ] Run code
- [ ] Stop recording
- [ ] Check timeline - main thread should be mostly green (idle)
- [ ] Verify no long yellow blocks (JS execution)

**Test All Lessons:**
```bash
# Each lesson should work with worker
# Manually test: open each lesson, run code, verify output
```

```bash
# Stop server
kill $SERVER_PID

# Run automated tests
uv run pytest -v
```

---

## Checklist

- [ ] `pyodide-worker.js` created
- [ ] `app.js` updated for worker communication
- [ ] Template updated (removed direct Pyodide load)
- [ ] Shapes code injected to window
- [ ] Build copies worker to output
- [ ] Worker initializes successfully
- [ ] Console shows worker messages
- [ ] Code executes in worker
- [ ] UI stays responsive during execution
- [ ] Canvas renders correctly from worker
- [ ] Errors display correctly
- [ ] Long-running code doesn't freeze UI
- [ ] All lessons work with worker
- [ ] Tests pass

---

## Expected Outcome

- ✅ Code execution happens in background thread
- ✅ UI remains fully responsive during execution
- ✅ All functionality identical to Phase 3
- ✅ Better performance on slower devices
- ✅ Main thread not blocked
- ✅ Smooth user experience

---

## Performance Gains

**Before (Main Thread):**
- UI freezes during execution
- Can't interact with panels/buttons
- Browser may show "Page Unresponsive"

**After (Worker):**
- UI always responsive
- Can toggle panels during execution
- Smoother experience
- Better for complex drawings

---

## Troubleshooting

**Worker not loading:**
- Check path: `/static/js/pyodide-worker.js`
- Verify file copied to `output/static/js/`
- Check browser console for 404 errors
- Verify CORS not blocking (should be fine for same-origin)

**Pyodide fails in worker:**
- Check `importScripts()` URL correct
- Verify Pyodide CDN accessible
- Check worker console logs (DevTools > Sources > Workers)

**Shapes code not loading:**
- Verify `window.SHAPES_CODE` defined
- Check template injects: `window.SHAPES_CODE = \`{{ shapes_code }}\``
- Verify no backticks in shapes_code breaking the injection

**Worker doesn't send results:**
- Check `postMessage()` calls in worker
- Verify `onmessage` handler in app.js
- Check browser console for errors

**UI still freezes:**
- Verify code actually running in worker (check console logs)
- Confirm `runCode()` uses `postMessage()` not direct execution
- Check no synchronous operations on main thread

---

## Rollback

```bash
git checkout HEAD -- static/js/pyodide-worker.js static/js/app.js templates/
# System reverts to Phase 3 (direct Pyodide)
```

---

## Commit

```bash
git add static/js/pyodide-worker.js static/js/app.js templates/ tests/
git commit -m "Phase 4: Move Pyodide to Web Worker for better performance"
```

---

## Conclusion

Congratulations! You now have a fully functional multi-lesson Python learning platform with:
- ✅ Alpine.js reactive UI
- ✅ Multi-lesson support
- ✅ Progress tracking
- ✅ 3-panel responsive layout
- ✅ Non-blocking Python execution

The platform is ready for:
- Adding more lessons
- Deploying to static hosting (GitHub Pages, Netlify, etc.)
- Customizing styling and content
- Adding more features (user accounts, challenges, etc.)

---

**All phases complete!** 🎉

Return to [Overview](./alpine-overview.md) to review the full journey.
