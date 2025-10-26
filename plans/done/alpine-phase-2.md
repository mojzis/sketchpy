# Phase 2: Multi-Panel Alpine UI

**Status**: ✅ Complete

**Prerequisites**: Phase 1 complete

---

## Goal

Implement 3-panel layout with collapsible sidebars, tabbed output, and Alpine-controlled UI state.

---

## What Gets Created

```
templates/components/
├── sidebar.html          # Left sidebar with lesson list
├── output-tabs.html      # Right sidebar with tabs
└── editor-controls.html  # Editor toolbar
static/js/app.js          # Enhanced with full UI state
templates/lesson.html.jinja  # Updated for 3-panel layout
```

---

## Architecture

```
┌──────────┬────────────┬──────────┐
│ Sidebar  │  Editor    │ Output   │
│ (toggle) │            │ Tabs:    │
│ Lessons: │ Instructions│ -Canvas  │
│ • Flower │  (collapse)│ -Output  │
│          │            │ -Help    │
│          │  CodeMirror│          │
└──────────┴────────────┴──────────┘
```

---

## Tasks

### 1. Create `templates/components/sidebar.html`

```html
<div class="lesson-list">
    <h3>Lessons</h3>

    <!-- For now, hardcode single lesson -->
    <!-- Phase 3 will make this dynamic with x-for -->
    <div class="lesson-item active">
        <div class="lesson-link">
            <span class="lesson-icon">1</span>
            <div class="lesson-info">
                <div class="lesson-title">Draw Your First Flower</div>
                <div class="lesson-meta">
                    <span class="difficulty">beginner</span>
                    <span class="duration">15min</span>
                </div>
            </div>
        </div>
    </div>
</div>
```

### 2. Create `templates/components/output-tabs.html`

```html
<div class="output-tabs">
    <button @click="activeTab = 'canvas'"
            :class="{ active: activeTab === 'canvas' }"
            class="tab-btn">
        Canvas
    </button>
    <button @click="activeTab = 'output'"
            :class="{ active: activeTab === 'output' }"
            class="tab-btn">
        Output
    </button>
    <button @click="activeTab = 'help'"
            :class="{ active: activeTab === 'help' }"
            class="tab-btn">
        Help
    </button>
</div>

<div class="output-content">
    <!-- Canvas Tab -->
    <div x-show="activeTab === 'canvas'"
         class="canvas-container"
         id="canvas">
        <div style="color: #999;">Your drawing will appear here. Click "Run Code" ▶</div>
    </div>

    <!-- Output Tab -->
    <div x-show="activeTab === 'output'"
         class="output-text">
        <pre x-text="output || 'No output yet'"></pre>
        <div x-show="error" class="error-message">
            <strong>Error:</strong>
            <pre x-text="error"></pre>
        </div>
    </div>

    <!-- Help Tab -->
    <div x-show="activeTab === 'help'"
         class="help-content">
        {{ lesson.help_html | safe }}
    </div>
</div>
```

### 3. Create `templates/components/editor-controls.html`

```html
<div class="editor-header">
    <button @click="showInstructions = !showInstructions"
            class="btn-secondary">
        <span x-text="showInstructions ? '📖 Hide Instructions' : '📖 Show Instructions'"></span>
    </button>
</div>
```

### 4. Update `static/js/app.js` with Full State

Replace the content with:

```javascript
/**
 * Alpine.js app state for sketchpy learning platform
 */

function appState() {
    return {
        // Panel visibility
        panels: { left: true, right: true },
        showInstructions: true,
        activeTab: 'canvas',

        // Execution state
        isRunning: false,
        output: '',
        error: '',

        // Current lesson
        lesson: window.CURRENT_LESSON || null,

        // Initialization
        init() {
            console.log('Alpine initialized');
            console.log('Current lesson:', this.lesson?.id);
            this.loadPanelState();
            this.initPyodide();
        },

        // Panel Management
        togglePanel(side) {
            this.panels[side] = !this.panels[side];
            localStorage.setItem('panels', JSON.stringify(this.panels));
        },

        loadPanelState() {
            const saved = localStorage.getItem('panels');
            if (saved) {
                try {
                    this.panels = JSON.parse(saved);
                } catch (e) {
                    console.warn('Failed to load panel state:', e);
                }
            }
        },

        // Pyodide initialization (moved from inline script)
        async initPyodide() {
            // Wait for Pyodide to load
            window.pyodide = await loadPyodide();

            // Load shapes library
            await window.pyodide.runPythonAsync(`{{ shapes_code }}`);

            document.getElementById('loading').style.display = 'none';
            document.getElementById('runBtn').disabled = false;
            document.getElementById('status').textContent = 'Ready! ✓';

            console.log('Pyodide ready');
        },

        // Code Execution (moved from window.runCode)
        async runCode() {
            if (this.isRunning) return;

            this.isRunning = true;
            this.output = '';
            this.error = '';
            this.activeTab = 'canvas';

            const code = window.editorView.state.doc.toString();
            const errorDiv = document.getElementById('error');
            const canvasDiv = document.getElementById('canvas');
            const statusSpan = document.getElementById('status');

            errorDiv.style.display = 'none';
            statusSpan.textContent = 'Running...';

            try {
                // Run the code
                await window.pyodide.runPythonAsync(code);

                // Get the canvas result
                const result = window.pyodide.globals.get('can');

                if (result && typeof result.to_svg === 'function') {
                    const svg = result.to_svg();
                    canvasDiv.innerHTML = svg;
                    statusSpan.textContent = 'Success! ✓';
                    statusSpan.style.color = '#4CAF50';
                } else {
                    canvasDiv.innerHTML = '<div style="color: #999;">Make sure your code ends with "can" to display the canvas.</div>';
                    statusSpan.textContent = '';
                }
            } catch (err) {
                this.error = err.message;
                this.activeTab = 'output';
                errorDiv.textContent = '❌ Error: ' + err.message;
                errorDiv.style.display = 'block';
                statusSpan.textContent = 'Error';
                statusSpan.style.color = '#f44336';
                console.error(err);
            } finally {
                this.isRunning = false;
            }
        },

        // Clear Canvas (moved from window.clearCanvas)
        clearCanvas() {
            document.getElementById('canvas').innerHTML = '<div style="color: #999;">Canvas cleared. Click "Run Code" to draw.</div>';
            document.getElementById('error').style.display = 'none';
            this.output = '';
            this.error = '';
        }
    }
}

// Make globally available
window.appState = appState;

// Keep these for backward compatibility with HTML onclick
window.runCode = function() {
    const app = Alpine.$data(document.querySelector('[x-data]'));
    if (app) app.runCode();
};

window.clearCanvas = function() {
    const app = Alpine.$data(document.querySelector('[x-data]'));
    if (app) app.clearCanvas();
};
```

### 5. Update `templates/lesson.html.jinja` for 3-Panel Layout

Replace the `<body>` content with:

```html
<body>
    <div x-data="appState()" class="app-container">

        <!-- Top Toolbar -->
        <div class="toolbar">
            <button @click="togglePanel('left')" class="btn-icon" title="Toggle Lessons">
                📚
            </button>
            <button id="runBtn" @click="runCode()" :disabled="isRunning" class="btn-run">
                <span x-show="!isRunning">▶ Run Code</span>
                <span x-show="isRunning">⏳ Running...</span>
            </button>
            <button @click="clearCanvas()" class="btn-secondary">🗑️ Clear</button>
            <button @click="togglePanel('right')" class="btn-icon" title="Toggle Output">
                📊
            </button>
            <span id="status" style="color: #aaa; margin-left: 10px;"></span>
        </div>

        <div class="error" id="error"></div>

        <!-- Main Content Area (3 panels) -->
        <div class="main-content">

            <!-- Left Sidebar: Lesson Navigation -->
            <aside x-show="panels.left"
                   x-transition
                   class="sidebar sidebar-left">
                {% include 'components/sidebar.html' %}
            </aside>

            <!-- Center: Editor + Instructions -->
            <main class="editor-area">
                <!-- Instructions (collapsible) -->
                <div x-show="showInstructions"
                     x-transition
                     class="instructions-panel">
                    <div class="instructions-header">
                        <h2>{{ lesson.title }}</h2>
                        <button @click="showInstructions = false" class="btn-icon">
                            ✕
                        </button>
                    </div>
                    <div class="instructions-content">
                        {{ lesson.instructions_html | safe }}
                    </div>
                </div>

                <!-- Editor Controls -->
                {% include 'components/editor-controls.html' %}

                <!-- CodeMirror Editor Container -->
                <div class="editor-container">
                    <textarea id="editor" spellcheck="false">{{ lesson.starter_code }}</textarea>
                </div>
            </main>

            <!-- Right Sidebar: Output Tabs -->
            <aside x-show="panels.right"
                   x-transition
                   class="sidebar sidebar-right">
                {% include 'components/output-tabs.html' %}
            </aside>

        </div>
    </div>

    <div class="loading" id="loading">Loading Python... ⏳</div>

    <!-- Keep existing scripts (CodeMirror, Pyodide) -->
    <!-- ... -->

    <!-- Alpine app state (already included from Phase 1) -->
    <script src="/static/js/app.js"></script>

    <!-- Inject lesson data -->
    <script>
        window.CURRENT_LESSON = {{ lesson | tojson }};
        window.ALL_LESSONS = {{ all_lessons | tojson }};
    </script>
</body>
```

### 6. Update CSS for 3-Panel Layout

Add to `<style>` section in template:

```css
/* App Container */
.app-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
}

/* Main Content Grid */
.main-content {
    display: grid;
    grid-template-columns: auto 1fr auto;
    flex: 1;
    overflow: hidden;
}

/* Sidebars */
.sidebar {
    transition: all 0.3s ease;
    overflow-y: auto;
    background: #f5f5f5;
    border-right: 2px solid #ddd;
}

.sidebar-left {
    width: 300px;
    padding: 20px;
}

.sidebar-right {
    width: 400px;
    border-right: none;
    border-left: 2px solid #ddd;
}

/* Editor Area */
.editor-area {
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

/* Instructions Panel */
.instructions-panel {
    background: #fff3cd;
    border-bottom: 2px solid #ffc107;
    max-height: 40vh;
    overflow-y: auto;
}

.instructions-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    background: #ffe69c;
    border-bottom: 1px solid #ffc107;
}

.instructions-header h2 {
    margin: 0;
    font-size: 18px;
}

.instructions-content {
    padding: 20px;
}

/* Editor Controls */
.editor-header {
    padding: 10px 20px;
    background: #2d2d2d;
    border-bottom: 1px solid #444;
}

/* Output Tabs */
.output-tabs {
    display: flex;
    background: #2d2d2d;
    border-bottom: 2px solid #444;
}

.tab-btn {
    flex: 1;
    padding: 10px;
    background: transparent;
    color: #aaa;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
}

.tab-btn:hover {
    background: #3d3d3d;
    color: #fff;
}

.tab-btn.active {
    background: #4CAF50;
    color: white;
}

.output-content {
    flex: 1;
    overflow: auto;
    background: white;
}

.output-content > div {
    padding: 20px;
}

.canvas-container {
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Buttons */
.btn-icon {
    background: transparent;
    border: none;
    font-size: 20px;
    cursor: pointer;
    padding: 5px 10px;
}

.btn-icon:hover {
    background: rgba(255, 255, 255, 0.1);
}

.btn-run {
    background: #4CAF50;
    color: white;
    border: none;
    padding: 8px 20px;
    border-radius: 4px;
    cursor: pointer;
}

.btn-run:disabled {
    background: #666;
    cursor: not-allowed;
}

.btn-secondary {
    background: #666;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
}

.btn-secondary:hover {
    background: #777;
}

/* Responsive */
@media (max-width: 1024px) {
    .sidebar-left {
        width: 250px;
    }
    .sidebar-right {
        width: 350px;
    }
}

@media (max-width: 768px) {
    .main-content {
        grid-template-columns: 1fr;
    }

    .sidebar {
        position: fixed;
        top: 50px;
        bottom: 0;
        z-index: 100;
        box-shadow: 0 0 20px rgba(0,0,0,0.3);
    }

    .sidebar-left {
        left: 0;
    }

    .sidebar-right {
        right: 0;
    }
}
```

---

## Verification Commands

```bash
# 1. Build
uv run build

# 2. Start server
uv run srv -f &
SERVER_PID=$!
sleep 3

# 3. Open browser
# https://localhost:8000/lessons/01-first-flower.html
```

### Manual Browser Testing Checklist

**Layout:**
- [ ] Left sidebar visible by default
- [ ] Right sidebar visible by default
- [ ] Center editor area visible
- [ ] Instructions panel visible at top of editor area

**Panel Toggles:**
- [ ] Click 📚 - left sidebar hides/shows smoothly
- [ ] Click 📊 - right sidebar hides/shows smoothly
- [ ] Panel state persists after reload
- [ ] Transitions are smooth (0.3s ease)

**Instructions:**
- [ ] Instructions visible by default
- [ ] Click ✕ - instructions collapse
- [ ] Click "Show Instructions" - instructions expand
- [ ] Content scrolls if too tall

**Output Tabs:**
- [ ] Three tabs visible: Canvas, Output, Help
- [ ] Canvas tab active by default
- [ ] Click Output tab - switches to output view
- [ ] Click Help tab - switches to help view
- [ ] Active tab highlighted in green
- [ ] Tab content switches correctly

**Code Execution:**
- [ ] Click "Run Code" - code executes
- [ ] Automatically switches to Canvas tab
- [ ] SVG displays in canvas area
- [ ] Status shows "Success! ✓"
- [ ] Button disabled during execution
- [ ] Button shows "Running..." with ⏳ icon

**Error Handling:**
- [ ] Type invalid Python code
- [ ] Click "Run Code"
- [ ] Automatically switches to Output tab
- [ ] Error message displays
- [ ] Error banner appears at top

**Clear Function:**
- [ ] Click "Clear" button
- [ ] Canvas clears
- [ ] Error messages clear
- [ ] Status resets

**Keyboard Shortcuts:**
- [ ] Cmd/Ctrl+Enter runs code

**Console Checks:**
```javascript
// Get Alpine state
let app = Alpine.$data(document.querySelector('[x-data]'))

// Test reactivity
app.panels.left = false  // Left sidebar should hide
app.activeTab = 'help'   // Should switch to help tab
app.showInstructions = false  // Instructions should hide

// Check localStorage
localStorage.getItem('panels')  // Should show saved state
```

**Responsive Testing:**
- [ ] Open DevTools device toolbar
- [ ] Test at 375px (mobile)
- [ ] Test at 768px (tablet)
- [ ] Test at 1024px (laptop)
- [ ] Test at 1920px (desktop)
- [ ] Sidebars adapt appropriately

```bash
# 4. Stop server
kill $SERVER_PID

# 5. Run tests
uv run pytest -v

# 6. Check for console errors (should be none)
```

---

## Checklist

- [ ] Component templates created (sidebar, output-tabs, editor-controls)
- [ ] `app.js` enhanced with full UI state
- [ ] Template updated for 3-panel layout
- [ ] CSS added for layout and transitions
- [ ] Left sidebar toggles correctly
- [ ] Right sidebar toggles correctly
- [ ] Instructions collapse/expand
- [ ] Output tabs switch correctly
- [ ] Code execution through Alpine works
- [ ] Clear function works
- [ ] Panel state persists (localStorage)
- [ ] Responsive layout works
- [ ] No console errors
- [ ] All tests pass

---

## Expected Outcome

- ✅ Fully interactive 3-panel layout
- ✅ All panels collapse/expand smoothly
- ✅ Alpine controls all UI state
- ✅ Output tabs functional
- ✅ Code execution works via Alpine methods
- ✅ Responsive on mobile
- ✅ Panel state persists

---

## Troubleshooting

**Panels not toggling:**
- Check `x-show="panels.left"` attribute present
- Verify Alpine initialized (`Alpine.version` in console)
- Check `togglePanel()` method in app.js

**Tabs not switching:**
- Check `x-show="activeTab === 'canvas'"` attributes
- Verify `@click="activeTab = 'canvas'"` on buttons
- Check `activeTab` in Alpine state

**Transitions not smooth:**
- Verify `x-transition` directive present
- Check CSS has `transition: all 0.3s ease`

**Code not running:**
- Check `runCode()` moved to Alpine state
- Verify `@click="runCode()"` on button
- Check browser console for errors

---

## Rollback

```bash
git checkout HEAD -- templates/ static/ tests/
```

---

## Document and Commit
once the user confirms the manual testing
use the skills for documenting the changes and commiting them

```bash
git add templates/ static/ tests/
git commit -m "Phase 2: Implement 3-panel Alpine UI with collapsible panels"
```

---

## Next Steps

When this phase is complete, proceed to:
**[Phase 3 - Multi-Lesson Support](./alpine-phase-3.md)**
