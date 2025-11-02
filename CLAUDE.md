# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Communication Style

**CRITICAL: Be concise. State what was done, nothing more.**

- Skip evaluation, flattery, praise
- Use minimal words to describe actions
- Example: "Added X to Y" not "Successfully implemented X feature in Y component"

## Environment Activation

**IMPORTANT: Activate the virtual environment before running commands.**

Check if environment is activated:
```bash
which python
```

If output shows `.venv/bin/python`, environment is active. Otherwise, activate it:
```bash
source .venv/bin/activate
```

## Testing Requirements

**CRITICAL: Run tests after every change. Browser tests must pass.**

- Run `pytest` after every code change
- Browser tests are baseline - investigate all failures immediately
- Passing tests before change + failing tests after = regression requiring fix

## Important: Always Start the Server After Changes

After making changes to lesson files, templates, or the shapes.py library, always run:
```bash
srv
```

Just report "Server running at https://localhost:8007/sketchpy/" - no need for verbose output.

## Project Overview

**sketchpy** is an educational Python graphics library for teaching programming through visual art. It provides a simple SVG-based canvas API that works in Jupyter notebooks, marimo, and web browsers via Pyodide. The library emphasizes ease of learning with no "turtle walking" paradigm - just direct shape drawing.

## Architecture

### Core Components

1. **sketchpy/shapes.py** - Main library containing:
   - `Canvas` class: SVG rendering engine with method chaining support
   - `Color` class: Predefined color constants for IDE autocomplete
   - `CarShapes` class: Educational helper shapes (cars, traffic lights, roads)
   - Shape methods: `rect()`, `circle()`, `ellipse()`, `line()`, `polygon()`, `text()`, `rounded_rect()`, `grid()`

2. **templates/lesson.html.jinja** - Browser-based learning environment template:
   - Split-pane UI with instructions and live code editor
   - Pyodide integration for running Python in the browser
   - Interactive tutorials for drawing cars and scenes
   - Jinja2 template that embeds shapes.py code at build time
   - **⚠️ CRITICAL: Contains two script blocks marked "DO NOT MODIFY"** - these handle async module loading timing with Alpine.js. Modifying them causes "appState is not defined" errors.

3. **scripts/** - Development utilities:
   - `srv.py`: HTTPS server with logging support (serves from project root)
   - `build.py`: Generates output/index.html from template + shapes.py

### Design Philosophy

- **No state machine**: Unlike turtle graphics, Canvas doesn't track position/heading. Each shape is independently positioned.
- **Method chaining**: All drawing methods return `self` for fluent API usage
- **Multiple display targets**: Supports marimo (`_repr_html_`) and web via Pyodide
- **Educational focus**: Pre-built shapes (CarShapes) scaffold learning without overwhelming beginners
- **Browser-first**: No IPython/Jupyter dependency; focuses on pure HTML and marimo environments

## Development Commands

### Package Management (uv)

This project uses `uv` for Python dependency management and requires Python 3.14+:

```bash
# Install dependencies (use uv for package management)
uv sync

# Add a dependency (use uv for package management)
uv add <package>

# Activate environment before running commands
source .venv/bin/activate

# Run Python with project dependencies (after activation)
python main.py
```

### Running Tests

The project includes both Python tests (Pytest) and JavaScript tests (Vitest):

**Python Tests:**
```bash
# First time setup: Install Playwright browsers (only needed once, for browser tests)
playwright install chromium

# Run all Python tests EXCEPT browser tests (default, fast ~2s)
pytest

# Run only browser tests (slower, uses real Chromium browser)
pytest -m browser

# Run ALL tests including browser tests
pytest -m ""

# Run tests with verbose output showing test names (when debugging)
pytest -vv

# Run tests with full tracebacks (only when deep debugging needed)
pytest -vv --tb=long

# Run only build tests (fast, no browser)
pytest tests/test_build.py

# Run only server tests
pytest tests/test_server.py

# Run specific test
pytest tests/test_build.py::test_generated_python_syntax

# Run only last failed tests (efficient when fixing failures)
pytest --lf

# Stop after N failures (useful for large test suites)
pytest --maxfail=5
```

**Test Organization:**
- **Fast tests** (default): Build validation, server tests, unit tests (~2s, no browser)
- **Browser tests** (`-m browser`): Playwright E2E tests (~30s, requires Chromium)
- **Why separated**: Browser tests are CPU/memory intensive - skip them during rapid development
- **CI runs both**: GitHub Actions runs full suite including browser tests

**Test Output Philosophy:**
- **Default mode** (configured in `pyproject.toml`): Quiet mode (`-q`) shows only dots and summary
- **Reduces token usage by 10-50x** - what you see in terminal matches what LLMs see
- **Verbose mode** (`-vv` flag): Shows test names and detailed output for debugging
- Configured with `--tb=short` for concise failure tracebacks by default
- Override with `--tb=long` only when actively debugging specific failures
- **Users and AI see the same minimal output** by default, optimizing for efficiency

**JavaScript Tests:**
```bash
# Run JavaScript unit tests (fast, ~400ms, 43 tests)
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage report
npm run test:coverage

# Run linter
npm run lint

# Auto-fix linting issues
npm run lint:fix
```

**JS Test Coverage:**
- **errorHandler.test.js** (26 tests): Error formatting, hints, categorization
- **apiDefinitions.test.js** (10 tests): Palette extraction, Canvas API generation
- **canvasApi.test.js** (7 tests): API presence in generated code
- **domElements.test.js** (10 tests): Template structure validation
- All tests use Vitest + jsdom (no real browser needed)

**Full Test Suite:**
```bash
# Run fast tests only (JS unit + Python non-browser, ~3s total)
npm test && pytest

# Run EVERYTHING including browser tests (~35s total)
npm test && pytest -m ""
```

**Build Tests (`test_build.py`)** - Fast, no browser:
- Build command runs successfully
- Output file is generated
- Generated Python code is syntactically valid
- Required classes (Color, Canvas) are present
- Browser-incompatible code is excluded (save(), Point, CarShapes)
- Required imports are included (typing)
- Unused imports are excluded (dataclasses, enum)
- `_repr_html_()` is present for marimo support
- Generated code size is reasonable (~4KB)

**Browser Tests (`test_browser.py`)** - Requires Chromium (skip by default):
- Page loads in real browser without errors
- Pyodide loads and initializes successfully
- Python code executes without runtime errors
- Canvas renders SVG output correctly
- Keyboard shortcut (Ctrl-Enter) runs code
- Theme switching navigates to new lesson
- Uses Playwright to verify end-to-end functionality
- **9 critical E2E tests** (reduced from 11 to minimize CPU usage)

**Server Tests (`test_server.py`)** - Fast, no browser:
- Server automatically kills existing instance on restart
- PID file is properly created and managed
- Old server process is terminated when new one starts
- New server process starts with different PID
- Server cleanup works correctly

**JavaScript Unit Tests (`tests/js/`)** - Fast, jsdom only:
- **errorHandler.test.js** (26 tests): Error formatting, hints, categorization
- **apiDefinitions.test.js** (10 tests): Palette extraction, Canvas API generation
- **canvasApi.test.js** (7 tests): API presence checks (Canvas, Color classes)
- **domElements.test.js** (10 tests): Template structure (buttons, editor, Alpine.js)
- **Total: 53 unit tests** verifying core JS/template logic
- Run with `npm test` (fast, ~500ms)

### CRITICAL: Alpine.js Initialization Pattern

**⚠️ DO NOT MODIFY the Alpine.js loading pattern in `templates/lesson.html.jinja`**

The template contains two critical script blocks that handle async module loading timing:

1. **Module Import Block** (lines ~17-52):
   - Wraps dynamic import in async IIFE
   - Exposes `window.appState` as a **function** (not direct assignment)
   - Sets `window.appStateReady` flag after import completes
   - Must complete before Alpine.js initializes

2. **Alpine.js Loading Block** (lines ~1262-1279):
   - Polls for `window.appStateReady` flag
   - Only loads Alpine.js after appState is defined
   - Prevents "appState is not defined" errors

**Why this pattern?**
- ES6 modules (`type="module"`) are async and deferred by default
- Dynamic `import()` adds another async layer
- Alpine.js `defer` script can load before modules finish
- Without polling, Alpine tries to call `appState()` before it exists
- This pattern ensures correct initialization order

**If you see "appState is not defined" errors:**
1. Check that both script blocks are intact
2. Verify `window.appState = () => createAppState()` wrapper exists
3. Confirm polling script waits for `appStateReady` flag

### JavaScript Architecture

The web interface uses modular ES6 JavaScript with no bundler (CDN dependencies):

**Core Modules (`static/js/core/`):**
- **lessonState.dev.js** - Alpine.js reactive state management
  - Pyodide worker initialization
  - Code execution handling
  - Error formatting and display
  - Progress tracking (localStorage)
- **editorSetup.dev.js** - CodeMirror 6 editor initialization
  - Python syntax highlighting
  - Smart autocomplete (context-aware)
  - Keyboard shortcuts (Ctrl/Cmd-Enter)
- **apiDefinitions.dev.js** - Dynamic API extraction from shapes.py
  - Builds autocomplete definitions for Canvas methods
  - Extracts Color palette constants
  - Provides working code examples with parameters

**Supporting Files:**
- **errorHandler.dev.js** - Beginner-friendly error messages
- **pyodide-worker.dev.js** - Python execution in Web Worker
- **security/** - Code validation and timeout handling

**Dependencies (CDN):**
- Alpine.js 3.x - Reactive UI framework
- CodeMirror 6 - Code editor
- Pyodide - Python in the browser

**Code Quality:**
- ESLint configured (flat config, ES2021)
- 47 tests total (36 unit + 11 E2E)
- No bundler (browser-native ES modules)

### Building and Running the Web Interface

The web interface is generated from a Jinja2 template that embeds the current shapes.py code.

**Quick Start:**
```bash
# Start the development server (runs in background by default)
srv

# Server starts in background and returns immediately:
# ✓ Server started in background (PID: 12345)
#   Access: https://localhost:8007/sketchpy/
#   Logs: tail -f logs/srv.log
#   Restart: srv (auto-kills existing server)
#   Stop: kill $(cat logs/srv.pid)
```

The `srv` command runs in **background mode by default**, freeing up your terminal:
- Automatically kills any existing server before starting (safe to run multiple times)
- Runs initial build on startup
- Daemonizes automatically (double-fork, detaches from terminal)
- Serves from `output/` directory (accessible at root URL)
- Watches `sketchpy/` and `templates/` directories for changes
- Auto-rebuilds when `.py`, `.html`, or `.jinja` files are modified
- Logs all activity to `logs/srv.log`

**Run in foreground (if needed):**
```bash
srv --foreground
# or
srv -f
```

**Build Process (happens automatically):**
- Auto-discovers all lessons from `themes/` directory (no manual YAML maintenance)
- Extracts lesson metadata (title, description) from `lesson.md` files
- Reads `sketchpy/shapes.py` and removes browser-incompatible code:
  - File I/O methods like `save()`
  - Unused `Point` dataclass (and associated `dataclasses`, `enum` imports)
- Keeps `from typing` import (used for type hints in function signatures)
- Keeps `_repr_html_()` for marimo compatibility
- Removes type hints from function signatures for cleaner browser-side code
- Stops at convenience functions (quick_draw, CarShapes) to keep payload small (~4KB)
- Renders all templates with `BASE_PATH` configuration for deployment flexibility
- Outputs to `output/` directory (ignored by git, regenerate as needed)

**Development Server Features:**
- Auto-generates self-signed SSL certificates (localhost.pem)
- Requires accepting certificate warnings in browser
- Serves on port 8007 from `output/` directory
- Binds to 0.0.0.0 (accessible from localhost and local network)
- Uses HTTPS (required for Pyodide SharedArrayBuffer)
- Logs all requests and rebuilds to `logs/srv.log`
- Writes PID to `logs/srv.pid` for process management
- **Auto-rebuild**: Detects changes in `sketchpy/` and `templates/` with 0.5s debounce

**Manual Build (optional):**
```bash
# Build without starting server
build
```

**Workflow:**
```bash
# Start server (runs in background, builds automatically, watches for changes)
srv

# Terminal is immediately free - server runs in background
# Edit sketchpy/shapes.py or templates/index.html.jinja
# -> Server auto-rebuilds and logs: "📝 Detected change: ..."

# Monitor logs
tail -f logs/srv.log

# Restart server if needed (automatically kills existing server)
srv

# Stop server when done
kill $(cat logs/srv.pid)
```

**Restarting/Stopping the server:**

⚠️ **IMPORTANT: To restart the server, just run `srv` again!** ⚠️

The server **AUTOMATICALLY KILLS ANY EXISTING INSTANCE** before starting.
You do NOT need to manually kill processes first.

```bash
# ✅ CORRECT: Just restart (auto-kills old server)
srv

# ❌ WRONG: Don't manually kill first (unnecessary)
kill $(cat logs/srv.pid) && srv

# Manual stop without restarting (rarely needed)
kill $(cat logs/srv.pid)
```

**THE SERVER IS SELF-RESTARTING. JUST RUN `srv` EVERY TIME.**

### Deployment Configuration

**BASE_PATH Setting:**
The build system uses a configurable `BASE_PATH` for deployment flexibility. This is set in `scripts/build.py`:

```python
# Use '/sketchpy' for GitHub Pages, '' for local development or custom domain
BASE_PATH = '/sketchpy'
```

**Deployment targets:**
- **GitHub Pages** (current): Uses `BASE_PATH = '/sketchpy'` to match the repository name
  - URL: https://mojzis.github.io/sketchpy/
  - All links include the `/sketchpy` prefix
- **Custom domain** (future): Change to `BASE_PATH = ''` for root-level deployment
  - All links work without prefix

**How it works:**
- Build script passes `base_path` to all Jinja2 templates
- Templates use `{{ base_path }}/lessons/...` for links
- JavaScript receives `window.BASE_PATH` for dynamic resource loading
- Worker paths and static assets use the BASE_PATH prefix

**To change deployment:**
1. Edit `BASE_PATH` in `scripts/build.py`
2. Run `build` to regenerate all files
3. Deploy the `output/` directory

### Testing the Library

**In marimo notebooks:**

```python
from sketchpy.shapes import Canvas, Color, CarShapes

# Create and display a canvas
c = Canvas(800, 600)
c.rect(100, 100, 200, 150, fill=Color.BLUE)
c.circle(200, 200, 50, fill=Color.RED)
c  # Auto-displays via _repr_html_()
```

**In the browser (via development server):**

Edit the code directly in the web interface at `https://localhost:8007/sketchpy/` after running `srv`.

## Key Technical Details

### Canvas Coordinate System
- Origin (0,0) is top-left corner
- X increases rightward, Y increases downward
- Matches standard SVG/web conventions

### Display Methods
- `to_svg()`: Returns SVG string
- `save(filename)`: Writes SVG to file (not available in browser/Pyodide)
- `_repr_html_()`: Auto-display in marimo notebooks and compatible environments

### Method Chaining Pattern
All drawing methods return the Canvas instance, enabling:
```python
Canvas(800, 600).rect(...).circle(...).line(...)
```

### Grid Method
The `grid()` method helps visualize coordinates on the canvas:
```python
can = Canvas(800, 600)
can.grid(spacing=50, color="#E8E8E8", show_coords=True)  # Draw subtle grey grid
```
- Default spacing: 50 pixels
- Default color: Very light grey (#E8E8E8)
- Shows coordinate labels every 100 pixels
- Includes origin marker (0,0) at top-left
- Useful for learning coordinate positioning

### Palette Display
The `show_palette()` method displays all colors from a palette class as colored rectangles:
```python
can = Canvas(800, 600)
can.show_palette(CreativeGardenPalette)  # Display all palette colors
can.show_palette(CalmOasisPalette)       # Or use a different palette
can.show_palette(Color)                  # Basic colors
```
- Displays color names and hex values
- Customizable layout (columns, padding, size)
- Useful for exploring available colors
- Available palettes:
  - `CreativeGardenPalette`: 12 pastel colors (PEACH_WHISPER, ROSE_QUARTZ, BUTTER_YELLOW, etc.)
  - `CalmOasisPalette`: 12 calming blues/greens (SKY_BLUE, MINT_FRESH, LAVENDER_MIST, etc.)
  - `Color`: 12 basic colors (RED, BLUE, GREEN, etc.)

### CarShapes Helpers
Pre-built educational shapes demonstrate composition:
- `simple_car()`: Full car from primitives
- `wheel()`: Multi-layered wheel (tire, rim, hub)
- `traffic_light()`: State-based light (red/yellow/green)
- `road()`: Procedural dashed lane markers

## Skills

Active skills loaded in Claude's context. Use when trigger conditions match.

### auto-commit-push

**Auto-trigger after**:
- Feature/bugfix/refactor complete AND tests passing
- Code review changes implemented
- Discrete work unit finished (can be described in single commit message)

**Manual trigger**:
- User says: "commit and push", "commit these changes", "push this"

**Action**:
1. Create atomic commit with descriptive message
2. Push to remote branch
3. Report commit SHA and push status

**Skip when**:
- Tests failing
- Work in progress
- User says "don't commit yet"

### project-documentation-tracker

**Auto-trigger after**:
- Completing implementation phase/milestone
- Making architectural decision (choosing between alternatives)
- Significant refactoring with rationale
- Adding/removing major dependencies

**Manual trigger**:
- User says: "update docs", "document this decision", "update project state"

**Action**:
1. Update PROJECT_STATE.md: Add to Completed, update test counts, note constraints
2. Update DECISIONS.md: New entry with decision/why/rejected/implementation (keep under 150 words)

**Skip when**:
- Minor code changes (typo fixes, formatting)
- Work still in progress
- Documentation already up-to-date

**Format rules**:
- DECISIONS.md: Decision (1 sentence) + Why (1 sentence) + Rejected bullets + Implementation paths
- PROJECT_STATE.md: Feature name + date + brief description
- Aim for 70-85% token reduction vs traditional decision logs## Project Structure Notes

- **main.py**: Placeholder entry point (currently just prints hello message)
- **pyproject.toml**: Defines project metadata, dependencies (marimo, not IPython), and console script entry points (`srv`, `build`, `test`)
- **package.json**: NPM dependencies for JavaScript tooling (ESLint, Vitest, jsdom)
- **templates/**: Jinja2 templates for generating web interface
  - `lesson.html.jinja`: Lesson page template (imports modular JS)
  - `index.html.jinja`: Landing page template
- **output/**: Generated files (gitignored, create via `build`)
- **scripts/**: Python scripts exposed as commands via pyproject.toml
- **sketchpy/**: Core library package (browser-first, marimo-compatible)
- **static/js/**: Modular JavaScript (ES6 modules, no bundler)
  - `core/`: Main application modules (lessonState, editorSetup, apiDefinitions)
  - `errorHandler.js`: Beginner-friendly error formatting
  - `pyodide-worker.js`: Python execution in Web Worker
  - `security/`: Code validation and sandboxing
- **tests/**: Automated tests
  - `test_*.py`: Python tests (pytest + Playwright)
  - `js/*.test.js`: JavaScript unit tests (Vitest)
- **logs/**: Runtime logs and PID files (gitignored, created by srv command)
- **.claude/skills/**: Custom Claude Code skills for workflow automation
- **Dependencies**:
  - Production: marimo, jinja2, watchdog, colabturtleplus
  - Dev (Python): pytest, playwright
  - Dev (JavaScript): eslint, vitest, jsdom
  - Removed: IPython/Jupyter (browser-first approach)
- **sketchpy/** vs **turtles/**: Git history shows migration from turtle-based approach (deleted turtles/) to current SVG approach
