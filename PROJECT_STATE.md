# Project State

Last Updated: 2025-10-27 (Complete Lesson Curriculum)

## Overview

**sketchpy** is an educational Python graphics library for teaching programming through visual art. It provides a simple SVG-based canvas API that works in Jupyter notebooks, marimo, and web browsers via Pyodide. The library emphasizes ease of learning with direct shape drawing (no "turtle walking" paradigm).

Currently in active development with a functional web-based editor powered by CodeMirror 6 and Pyodide.

## Implementation Status

### Completed

- **Core Canvas Library** (2025-10-26)
  - SVG-based rendering engine with method chaining
  - Shape methods: rect, circle, ellipse, line, polygon, text, rounded_rect
  - Grid helper with coordinate labels
  - Palette display functionality
  - Color classes: Color, CreativeGardenPalette, CalmOasisPalette

- **Web Editor Interface** (2025-10-26)
  - CodeMirror 6 editor with Python syntax highlighting
  - Pyodide integration for running Python in browser
  - Live SVG output rendering
  - Custom autocomplete for Canvas API

- **Keyboard Shortcut for Code Execution** (2025-10-26)
  - Cmd+Enter (Mac) / Ctrl+Enter (Windows/Linux) runs code
  - Fixed keymap precedence issue using Prec.highest()
  - Test coverage via Playwright

- **Test Suite** (2025-10-27)
  - Build tests (11 tests): syntax validation, code generation, snippet integration
  - Browser tests with Playwright (9 tests)
  - Autocomplete tests (8 tests)
  - Server tests (2 tests): auto-restart and PID management
  - Keyboard shortcut test for Cmd/Ctrl+Enter functionality
  - Lesson tests (60 tests): validates all 15 lesson starter.py files execute, create canvas, draw shapes, generate valid SVG (4 test types × 15 lessons)
  - Snippet tests (5 tests): validates snippet execution, SVG generation, palette usage
  - Total: 95 tests (78 passing for core: build 11, snippet 5, lesson 60, server 2)

- **Development Server** (2025-10-26)
  - Background HTTPS server with auto-rebuild on file changes
  - Watches sketchpy/ and templates/ directories
  - Self-signed SSL certificates for Pyodide compatibility
  - Automatic server restart: kills existing instance when run again
  - Test coverage for server lifecycle and auto-restart functionality

- **Lesson Content Structure - Phase 0** (2025-10-26)
  - Created lessons/ directory with YAML metadata and Markdown content
  - Added dependencies: pyyaml, markdown
  - Implemented first lesson: "Draw Your First Flower"
  - Structure: lessons.yaml + lesson.md + starter.py + help.md per lesson
  - All 25 tests still passing, no breaking changes to existing system

- **Multi-Lesson Build System - Phase 1** (2025-10-26)
  - Enhanced build.py with LessonLoader class for YAML/Markdown processing
  - Created lesson.html.jinja template with Alpine.js integration
  - Build generates both old (/) and new (/lessons/{id}.html) versions
  - Static file copying (app.js) to output directory
  - Generates lessons.json for client-side use
  - Alpine.js v3 CDN integration for reactive UI foundation
  - All 25 tests passing, old version unchanged

- **2-Column Responsive Layout - Phase 2** (2025-10-26)
  - Redesigned from 3-panel to 2-column layout (left sidebar 20%, right editor/canvas 80%)
  - Left sidebar: lesson dropdown, instructions, run/clear buttons
  - Right area: vertical split (editor top 50%, canvas/output/help tabs bottom 50%)
  - Collapsible sidebar with state persistence (localStorage)
  - Removed top toolbar to maximize canvas space
  - Alpine.js state management for UI interactions
  - Component-based templates (sidebar.html, output-tabs.html)
  - Mobile responsive with fixed sidebar overlay
  - All 8 build tests passing

- **Lesson Starter File Tests** (2025-10-26)
  - Created tests/test_lessons.py with parameterized tests for all lesson starter.py files
  - Tests verify: code execution without errors, canvas creation, shape drawing, SVG generation
  - Fixed bug in lesson 03-geometric-patterns: replaced non-existent OCEAN_DEEP with POWDER_BLUE
  - Automatically discovers new lessons via glob pattern (scalable to future lessons)
  - 12 tests total (4 test types × 3 lessons)

- **Pyodide Web Worker - Phase 4** (2025-10-26)
  - Moved Python execution from main thread to Web Worker for non-blocking UI
  - Created static/js/pyodide-worker.js with Pyodide loading and code execution
  - Updated app.js to communicate with worker via postMessage API
  - Removed direct Pyodide loading from template (now loaded in worker)
  - Auto-run code on page load when worker ready
  - UI stays responsive during Python execution
  - All 8 build tests passing with updated regex for window.SHAPES_CODE
  - Test file path updated to point to lessons/01-first-flower.html (multi-lesson structure)

- **Landing Page with Server-Side Snippet Execution** (2025-10-27)
  - Converted index.html to index.html.jinja template
  - Created snippets/ directory with 3 visual examples using CreativeGardenPalette and CalmOasisPalette
  - Enhanced build.py to execute snippets server-side and capture SVG output
  - Snippets embedded in landing page with rotating display (5-second intervals)
  - Added snippet execution tests (5 tests) and build validation tests (3 tests)
  - Total test count: 49 tests (30 passing for core functionality: build, snippet, lesson, server)
  - Snippets: sunset_garden.py, calm_waves.py, geometric_harmony.py

- **Beginner-Friendly Error Handling System** (2025-10-27)
  - Created errorHandler.js module for transforming Python errors into beginner-friendly messages
  - Integrated error handler with app.js (ES6 module) and pyodide-worker.js
  - Enhanced error extraction to show only user code line numbers (from `<exec>`), not Pyodide internals
  - Smart error message parsing extracts error type from full traceback
  - Category-based error display: Python (orange), Security (blue), Timeout (purple), System (gray)
  - Context-aware hints based on error patterns (e.g., "Define the variable first: xx = ...")
  - Visual error display with line number badge, hint bubble, and code snippet
  - Editor scrolls to error line when error occurs
  - Files: static/js/errorHandler.js, static/js/app.js, static/js/pyodide-worker.js, templates/lesson.html.jinja, templates/components/output-tabs.html

- **Complete 15-Lesson Python Curriculum** (2025-10-27)
  - Created 12 new lessons (lessons 4-15) to complete the curriculum outlined in plans/lessons.md
  - Each lesson includes: starter.py (working code), lesson.md (instructions), help.md (troubleshooting)
  - Car/vehicle theme consistent across all lessons
  - **Level 1 (Foundations)**: Variables, strings, text, booleans, conditionals
  - **Level 2 (Control Flow)**: For loops, lists, nested loops, while loops, compound conditions
  - **Level 3 (Functions)**: Basic functions, parameters, return values, data structures, integration
  - All 60 lesson tests passing (15 lessons × 4 test types)
  - Fixed color compatibility issues (replaced LIGHT_GRAY, DARK_GRAY, SAGE_GREEN with valid colors)
  - Progressive complexity from simple shapes to complete city traffic scenes
  - Final project integrates all concepts: functions, loops, conditionals, lists, dictionaries
  - Directories: lessons/04-strings-and-text through lessons/15-final-project

### In Progress

None currently

### Planned

- Gradient support for shapes (see plans/gradients.md)
- Additional educational helper shapes
- More color palettes
- Enhanced autocomplete with better context awareness
- Performance optimizations for large drawings

## Architecture Decisions

### Browser-First Approach
- **Decision**: Focus on browser environment via Pyodide, not IPython/Jupyter
- **Rationale**: Eliminates installation friction for learners, works on any device with a browser
- **Date**: 2025-10-26

### CodeMirror 6 for Editor
- **Decision**: Use CodeMirror 6 instead of CodeMirror 5
- **Rationale**: Modern ES module architecture, better extensibility, improved autocomplete API
- **Date**: 2025-10-26

### SVG-Based Rendering
- **Decision**: Generate SVG instead of Canvas 2D API
- **Rationale**: SVG is inspectable, scalable, and easier to debug for learners
- **Date**: 2025-10-26

### Method Chaining Pattern
- **Decision**: All drawing methods return self for fluent API
- **Rationale**: Enables concise code like `Canvas(800,600).rect(...).circle(...)`
- **Date**: 2025-10-26

### YAML + Markdown Lesson Structure
- **Decision**: Store lessons as YAML metadata + Markdown files, not hardcoded in HTML
- **Rationale**: Enables multiple lessons, easier content authoring, separation of content from code
- **Date**: 2025-10-26

### Alpine.js for Reactive UI
- **Decision**: Use Alpine.js v3 for client-side interactivity and state management
- **Rationale**: Lightweight (~15KB), simple API, perfect for progressive enhancement, no build step needed
- **Date**: 2025-10-26

### 2-Column Layout with Vertical Canvas/Editor Split
- **Decision**: Use 2-column layout (left sidebar 20%, right 80%) with vertical split on right (editor top, canvas bottom)
- **Rationale**: Maximizes canvas space (80% width), keeps controls accessible in sidebar, better than 3-column which cramped canvas
- **Date**: 2025-10-26

### Pyodide Web Worker for Non-Blocking Execution
- **Decision**: Run Pyodide in a Web Worker instead of main thread
- **Rationale**: Keeps UI responsive during Python code execution, prevents UI freezing on long-running code, better performance on slower devices
- **Date**: 2025-10-26

### Beginner-Friendly Error Messages
- **Decision**: Transform technical Python errors into friendly, actionable messages with context-aware hints
- **Rationale**: Students learning to code need clear explanations, not technical tracebacks; show only user code errors, hide Pyodide internals
- **Date**: 2025-10-27

## Code Patterns

### Jinja2 Template Code Embedding
- **Usage**: Build process embeds processed shapes.py into HTML template
- **Example**: `templates/index.html.jinja` with `{{ shapes_code }}` placeholder
- **Rationale**: Single-file distribution, browser-compatible code, eliminates file I/O and unused classes

### Keymap Precedence with Prec.highest()
- **Usage**: Custom keymaps wrapped with `Prec.highest()` in CodeMirror 6
- **Example**: `Prec.highest(keymap.of([...]))` in templates/index.html.jinja:571
- **Rationale**: Ensures custom shortcuts override default CodeMirror keymaps

### Auto-extracting API for Autocomplete
- **Usage**: JavaScript regex extracts class constants from embedded Python code
- **Example**: Dynamically builds Color/Palette options from shapes_code
- **Rationale**: Single source of truth, autocomplete stays in sync with Python API

### LessonLoader Pattern
- **Usage**: Build-time class that loads and processes lesson content from YAML and Markdown
- **Example**: `LessonLoader` in `scripts/build.py` with `load_lessons_config()` and `load_lesson_content()`
- **Rationale**: Encapsulates lesson loading logic, supports optional help files, converts Markdown to HTML

### Parameterized Lesson Tests
- **Usage**: Pytest's `@pytest.mark.parametrize` with dynamic lesson file discovery
- **Example**: `tests/test_lessons.py` uses `get_lesson_starter_files()` to find all `lessons/*/starter.py` files
- **Rationale**: Automatically scales to new lessons without modifying test code, ensures consistent validation across all lessons

### Web Worker Communication for Pyodide
- **Usage**: Worker handles Pyodide loading and Python execution, main thread stays responsive
- **Example**: `static/js/pyodide-worker.js` receives code via postMessage, executes in Pyodide, sends results back
- **Rationale**: Non-blocking UI prevents freezing during code execution, better UX for long-running code, allows panel toggling during execution

### Server-Side Snippet Execution Pattern
- **Usage**: Build process executes Python snippets and captures SVG output for embedding
- **Example**: `scripts/build.py` has `execute_snippet()` and `load_snippets()` functions that run code in snippets/ directory
- **Rationale**: Pre-rendered SVG avoids Pyodide loading on landing page, showcases library capabilities immediately, enables snippet rotation without runtime execution

### Error Handler Transformation Pattern
- **Usage**: PyodideErrorHandler class transforms technical errors into beginner-friendly messages
- **Example**: Worker extracts error info from `sys.last_type`, filters for `<exec>` frames only, sends to main thread for formatting
- **Rationale**: Separates error extraction (Python/worker) from formatting (JavaScript/main thread); shows only user code line numbers; provides category-based styling hints

### Traceback Parsing for User Code Only
- **Usage**: Filter traceback frames to show only `<exec>` (user code), exclude Pyodide internals
- **Example**: `get_error_info()` in errorHandler.js filters frames where `'<exec>' in f.filename`
- **Rationale**: Beginners don't need internal Python machinery details; showing line 20 (user code) instead of line 573 (Pyodide) is much clearer

## Known Constraints

### Technical

- **Pyodide Loading Time**
  - Impact: 5-10 second initial load for Python runtime
  - Workaround: Loading indicator, auto-run after initialization

- **Browser SharedArrayBuffer Requirement**
  - Impact: Requires HTTPS (even for localhost)
  - Workaround: Development server auto-generates self-signed certificates

- **CodeMirror 6 Keymap Precedence**
  - Impact: Default keymaps can intercept custom shortcuts
  - Workaround: Use Prec.highest() to give custom keymaps priority

### Dependencies

- **Pyodide v0.25.0**
  - Required for browser Python execution
  - Loaded from CDN (jsdelivr)

- **CodeMirror 6**
  - Editor component loaded via ES module imports
  - Requires modern browser with ES module support

- **Python 3.14+**
  - Development environment requirement
  - Uses uv for package management

- **Playwright + Chromium**
  - Browser testing framework
  - One-time install: `uv run playwright install chromium`

- **PyYAML + Markdown**
  - YAML parsing for lesson metadata (lessons.yaml)
  - Markdown conversion for lesson content (lesson.md files)
  - Added in Phase 0 for multi-lesson support

## Next Steps

1. **Implement gradient support** (Next Priority)
   - Add linear and radial gradient methods to Canvas
   - Update autocomplete with gradient examples
   - See plans/gradients.md for specification

2. **Improve autocomplete context awareness**
   - Detect when inside method calls for parameter hints
   - Show relevant palette when typing fill= or color=

3. **Add more example lessons**
   - Leverage new lesson structure to create varied tutorials
   - Build lesson library (cars, landscapes, patterns, etc.)

4. **Performance profiling**
   - Test with complex drawings (many shapes)
   - Optimize SVG generation if needed
