# Project State

Last Updated: 2025-10-28

## Overview

Educational Python graphics library for teaching programming through visual art. SVG-based Canvas API works in marimo and browsers via Pyodide.

## Completed

- **JavaScript Modularization** (2025-10-28) - Modular ES6 structure with unit testing (36 tests, Vitest, ESLint)
- **15-Lesson Curriculum** (2025-10-27) - Complete Python course (variables to functions, car theme)
- **Error Handling System** (2025-10-27) - Beginner-friendly errors with context-aware hints
- **Landing Page Snippets** (2025-10-27) - Server-side execution shows library capabilities
- **Pyodide Web Worker** (2025-10-26) - Non-blocking UI during code execution
- **2-Column Layout** (2025-10-26) - Canvas gets 80% width, collapsible sidebar
- **Multi-Lesson System** (2025-10-26) - YAML + Markdown content structure with Alpine.js UI
- **Development Server** (2025-10-26) - Background HTTPS with auto-rebuild, auto-restart
- **CodeMirror 6 Migration** (2025-10-26) - Modern editor with improved autocomplete
- **Core Canvas Library** (2025-10-26) - SVG rendering with shapes, grids, palettes, method chaining

## Test Coverage

- Total: 125 tests (114 passing)
- JavaScript unit: 36 tests (errorHandler 26, apiDefinitions 10)
- Python: 78 tests (build 11, lesson 60, snippet 5, server 2)
- Browser E2E: 11 tests (Playwright, currently skipped)

## Known Constraints

- **Pyodide load time**: 5-10s initial load
- **HTTPS required**: Self-signed certs for localhost
- **CodeMirror keymaps**: Use Prec.highest() for custom shortcuts
