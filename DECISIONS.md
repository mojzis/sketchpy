# Architectural Decisions

## Test Suite Optimization with Browser Marker (2025-11-02)

**Decision**: Separate fast unit tests from slow browser E2E tests using pytest markers; skip browser tests by default

**Why**: Browser tests (Playwright) are CPU/memory intensive on VPS; 90% reduction in local test time enables faster development iteration

**Rejected**:
- Run browser tests always (slows VPS, blocks rapid development)
- Move to JS-based Playwright (same Chromium overhead, minimal benefit)
- Remove browser tests entirely (lose critical E2E validation)
- Separate test commands without markers (inconsistent, easy to forget)
- Run browser tests only in CI (local testing becomes incomplete)

**Implementation**:
- pyproject.toml (browser marker, `-m "not browser"` in addopts)
- tests/test_browser.py (all 9 tests marked `@pytest.mark.browser`)
- tests/js/canvasApi.test.js (7 unit tests for API presence)
- tests/js/domElements.test.js (10 unit tests for template structure)
- .github/workflows/test.yml (3 jobs: JS unit, Python fast, Python browser)
- CLAUDE.md (updated test commands, organization documented)

---

## Math Doodling Theme with Opacity and Global Math Module (2025-10-29)

**Decision**: Create third curriculum theme focused on abstract geometric patterns using overlapping transparent circles; add opacity parameter to circle(); make math module globally available in Pyodide

**Why**: Transparency-based art teaches color mixing through experimentation; mathematical patterns (mandalas, spirals) demonstrate trigonometry visually; global math removes import barrier for students

**Rejected**:
- Require `import math` for lessons (adds friction, confusing error for beginners)
- Opacity via CSS classes (less flexible, harder to teach programmatically)
- Separate gradient methods (opacity more versatile, simpler API)
- Keep functions outside main() in lessons 11-15 (browser extracts only main() body)
- Complex shapes beyond circles (reduces focus on core concept)

**Implementation**:
- themes/theme-3/ (15 lessons: first-overlap → meditative-masterpiece)
- sketchpy/shapes.py (MathDoodlingPalette with 8 triadic colors, circle opacity parameter)
- static/js/pyodide-worker.dev.js (pre-import math, add to allowed modules)
- static/js/core/apiDefinitions.dev.js (extract MathDoodlingPalette, show opacity in autocomplete)
- tests/test_lessons.py (add math and MathDoodlingPalette to test namespace)

---

## Timestamp-Based Cache Busting for JavaScript (2025-10-29)

**Decision**: Use single build timestamp in JS filenames instead of content-based hashing

**Why**: Varnish CDN on GitHub Pages ignores query strings; content hashing creates cascade problem where changing one file requires rewriting imports in dependent files

**Rejected**:
- Query strings (?v=timestamp) - Ignored by Varnish cache
- Content-based hashing (SHA256) - Import cascade hell (changing errorHandler.abc.js breaks lessonState.js imports)
- Manual versioning - Requires remembering to bump version
- No cache busting - Users see stale JS after deployments
- Service workers - Complex, requires maintenance
- ETags only - Not sufficient for aggressive CDN caching

**Implementation**:
- Source files: *.dev.js (unchanged for tests/dev)
- Build output: *.{YYYYMMDDHHMMSS}.js (timestamped)
- scripts/build.py (timestamp generation, file copying with string replacement)
- templates/lesson.html.jinja ({{ build_version }} template variable)
- Cleanup: output/static/js/ removed before each build

---

## Type Checking with ty (2025-10-28)

**Decision**: Add ty static type checker to dev toolchain with type hints for all function signatures

**Why**: Catch type errors early before runtime; improve code maintainability; enable better IDE support

**Rejected**:
- mypy (slower, more configuration needed)
- pyright (requires Node.js, heavier)
- pytype (Google-only focus, limited adoption)
- No type checking (missed Union type issue in gradients)
- Type hints without checker (annotations ignored)
- Runtime type checking with typeguard (performance overhead)

**Implementation**:
- sketchpy/shapes.py (Union types for gradient methods)
- tests/*.py (None checks, proper imports)
- scripts/build.py (improved type hint removal for Union types)
- pyproject.toml (ty dependency, exclusions)

---

## Pygments Syntax Highlighting for Help Content (2025-10-28)

**Decision**: Add Pygments codehilite to Markdown processor for colored Python syntax in help tabs

**Why**: Code examples easier to read with colors; matches editor theme for visual consistency

**Rejected**:
- highlight.js (requires JavaScript, client-side processing)
- Prism.js (requires JavaScript, bundle size)
- Plain code blocks (harder to read, less professional)
- Server-side highlight.js (requires Node, complex setup)
- Manual HTML spans (unmaintainable)

**Implementation**:
- scripts/build.py (codehilite extension config)
- templates/lesson.html.jinja (Dracula theme CSS)

---

## JavaScript Modularization with Unit Testing (2025-10-28)

**Decision**: Restructure JavaScript from monolithic app.js to modular ES6 modules with unit testing

**Why**: Enable fast unit testing (400ms vs 30s E2E); improve maintainability and separation of concerns

**Rejected**:
- Keep monolithic app.js (hard to test, poor separation)
- Webpack bundler (unnecessary complexity for CDN dependencies)
- Jest with jsdom (poor ES module support)
- Mocha/Chai (older API)
- Only E2E tests (too slow for development iteration)
- TypeScript conversion (adds build step, not critical yet)

**Implementation**:
- static/js/core/lessonState.js
- static/js/core/editorSetup.js
- static/js/core/apiDefinitions.js
- static/js/errorHandler.js
- tests/js/errorHandler.test.js (26 tests)
- tests/js/apiDefinitions.test.js (10 tests)
- package.json, vitest.config.js, eslint.config.js

---

## Car Theme for 15-Lesson Curriculum (2025-10-27)

**Decision**: Use car/vehicle theme for lessons 4-15, progressing from simple labeled cars to city traffic scenes

**Why**: Universal appeal, natural complexity progression, modular composition teaches functions well

**Rejected**:
- Mixed themes per lesson (cognitive overhead switching contexts)
- Flower theme for all (repetitive, less modular)
- Abstract patterns (less relatable, no real-world scenarios)
- Game sprites (too complex, less universal)
- House/building theme (too static, harder to teach loops)
- Robot/character theme (complex shapes, no standard design)

**Implementation**:
- lessons/04-strings-and-text through lessons/15-final-project
- 36 files total (12 lessons × 3 files: starter.py, lesson.md, help.md)
- 60 tests passing (15 lessons × 4 test types)

---

## Server-Side Snippet Execution (2025-10-27)

**Decision**: Execute Python snippets during build, embed SVG in landing page

**Why**: Landing page loads instantly (no Pyodide delay); showcases actual library code

**Rejected**:
- Client-side Pyodide execution (5-10s load on landing page)
- JavaScript canvas examples (not real library code)
- Static screenshot images (larger files, less crisp)
- Iframe embedding (complex, still needs Pyodide)
- Single static example (less engaging)

**Implementation**:
- scripts/build.py (execute_snippet, load_snippets)
- templates/index.html.jinja
- snippets/ (sunset_garden.py, calm_waves.py, geometric_harmony.py)
- tests/test_snippets.py (5 tests)

---

## Pyodide Web Worker (2025-10-26)

**Decision**: Move Python execution from main thread to Web Worker (background thread)

**Why**: UI froze during code execution; users couldn't interact while code ran; educational tool needs responsive interface

**Rejected**:
- setTimeout chunking (can't interrupt Pyodide's synchronous execution)
- requestAnimationFrame (same synchronous execution issue)
- Cancel button with page reload (loses user's code and state)
- Modal "Please wait" overlay (doesn't prevent the freezing)
- Warning users about long code (defeats learning purpose)
- SharedArrayBuffer for shared memory (unnecessary complexity)

**Implementation**:
- static/js/pyodide-worker.js
- static/js/app.js (worker communication)
- templates/lesson.html.jinja

---

## Parameterized Tests for Lessons (2025-10-26)

**Decision**: Use pytest's @pytest.mark.parametrize with dynamic file discovery to validate all lesson starter files

**Why**: Scalable - new lessons automatically tested without modifying test code; ensures consistency

**Rejected**:
- Individual test function per lesson (doesn't scale, code duplication)
- Single test with manual loop (no granularity in failures)
- Pytest metaprogramming (more complex, harder to maintain)
- Separate test files per lesson (file explosion)
- JSON/YAML test data (over-engineered)

**Implementation**:
- tests/test_lessons.py (get_lesson_starter_files, 4 parameterized tests)

---

## Automatic Server Restart (2025-10-26)

**Decision**: kill_existing_server() function runs automatically at startup

**Why**: Reduces friction - developers don't need to remember manual kill steps; prevents "Address already in use" errors

**Rejected**:
- Require manual kill before restart (error-prone, easy to forget)
- Use different port per instance (breaks bookmarks, confusing)
- Detect port and auto-choose next available (port changes confusing)
- Process manager like PM2 (external dependency, overkill)
- Check port and fail with error (still requires manual intervention)
- Explicit --force flag (adds cognitive overhead)

**Implementation**:
- scripts/srv.py (kill_existing_server function)
- tests/test_server.py (lifecycle tests)

---

## 2-Column Layout (2025-10-26)

**Decision**: Left sidebar (20%), right area (80%) with vertical split (editor top, canvas bottom)

**Why**: Canvas needs width more than height; 80% better than 40%; collapsible sidebar gives 100% when needed

**Rejected**:
- 3-panel layout (canvas cramped at 40%, lesson list wasteful)
- Horizontal split no sidebar (where do instructions/controls go?)
- Bottom canvas like DevTools (wastes space on wide screens)
- Tabs instead of split (can't see code and output simultaneously)
- Three equal columns (still cramps canvas)

**Implementation**:
- templates/lesson.html.jinja
- templates/components/sidebar.html
- templates/components/output-tabs.html

---

## YAML + Markdown Lessons (2025-10-26)

**Decision**: lessons/ directory with YAML metadata + Markdown files

**Why**: Separation of concerns; Markdown easier than HTML; scalable to many lessons; version control friendly

**Rejected**:
- Hardcoded HTML lessons (not scalable, requires HTML knowledge)
- JSON metadata (less readable, no comments)
- HTML lesson content (verbose, harder to write)
- Single monolithic lessons.json (poor version control)
- Database storage (overkill, not version controllable)
- Python modules (requires Python knowledge for authors)

**Implementation**:
- lessons/{id}/lesson.md, starter.py, help.md
- scripts/build.py (LessonLoader class)

---

## Alpine.js for UI (2025-10-26)

**Decision**: Use Alpine.js v3 for client-side state management and reactive UI

**Why**: Lightweight (~15KB), no build step, perfect for progressive enhancement

**Rejected**:
- React (requires build, ~45KB, overkill)
- Vue.js (~33KB, requires setup)
- Vanilla JavaScript (reinventing reactivity wheel)
- Svelte (requires build/compilation)
- Petite-Vue (smaller community)
- htmx (doesn't provide client-side state management)

**Implementation**:
- templates/lesson.html.jinja (Alpine directives)
- static/js/app.js (appState function)

---

## CodeMirror 6 Keymap Precedence (2025-10-26)

**Decision**: Wrap custom keymaps with Prec.highest() to override default CodeMirror keymaps

**Why**: Default keymaps intercepted Ctrl/Cmd+Enter before custom handler could process it

**Rejected**:
- domEventHandlers for raw events (doesn't have precedence over keymap system)
- Remove conflicting keymaps from basicSetup (fragile, loses defaults)
- Different keyboard shortcut (Cmd/Ctrl+Enter is standard)
- Move function definitions before editor (necessary but insufficient)

**Implementation**:
- templates/lesson.html.jinja (Prec.highest wrapper)
- tests/test_browser.py (keyboard shortcut test)

---

## CodeMirror 6 Migration (2025-10-26)

**Decision**: Migrate from CodeMirror 5 to CodeMirror 6

**Why**: Actively maintained; better autocomplete API; modern ES modules; improved extensibility

**Rejected**:
- Stay on CodeMirror 5 (end of life, limited autocomplete)
- Monaco Editor (3MB bundle, overkill)
- Ace Editor (less active development)

**Implementation**:
- templates/lesson.html.jinja (ES module imports)
- CSS updates (.CodeMirror → .cm-editor)

---

## Browser-First with Pyodide (2025-10-26)

**Decision**: Use Pyodide to run Python in browser; web editor as primary interface

**Why**: Zero installation friction; works on any device; can't break environment; instant feedback

**Rejected**:
- Jupyter/IPython primary (installation barrier too high)
- Local Python REPL (requires installation, turtle outdated)
- Online REPLs like Repl.it (requires account, rate limits)
- Python desktop app (distribution complexity, per-platform builds)

**Implementation**:
- static/js/pyodide-worker.js
- templates/lesson.html.jinja

---

## Playwright Testing (2025-10-26)

**Decision**: Use Playwright with Chromium for browser integration tests

**Why**: Can test real browser interactions; headless for CI; catches issues unit tests can't

**Rejected**:
- Jest with jsdom (can't test Pyodide, no real keyboard events)
- Selenium (older API, slower, more flaky)
- Cypress (not designed for file:// protocol)
- Manual testing only (keyboard shortcut broke without notice)

**Implementation**:
- tests/test_browser.py (9 tests)
- .github/workflows/test.yml (CI integration)

---

## Jinja2 Template Build (2025-10-26)

**Decision**: Build process reads shapes.py, filters browser-incompatible code, embeds in HTML template

**Why**: Single HTML file easy to distribute; build ensures browser compatibility; Python code stays in .py files

**Rejected**:
- Fetch shapes.py at runtime (requires server, CORS issues)
- Python code directly in HTML (loses syntax highlighting, messy diffs)
- Separate JS and Python files (harder to distribute, CORS issues)
- Webpack/rollup bundler (overkill for embedding one file)

**Implementation**:
- scripts/build.py (code filtering)
- templates/index.html.jinja ({{ shapes_code }} placeholder)
