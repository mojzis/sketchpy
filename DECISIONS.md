# Architectural and Implementation Decisions

## Decision Log Format
Each decision includes: Context, Decision, Rationale, Trade-offs, Alternatives Considered

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
