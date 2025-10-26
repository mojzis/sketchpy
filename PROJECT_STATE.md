# Project State

Last Updated: 2025-10-26 (Server Auto-Restart Complete)

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

- **Test Suite** (2025-10-26)
  - Build tests (syntax validation, code generation, 8 tests)
  - Browser tests with Playwright (9 tests)
  - Autocomplete tests (8 tests)
  - Server tests (2 tests): auto-restart and PID management
  - Keyboard shortcut test for Cmd/Ctrl+Enter functionality
  - Total: 27 passing tests

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

1. **Phase 3: Multi-Lesson Switching** (Immediate Priority)
   - Make lesson dropdown functional with Alpine.js
   - Implement dynamic lesson switching without page reload
   - Update editor content and instructions when lesson changes
   - See plans/alpine-phase-3.md for detailed steps

2. **Implement gradient support**
   - Add linear and radial gradient methods to Canvas
   - Update autocomplete with gradient examples
   - See plans/gradients.md for specification

3. **Improve autocomplete context awareness**
   - Detect when inside method calls for parameter hints
   - Show relevant palette when typing fill= or color=

4. **Add more example lessons**
   - Leverage new lesson structure to create varied tutorials
   - Build lesson library (cars, landscapes, patterns, etc.)

5. **Performance profiling**
   - Test with complex drawings (many shapes)
   - Optimize SVG generation if needed
