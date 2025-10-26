# Project State

Last Updated: 2025-10-26

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
  - Build tests (syntax validation, code generation)
  - Browser tests with Playwright (9 tests, all passing)
  - Keyboard shortcut test for Cmd/Ctrl+Enter functionality

- **Development Server** (2025-10-26)
  - Background HTTPS server with auto-rebuild on file changes
  - Watches sketchpy/ and templates/ directories
  - Self-signed SSL certificates for Pyodide compatibility

### In Progress

- None currently

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

## Next Steps

1. **Implement gradient support** (High Priority)
   - Add linear and radial gradient methods to Canvas
   - Update autocomplete with gradient examples
   - See plans/gradients.md for specification

2. **Improve autocomplete context awareness**
   - Detect when inside method calls for parameter hints
   - Show relevant palette when typing fill= or color=

3. **Add more example projects**
   - Update instructions panel with varied tutorials
   - Create gallery of example drawings

4. **Performance profiling**
   - Test with complex drawings (many shapes)
   - Optimize SVG generation if needed
