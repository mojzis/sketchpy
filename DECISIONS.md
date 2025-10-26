# Architectural and Implementation Decisions

## Decision Log Format
Each decision includes: Context, Decision, Rationale, Trade-offs, Alternatives Considered

---

## Server-Side Snippet Execution for Landing Page (2025-10-27)

**Status**: Accepted

**Context**
The landing page (index.html) needed to showcase the library's capabilities with visual examples. The previous approach used JavaScript canvas drawing with hardcoded examples that didn't use the actual sketchpy library. We wanted to demonstrate real Python code using the CreativeGardenPalette and CalmOasisPalette colors to make the landing page more appealing and showcase the library's visual capabilities.

**Decision**
Implement server-side snippet execution during the build process:
- Create `snippets/` directory with Python files that create visual examples
- Add `execute_snippet()` and `load_snippets()` functions to `build.py`
- Execute snippets during build, capturing both code and SVG output
- Embed snippets in landing page template (index.html.jinja) as JSON
- Use JavaScript to rotate through snippets every 5 seconds
- Convert index.html to index.html.jinja template

Created three example snippets:
- `sunset_garden.py` - Layered landscape with gradient sky and scattered flowers
- `calm_waves.py` - Ocean pattern with wave layers using sine curves
- `geometric_harmony.py` - Concentric squares with corner accents

**Rationale**
- Landing page loads instantly (no Pyodide initialization needed)
- Showcases actual library code, not fake examples
- Demonstrates new color palettes (CreativeGardenPalette, CalmOasisPalette)
- Pre-rendered SVG ensures consistent visual quality
- Snippets can be easily updated by adding new Python files
- Provides interesting, rotating visual examples for visitors
- Build-time execution catches snippet errors early

**Trade-offs**
- **Pros**:
  - No Pyodide loading delay on landing page
  - Shows real Python code from the library
  - Easy to add new snippets (just add .py files to snippets/)
  - Rotating examples keep landing page dynamic
  - Demonstrates advanced color palette usage
  - Snippets tested automatically (tests/test_snippets.py)
  - Clean separation between static landing page and interactive lessons

- **Cons**:
  - Adds complexity to build process
  - Snippets must avoid features not supported by Canvas (e.g., opacity parameter)
  - Build time slightly increased (executes 3 Python files)
  - Landing page HTML size increased with embedded SVG (~73KB total)
  - Snippets can't be interactive (pre-rendered)

**Alternatives Considered**

1. **Load Pyodide on landing page and execute snippets client-side**
   - Why rejected: 5-10 second Pyodide load time on landing page, bad first impression, unnecessary for static examples

2. **Use JavaScript canvas to draw examples (existing approach)**
   - Why rejected: Not using actual library code, doesn't showcase Python API, hardcoded examples, not maintainable

3. **Static screenshot images of example code**
   - Why rejected: Not as crisp as SVG, harder to update, larger file sizes, can't rotate through examples easily

4. **Iframe embedding Pyodide examples from lesson pages**
   - Why rejected: Still requires Pyodide load in iframe, complex iframe communication, over-engineered

5. **Single static example instead of rotating**
   - Why rejected: Less engaging, doesn't showcase variety of what library can do, missed opportunity to show multiple palettes

6. **Execute snippets in browser using Web Worker**
   - Why rejected: Still requires Pyodide load on landing page, defeats purpose of fast loading

**Related Decisions**
- CreativeGardenPalette and CalmOasisPalette color classes (provides the colors used in snippets)
- Jinja2 template build system (enables snippet embedding)
- Browser-first approach with Pyodide (used in lessons, avoided on landing page)

**Implementation Details**
- Snippet execution: `scripts/build.py` lines 84-149
- Test coverage: `tests/test_snippets.py` (5 tests), `tests/test_build.py` (3 new tests)
- Template updates: `templates/index.html.jinja` (converted from .html)
- Total passing tests: 30 core tests (build 11, snippet 5, lesson 12, server 2)

---

## Pyodide Web Worker for Non-Blocking Execution (2025-10-26)

**Status**: Accepted

**Context**
After implementing the Alpine.js-based UI with Pyodide running directly in the main thread, user testing revealed that running Python code would freeze the UI during execution. Users couldn't toggle panels, click buttons, or interact with the interface while code was running. For educational purposes, this is problematic - students may want to check instructions or adjust the canvas size while long-running code executes. Additionally, complex drawings with many shapes could take several seconds, creating a poor user experience.

**Decision**
Move Pyodide execution to a Web Worker running in a background thread. Created `static/js/pyodide-worker.js` that:
- Loads Pyodide in the worker thread
- Receives Python code from main thread via `postMessage`
- Executes code and captures output/SVG
- Sends results back to main thread via `postMessage`

Updated `app.js` to:
- Initialize worker instead of loading Pyodide directly
- Communicate with worker using message passing
- Handle async results from worker
- Auto-run code when worker is ready

**Rationale**
- Main thread stays responsive during Python execution
- Users can interact with UI (toggle panels, switch tabs) while code runs
- Better performance perception - UI never freezes
- Follows web best practices for CPU-intensive operations
- Prevents "Page Unresponsive" warnings on slower devices
- Enables future enhancements like progress reporting or cancellation

**Trade-offs**
- **Pros**:
  - UI always responsive (can toggle panels, click buttons during execution)
  - No UI freezing on long-running code
  - Better user experience overall
  - Follows modern web architecture patterns
  - Pyodide loading doesn't block main thread
  - Can add progress indicators or cancellation in future
  - Smoother experience on slower devices

- **Cons**:
  - Additional complexity (worker file, message passing protocol)
  - Slightly harder to debug (worker console separate from main)
  - Cannot directly access DOM from Python code (already wasn't doing this)
  - Small overhead from message serialization (~negligible for our use case)
  - Requires understanding of Web Worker API for future modifications

**Alternatives Considered**

1. **Keep Pyodide on main thread with setTimeout chunking**
   ```javascript
   // Break execution into chunks with setTimeout
   for (let i = 0; i < shapes.length; i++) {
       setTimeout(() => drawShape(shapes[i]), 0);
   }
   ```
   - Why rejected: Doesn't work with Pyodide's synchronous Python execution model, would require rewriting entire execution flow, still blocks during each chunk

2. **Use requestAnimationFrame for yielding**
   - Why rejected: Same issue as setTimeout - can't interrupt Pyodide's synchronous execution without major restructuring

3. **Add "Cancel" button and force-reload page**
   - Why rejected: Loses user's code and state, terrible UX, doesn't solve the freezing problem, nuclear option

4. **Show modal overlay saying "Please wait..." during execution**
   - Why rejected: Doesn't solve the actual problem (UI still frozen), just makes it more obvious

5. **Warn users not to write long-running code**
   - Why rejected: Defeats the purpose of a learning tool, students will experiment with loops/iterations naturally

6. **Use SharedArrayBuffer for shared memory between threads**
   - Why rejected: More complex than needed, requires additional CORS headers, message passing is simpler and sufficient

**Related Decisions**
- Browser-first development with Pyodide (provides the runtime being moved)
- Alpine.js for reactive UI (handles worker messages and updates DOM)
- Auto-run on load (implemented in worker ready handler)

**Implementation Details**
- Worker file: `static/js/pyodide-worker.js` (76 lines)
- Updated files: `static/js/app.js`, `templates/lesson.html.jinja`, `tests/test_build.py`
- Build system automatically copies worker to output directory
- Tests updated to look for `window.SHAPES_CODE` instead of inline Pyodide execution
- Auto-run feature: worker ready handler automatically executes starter code

---

## Parameterized Tests for Lesson Validation (2025-10-26)

**Status**: Accepted

**Context**
The project has multiple lesson directories (`lessons/01-first-flower/`, `lessons/02-colorful-garden/`, etc.), each containing a `starter.py` file with Python code that students will run. These starter files need to be validated to ensure they execute without errors, create a Canvas, draw shapes, and generate valid SVG. As more lessons are added, manually writing separate test functions for each lesson would become unmaintainable and error-prone.

**Decision**
Use pytest's `@pytest.mark.parametrize` decorator with dynamic file discovery to create parameterized tests that automatically validate all lesson starter files. Implemented in `tests/test_lessons.py`:
- `get_lesson_starter_files()` function uses glob to find all `lessons/*/starter.py` files
- Four test functions (execution, canvas creation, shape drawing, SVG validation) each parameterized with all discovered lessons
- Tests execute starter code in isolated namespace with required imports (Canvas, Color, palettes)

**Rationale**
- Scalability: New lessons automatically included without modifying test code
- Consistency: All lessons validated against same quality standards
- Maintainability: Single source of truth for validation logic
- Clarity: Pytest output shows which specific lesson failed (e.g., `test_lesson_starter_executes[starter_file2]`)
- Early detection: Tests caught bug in lesson 03 (non-existent `OCEAN_DEEP` color) immediately
- DRY principle: Avoid duplicating test logic for each lesson

**Trade-offs**
- **Pros**:
  - Automatically scales to new lessons (no test updates needed)
  - Clear test failure messages with lesson identification
  - 12 tests (4 types × 3 lessons) with minimal code (~100 lines)
  - Validates all critical aspects: execution, canvas, shapes, SVG
  - Caught real bug immediately on first run
  - Easy to add new validation criteria (just add one parameterized test)

- **Cons**:
  - Slightly harder to debug than named tests (need to map `starter_file2` to lesson ID)
  - All lessons must follow same structure (create `can` variable, import from sketchpy.shapes)
  - Test runs all validations even if one fails (could use `--maxfail=1` to stop early)
  - Glob pattern assumes consistent directory structure

**Alternatives Considered**

1. **Individual test function per lesson**
   ```python
   def test_lesson_01_first_flower():
       # Test lesson 01

   def test_lesson_02_colorful_garden():
       # Test lesson 02
   ```
   - Why rejected: Doesn't scale - need to add new test function for each lesson, lots of code duplication

2. **Single test with manual loop over lessons**
   ```python
   def test_all_lessons():
       for lesson in ['01-first-flower', '02-colorful-garden']:
           # Test each lesson
   ```
   - Why rejected: Single test failure means entire test fails, no granularity in test results, pytest output doesn't show which lesson failed

3. **Pytest test generation via metaprogramming**
   ```python
   for lesson_file in get_lesson_files():
       globals()[f'test_{lesson_file.stem}'] = create_test(lesson_file)
   ```
   - Why rejected: More complex than parameterize, harder to understand, pytest discovery issues, less maintainable

4. **Separate test files per lesson** (`tests/lessons/test_01_first_flower.py`, etc.)
   - Why rejected: File explosion, still requires creating new file for each lesson, harder to ensure consistency

5. **JSON/YAML-driven test data**
   ```python
   @pytest.mark.parametrize("lesson_data", load_lesson_test_data())
   def test_lesson(lesson_data):
       ...
   ```
   - Why rejected: Over-engineered - we don't need lesson-specific test data, just need to run the code

**Related Decisions**
- YAML + Markdown lesson structure (provides the files being tested)
- Lesson content structure (Phase 0)

---

## Automatic Server Restart via kill_existing_server() (2025-10-26)

**Status**: Accepted

**Context**
Development server (`srv.py`) runs in background mode by default (daemonized). When developers needed to restart the server (e.g., after changing server code, or to clear state), they had to manually kill the process using `kill $(cat logs/srv.pid)` before running `uv run srv` again. If they forgot to kill the old server first, they'd get "Address already in use" errors. This workflow was error-prone and added friction to development.

**Decision**
Implemented `kill_existing_server()` function that runs automatically at server startup. The function:
1. Checks if PID file exists
2. Reads PID and verifies process is running
3. Sends SIGTERM for graceful shutdown, waits briefly
4. Force kills with SIGKILL if process still exists
5. Removes stale PID file
6. Logs the restart action

This makes restarting the server as simple as running `uv run srv` again - no manual process management required.

**Rationale**
- Reduces cognitive load: developers don't need to remember manual kill steps
- Prevents "Address already in use" errors from forgetting to kill old server
- Makes restart workflow consistent: same command to start and restart
- Safer than relying on developers to manually manage PIDs
- Handles edge cases (stale PID files, crashed processes, non-existent processes)
- Improves developer experience with clear logging of restart actions

**Trade-offs**
- **Pros**:
  - Simple workflow: `uv run srv` works whether server is running or not
  - Prevents common "port in use" errors
  - Self-healing: cleans up stale PID files automatically
  - Clear logging when existing server is killed
  - Safe implementation with proper error handling
  - Testable behavior (test_server.py verifies it works)

- **Cons**:
  - Could accidentally kill a server you wanted to keep running (but PID file makes this explicit)
  - Adds ~30 lines of code to srv.py
  - Brief delay (0.5s) for graceful shutdown before starting new server

**Alternatives Considered**

1. **Require manual kill before restart**
   - Why rejected: Error-prone, adds friction, easy to forget, results in confusing errors

2. **Use a different port for each server instance**
   - Why rejected: Breaks bookmarks/links, confusing which port is current, doesn't solve the underlying issue

3. **Detect port in use and automatically choose next available port**
   - Why rejected: Same issues as above - port changes are confusing, doesn't match user intent

4. **Use a process manager (PM2, systemd)**
   - Why rejected: Adds external dependency, overkill for development server, less portable across platforms

5. **Check port availability and fail with helpful error message**
   - Why rejected: Still requires manual intervention, doesn't reduce friction, just makes error clearer

6. **Require explicit --force flag to kill existing server**
   - Why rejected: Adds cognitive overhead (need to remember flag), default behavior should be convenient for development

**Related Decisions**
- Background server mode by default (already implemented)
- PID file management for process tracking (already implemented)
- Test coverage for server lifecycle (implemented alongside this change)

---

## 2-Column Layout with Vertical Editor/Canvas Split (2025-10-26)

**Status**: Accepted

**Context**
After implementing Alpine.js foundation (Phase 1), started Phase 2 with a 3-panel layout (left sidebar for lessons, center for editor, right sidebar for canvas/output). User testing revealed the canvas had insufficient space - the lesson list took 20% width, editor 40%, and canvas only 40%. For an educational graphics tool, the canvas needs maximum space to clearly show drawing results.

**Decision**
Redesigned to 2-column layout:
- **Left sidebar (20%)**: Lesson dropdown, instructions (short version), run/clear buttons at bottom
- **Right area (80%)**: Vertical split with editor (top 50%) and canvas/output/help tabs (bottom 50%)
- Removed top toolbar to maximize vertical space
- Made sidebar collapsible (when hidden, canvas gets 100% width)
- Moved all controls from toolbar to sidebar bottom

**Rationale**
- Canvas needs width more than height for typical graphics (800x600, landscape orientation)
- Lesson list with one item wasteful - dropdown is sufficient
- Instructions can be short in sidebar (full help in Help tab)
- Run/Clear buttons logically grouped with lesson controls
- Collapsible sidebar gives full-screen canvas when needed
- 80% width for canvas much better than 40%
- Vertical split works well for code editor (readable) and canvas (can scroll if needed)

**Trade-offs**
- **Pros**:
  - Canvas gets 80% width (or 100% with sidebar collapsed)
  - Clean, focused UI with less clutter
  - Lesson dropdown scales to many lessons
  - Instructions always visible but unobtrusive
  - Mobile-friendly (sidebar becomes overlay)
  - State persists across reloads

- **Cons**:
  - Instructions limited to short version in sidebar (but full Help tab available)
  - Vertical split means less editor height (but CodeMirror scrolls well)
  - Can't see lesson list at a glance (but dropdown works fine)

**Alternatives Considered**

1. **Keep 3-panel layout (left lessons, center editor, right canvas)**
   - Why rejected: Canvas cramped at 40% width, lesson list wasteful with one item, top toolbar takes vertical space

2. **Horizontal split (editor left, canvas right) with no sidebar**
   - Why rejected: Where do instructions go? Where do controls go? No lesson switching UI

3. **Bottom canvas like browser DevTools (instructions/editor top, canvas full-width bottom)**
   - Why rejected: Canvas needs width more than height for typical graphics, wastes space on wide screens

4. **Tabs instead of split (switch between editor and canvas)**
   - Why rejected: Can't see code and output simultaneously - critical for learning

5. **Three equal columns (33% each)**
   - Why rejected: Still cramps canvas, doesn't solve the fundamental space problem

**Related Decisions**
- Alpine.js for reactive UI (Phase 1)
- Component-based templates (sidebar.html, output-tabs.html)
- LocalStorage for state persistence

---

## YAML + Markdown for Lesson Content Structure (2025-10-26)

**Status**: Accepted

**Context**
The web editor had a single hardcoded lesson embedded in the HTML template. To support multiple lessons and enable easier content authoring, needed a scalable way to store and manage lesson content (instructions, starter code, metadata) outside the HTML template.

**Decision**
Create a `lessons/` directory structure with:
- `lessons.yaml` - YAML file with lesson metadata (id, title, description, difficulty, duration)
- `lessons/{lesson-id}/lesson.md` - Markdown file with lesson instructions
- `lessons/{lesson-id}/starter.py` - Python starter code for the lesson
- `lessons/{lesson-id}/help.md` - Optional additional help/troubleshooting content

Add dependencies: `pyyaml` for YAML parsing, `markdown` for Markdown-to-HTML conversion.

**Rationale**
- Separation of concerns: content separate from code and templates
- Easy authoring: Markdown is simpler than HTML for educational content
- Structured metadata: YAML provides clean structure for lesson properties
- Version control friendly: Separate files show clear diffs
- Scalable: Easy to add new lessons without modifying build process
- Future-proof: Can add fields to YAML without breaking existing lessons
- Standard formats: YAML and Markdown are widely understood

**Trade-offs**
- **Pros**:
  - Content authors don't need to edit HTML/templates
  - Markdown is easier to write and read than HTML
  - YAML metadata enables lesson filtering, sorting, selection UI
  - Each lesson is self-contained in its own directory
  - Can version control lessons independently
  - Non-technical educators can author lessons

- **Cons**:
  - Adds build-time processing (YAML parsing, Markdown conversion)
  - Two new dependencies (pyyaml, markdown)
  - More complex directory structure
  - Build process needs to read multiple files per lesson

**Alternatives Considered**

1. **Continue hardcoding lessons in HTML template**
   - Why rejected: Not scalable, requires HTML knowledge, mixing content with code, version control diffs messy

2. **JSON instead of YAML for metadata**
   - Why rejected: Less human-readable, requires quotes everywhere, harder to hand-edit, no comment support

3. **HTML instead of Markdown for lesson content**
   - Why rejected: More verbose, harder to write, requires HTML knowledge, less accessible to educators

4. **Single monolithic lessons.json with all content**
   - Why rejected: Large file becomes unwieldy, poor version control (entire file changes), no file organization

5. **Database for lesson storage**
   - Why rejected: Overkill for static content, adds runtime dependency, complicates deployment, not version controllable

6. **Python modules with lesson data**
   - Why rejected: Requires Python knowledge for content authors, mixing code with content, awkward for long text

**Related Decisions**
- Build process integration (Phase 1)
- Alpine.js for lesson selector UI (Phase 1)

---

## Alpine.js for Reactive UI Framework (2025-10-26)

**Status**: Accepted

**Context**
After implementing the YAML-based lesson structure (Phase 0) and building a multi-lesson generation system (Phase 1), needed a way to add client-side interactivity for lesson switching, dynamic content loading, and UI state management. The application needs reactive UI without heavy framework overhead, and must work well with server-rendered HTML.

**Decision**
Use Alpine.js v3 for client-side state management and reactive UI. Load from CDN, integrate with minimal wrapper (`appState()` function in `/static/js/app.js`), and inject lesson data via template variables (`window.CURRENT_LESSON`, `window.ALL_LESSONS`).

**Rationale**
- Extremely lightweight (~15KB gzipped) compared to React/Vue
- No build step required - works directly in browser
- Perfect for progressive enhancement of server-rendered HTML
- Declarative syntax similar to Vue.js (familiar to many developers)
- Minimal learning curve for simple use cases
- Works well with Jinja2-rendered templates
- Can start minimal and grow functionality incrementally

**Trade-offs**
- **Pros**:
  - Tiny bundle size, fast load time
  - No webpack/build configuration needed
  - Simple `x-data`, `x-show`, `x-bind` directives easy to understand
  - Can enhance existing HTML without rewriting
  - CDN delivery with good caching
  - Active development and community

- **Cons**:
  - Less powerful than React/Vue for complex apps
  - No component system (but not needed for this use case)
  - Smaller ecosystem than major frameworks
  - Limited TypeScript support
  - Performance may degrade with very large DOM trees (not our use case)

**Alternatives Considered**

1. **React**
   - Why rejected: Requires build step, much larger bundle size (~45KB), overkill for our use case, would require rewriting server-rendered HTML

2. **Vue.js**
   - Why rejected: Larger than Alpine (~33KB for runtime), requires more setup, progressive enhancement less natural

3. **Vanilla JavaScript**
   - Why rejected: Would need to manually implement reactivity, state management, and DOM updates - reinventing the wheel

4. **Svelte**
   - Why rejected: Requires build step and compilation, not suitable for CDN delivery, overkill for simple interactivity

5. **Petite-Vue**
   - Why rejected: While lightweight like Alpine, Alpine has better documentation and larger community

6. **htmx**
   - Why rejected: Great for server-driven interactions but doesn't provide client-side state management we need for lesson switching

**Related Decisions**
- YAML + Markdown lesson structure (provides the data Alpine will manage)
- Multi-lesson build system (generates the HTML Alpine enhances)
- Future: Lesson selector UI (Phase 2 - will use Alpine directives)

---

## CodeMirror 6 Keymap Precedence for Custom Shortcuts (2025-10-26)

**Status**: Accepted

**Context**
After migrating from CodeMirror 5 to CodeMirror 6, the keyboard shortcut for running code (Cmd/Ctrl+Enter) stopped working. Users reported that the shortcut previously worked but no longer functioned after the migration. The CodeMirror 6 migration had replaced the old `extraKeys` configuration with a new `keymap` API, but the shortcut implementation wasn't working.

**Decision**
Wrap custom keymaps with `Prec.highest()` from `@codemirror/state` to give them the highest precedence over default CodeMirror keymaps.

```javascript
import { Prec } from "@codemirror/state";

Prec.highest(keymap.of([
    {
        key: 'Mod-Enter',
        run: () => {
            runCode();
            return true;
        }
    }
]))
```

**Rationale**
- CodeMirror 6's `basicSetup` includes default keymaps that were intercepting Ctrl/Cmd+Enter before our custom handler could process it
- Without explicit precedence, custom keymaps run after default keymaps
- `Prec.highest()` ensures our keymap is checked first in the precedence chain
- Using `'Mod-Enter'` provides cross-platform compatibility (Cmd on Mac, Ctrl on Windows/Linux)
- Verified fix with Playwright test that simulates keyboard input

**Trade-offs**
- **Pros**:
  - Simple one-line fix with Prec.highest() wrapper
  - Cross-platform 'Mod' key works on all systems
  - Proper CodeMirror 6 API usage
  - Test coverage ensures it keeps working

- **Cons**:
  - Requires understanding of CodeMirror's precedence system
  - Overrides any future default behavior for this key
  - Additional import from @codemirror/state

**Alternatives Considered**

1. **Use domEventHandlers to intercept raw keyboard events**
   - Why rejected: This was attempted first but didn't work because CodeMirror's internal event handling still ran first. Raw DOM events don't have precedence over CodeMirror's keymap system.

2. **Remove conflicting keymaps from basicSetup**
   - Why rejected: Would require manually reconstructing basicSetup without certain keymaps, losing other useful defaults. Too fragile and complex.

3. **Use a different keyboard shortcut**
   - Why rejected: Cmd/Ctrl+Enter is standard for running code in many editors (Jupyter, VSCode, etc.). Users expect this shortcut to work.

4. **Move function definitions before editor initialization**
   - Why attempted: Initially thought the issue was function hoisting, so reorganized code to define runCode() before the editor. This was necessary but insufficient - precedence was the real issue.

**Related Decisions**
- CodeMirror 6 migration (see below)
- Cross-platform keyboard shortcuts using 'Mod' key

---

## CodeMirror 5 to CodeMirror 6 Migration (2025-10-26)

**Status**: Accepted

**Context**
The web editor was using CodeMirror 5, which uses a legacy global object API and older module system. CodeMirror 6 offers improved extensibility, better autocomplete API, and modern ES module architecture.

**Decision**
Migrate web editor from CodeMirror 5 to CodeMirror 6, updating:
- Import from ES modules instead of CDN script tags
- Replace autocomplete format from strings to objects with label/type/detail/info
- Update CSS selectors from `.CodeMirror` to `.cm-editor`
- Implement context-based completion function
- Use `keymap.of()` instead of `extraKeys` configuration

**Rationale**
- CodeMirror 6 is the actively maintained version
- Better autocomplete API allows richer completion info (types, descriptions, working examples)
- ES module architecture enables tree-shaking and better dev tools
- More extensible for future features
- Better TypeScript support and documentation

**Trade-offs**
- **Pros**:
  - Modern API with better documentation
  - Richer autocomplete capabilities
  - Active maintenance and community
  - Improved performance for large documents

- **Cons**:
  - Breaking changes required code rewrite
  - Different precedence model for keymaps (required learning)
  - Slightly larger initial bundle size
  - Some documentation scattered across multiple packages

**Alternatives Considered**

1. **Stay on CodeMirror 5**
   - Why rejected: End of life approaching, missing modern features, limited autocomplete API

2. **Monaco Editor (VSCode's editor)**
   - Why rejected: Much larger bundle size (~3MB vs ~500KB), more complex API, overkill for this use case

3. **Ace Editor**
   - Why rejected: Less active development than CodeMirror 6, older architecture

**Related Decisions**
- Keymap precedence fix (see above)
- Autocomplete with working examples

---

## Browser-First Development with Pyodide (2025-10-26)

**Status**: Accepted

**Context**
Educational Python library needs to be accessible to learners without requiring local Python installation. Traditional approach would be IPython/Jupyter notebooks, but these require complex setup.

**Decision**
Use Pyodide to run Python entirely in the browser, with a web-based editor as the primary interface. Support marimo notebooks as a secondary target.

**Rationale**
- Zero installation friction - works on any device with a browser
- Students can't "break" their environment
- Easy sharing via URLs
- Works on locked-down school computers
- Instant feedback loop
- Cross-platform by default

**Trade-offs**
- **Pros**:
  - No installation required
  - Universal accessibility
  - Can't break the environment
  - Easy to share and collaborate
  - Works on Chromebooks and tablets

- **Cons**:
  - 5-10 second initial load for Pyodide runtime
  - Requires HTTPS (even localhost needs self-signed cert)
  - Can't access file system
  - Limited to what Pyodide supports
  - No package installation (must use pre-bundled packages)

**Alternatives Considered**

1. **Jupyter/IPython as primary target**
   - Why rejected: Installation barrier too high for beginners, environment issues frustrating for learners

2. **Local Python REPL with turtle graphics**
   - Why rejected: Requires Python installation, turtle graphics outdated, inconsistent cross-platform behavior

3. **Online Python REPLs (Repl.it, Trinket)**
   - Why rejected: Requires account, subject to rate limits, no control over environment, could go away

4. **Python desktop app with embedded runtime**
   - Why rejected: Distribution complexity, per-platform builds, installation still required

**Related Decisions**
- HTTPS development server with self-signed certificates
- SVG output instead of canvas (inspectable in browser dev tools)

---

## Playwright Testing for Browser Functionality (2025-10-26)

**Status**: Accepted

**Context**
Browser-based application needs verification that the editor, Python execution, and UI interactions work correctly. Keyboard shortcuts specifically needed test coverage after the CodeMirror 6 migration broke them.

**Decision**
Use Playwright with Chromium for browser-based integration tests. Created 9 tests covering page load, Pyodide initialization, code execution, SVG rendering, API availability, and keyboard shortcuts.

**Rationale**
- Can test real browser interactions (keyboard events, DOM manipulation)
- Headless execution for CI/CD
- Cross-browser support if needed later
- Can interact with Pyodide runtime via page.evaluate()
- Catches regressions in keyboard shortcuts and UI behavior
- Modern API with good TypeScript support

**Trade-offs**
- **Pros**:
  - Tests real browser environment
  - Catches issues unit tests can't detect
  - Can test async JavaScript/Pyodide interactions
  - Verified keyboard shortcut fix works
  - Prevents regressions

- **Cons**:
  - Slower than unit tests (30 seconds for full suite)
  - Requires Playwright browser installation (~170MB)
  - More complex to debug than unit tests
  - Flaky if not carefully written

**Alternatives Considered**

1. **Jest with jsdom**
   - Why rejected: Can't test Pyodide (requires real browser with WASM), can't simulate real keyboard events

2. **Selenium**
   - Why rejected: Older API, slower, more flaky, less modern than Playwright

3. **Cypress**
   - Why rejected: Not designed for testing file:// protocol, more complex setup for our use case

4. **Manual testing only**
   - Why rejected: Keyboard shortcut broke and wasn't noticed until user reported. Automated tests prevent this.

**Related Decisions**
- Keyboard shortcut verification test added after bug fix
- Test runs in CI to catch regressions

---

## Single-File HTML Distribution via Jinja2 Templates (2025-10-26)

**Status**: Accepted

**Context**
Web interface needs to embed the Python shapes library code. Need to filter out browser-incompatible code (file I/O, unused classes) while keeping the code maintainable as a single source.

**Decision**
Use Jinja2 templates with a build process that:
1. Reads `sketchpy/shapes.py`
2. Removes browser-incompatible code (save(), Point dataclass, etc.)
3. Keeps necessary imports and _repr_html_() for marimo
4. Embeds processed code into HTML template
5. Outputs single `index.html` file

**Rationale**
- Single HTML file easy to distribute and deploy
- Build process ensures browser compatibility
- Python code stays maintainable in .py files
- Auto-rebuild on file changes during development
- Can version control both source and output
- Template system allows multiple variations

**Trade-offs**
- **Pros**:
  - Single file distribution
  - Automatic filtering of incompatible code
  - Maintains Python code in proper .py files
  - Easy to customize for different tutorials
  - Fast auto-rebuild during development

- **Cons**:
  - Build step required (not direct edit of HTML)
  - Template syntax adds complexity
  - Must remember to rebuild for changes to take effect
  - Output file can get large (~40KB currently)

**Alternatives Considered**

1. **Fetch shapes.py at runtime**
   - Why rejected: Requires web server, CORS issues, can't work offline, slower startup

2. **Write Python code directly in HTML**
   - Why rejected: Loses syntax highlighting, IDE support, version control diffs messy

3. **Separate JavaScript and Python files**
   - Why rejected: Multiple files harder to distribute, CORS issues with file:// protocol

4. **Bundle with webpack/rollup**
   - Why rejected: Too complex for this use case, overkill for embedding one Python file

**Related Decisions**
- Auto-rebuild on file changes via watchdog
- Background development server

---
