# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**sketchpy** is an educational Python graphics library for teaching programming through visual art. It provides a simple SVG-based canvas API that works in Jupyter notebooks, marimo, and web browsers via Pyodide. The library emphasizes ease of learning with no "turtle walking" paradigm - just direct shape drawing.

## Architecture

### Core Components

1. **sketchpy/shapes.py** - Main library containing:
   - `Canvas` class: SVG rendering engine with method chaining support
   - `Color` class: Predefined color constants for IDE autocomplete
   - `CarShapes` class: Educational helper shapes (cars, traffic lights, roads)
   - Shape methods: `rect()`, `circle()`, `ellipse()`, `line()`, `polygon()`, `text()`, `rounded_rect()`, `grid()`

2. **templates/index.html.jinja** - Browser-based learning environment template:
   - Split-pane UI with instructions and live code editor
   - Pyodide integration for running Python in the browser
   - Interactive tutorials for drawing cars and scenes
   - Jinja2 template that embeds shapes.py code at build time

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
# Install dependencies
uv sync

# Add a dependency
uv add <package>

# Run Python with project dependencies
uv run python main.py
```

### Running Tests

The project includes automated tests to verify the build process and generated code:

```bash
# First time setup: Install Playwright browsers (only needed once)
uv run playwright install chromium

# Run all tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run only build tests (fast, no browser)
uv run pytest tests/test_build.py

# Run only browser tests (slower, uses real browser)
uv run pytest tests/test_browser.py

# Run specific test
uv run pytest tests/test_build.py::test_generated_python_syntax
```

**Build Tests (`test_build.py`):**
- Build command runs successfully
- Output file is generated
- Generated Python code is syntactically valid
- Required classes (Color, Canvas) are present
- Browser-incompatible code is excluded (save(), Point, CarShapes)
- Required imports are included (typing)
- Unused imports are excluded (dataclasses, enum)
- `_repr_html_()` is present for marimo support
- Generated code size is reasonable (~4KB)

**Browser Tests (`test_browser.py`):**
- Page loads in real browser without errors
- Pyodide loads and initializes successfully
- Embedded Python code executes without runtime errors
- Canvas renders SVG output correctly
- Color class is available and functional
- Canvas class is available and creates valid SVG

These tests use Playwright to load the generated HTML in Chromium and verify it works end-to-end.

### Building and Running the Web Interface

The web interface is generated from a Jinja2 template that embeds the current shapes.py code.

**Quick Start:**
```bash
# Start the development server (runs in background by default)
uv run srv

# Server starts in background and returns immediately:
# ✓ Server started in background (PID: 12345)
#   Access: https://localhost:8000/
#   Logs: tail -f logs/srv.log
#   Stop: kill $(cat logs/srv.pid)
```

The `srv` command runs in **background mode by default**, freeing up your terminal:
- Runs initial build on startup
- Daemonizes automatically (double-fork, detaches from terminal)
- Serves from `output/` directory (accessible at root URL)
- Watches `sketchpy/` and `templates/` directories for changes
- Auto-rebuilds when `.py`, `.html`, or `.jinja` files are modified
- Logs all activity to `logs/srv.log`

**Run in foreground (if needed):**
```bash
uv run srv --foreground
# or
uv run srv -f
```

**Build Process (happens automatically):**
- Reads `sketchpy/shapes.py` and removes browser-incompatible code:
  - File I/O methods like `save()`
  - Unused `Point` dataclass (and associated `dataclasses`, `enum` imports)
- Keeps `from typing` import (used for type hints in function signatures)
- Keeps `_repr_html_()` for marimo compatibility
- Removes type hints from function signatures for cleaner browser-side code
- Stops at convenience functions (quick_draw, CarShapes) to keep payload small (~4KB)
- Renders `templates/index.html.jinja` with the processed code
- Outputs to `output/index.html` (ignored by git, regenerate as needed)

**Development Server Features:**
- Auto-generates self-signed SSL certificates (localhost.pem)
- Requires accepting certificate warnings in browser
- Serves on port 8000 from `output/` directory
- Binds to 0.0.0.0 (accessible from localhost and local network)
- Uses HTTPS (required for Pyodide SharedArrayBuffer)
- Logs all requests and rebuilds to `logs/srv.log`
- Writes PID to `logs/srv.pid` for process management
- **Auto-rebuild**: Detects changes in `sketchpy/` and `templates/` with 0.5s debounce

**Manual Build (optional):**
```bash
# Build without starting server
uv run build
```

**Workflow:**
```bash
# Start server (runs in background, builds automatically, watches for changes)
uv run srv

# Terminal is immediately free - server runs in background
# Edit sketchpy/shapes.py or templates/index.html.jinja
# -> Server auto-rebuilds and logs: "📝 Detected change: ..."

# Monitor logs
tail -f logs/srv.log

# Stop server when done
kill $(cat logs/srv.pid)
```

**Stopping the server:**
```bash
# Using PID file (recommended)
kill $(cat logs/srv.pid)

# Or find and kill manually
ps aux | grep srv
kill <PID>
```

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

Edit the code directly in the web interface at `https://localhost:8000/` after running `uv run srv`.

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

## Claude Code Skills

This project includes custom skills that automate common development workflows.

### Auto-Commit-Push Skill

**Location**: `.claude/skills/auto-commit-push/`

**Purpose**: Automatically creates concise commits and pushes to remote after completing meaningful chunks of work.

**When Claude Uses This**:
Claude will automatically invoke this skill when you:
- Complete a feature or sub-feature
- Fix a bug
- Finish a refactoring
- Get tests passing
- Complete any logical unit of work

**What It Does**:
1. Reviews changes via `git status` and `git diff`
2. Analyzes recent commits to match the project's commit message style
3. Creates a concise, descriptive commit message
4. Stages relevant files
5. Commits with the generated message
6. Pushes to the remote repository

**Manual Invocation**:
You can also explicitly ask: "commit and push these changes" or "create a commit for this work"

**Safety Features**:
- Won't commit if there are no changes
- Won't push if not on a trackable branch
- Respects `.gitignore` patterns
- Shows confirmation of what was committed

## Project Structure Notes

- **main.py**: Placeholder entry point (currently just prints hello message)
- **pyproject.toml**: Defines project metadata, dependencies (marimo, not IPython), and console script entry points (`srv`, `build`, `test`)
- **templates/**: Jinja2 templates for generating web interface
- **output/**: Generated files (gitignored, create via `uv run build`)
- **scripts/**: Python scripts exposed as commands via pyproject.toml
- **sketchpy/**: Core library package (browser-first, marimo-compatible)
- **tests/**: Automated tests using pytest (verify build process, code generation)
- **logs/**: Runtime logs and PID files (gitignored, created by srv command)
- **.claude/skills/**: Custom Claude Code skills for workflow automation
- **Dependencies**:
  - Production: marimo, jinja2, watchdog, colabturtleplus
  - Dev: pytest (unit tests), playwright (browser tests)
  - Removed: IPython/Jupyter (browser-first approach)
- **sketchpy/** vs **turtles/**: Git history shows migration from turtle-based approach (deleted turtles/) to current SVG approach
