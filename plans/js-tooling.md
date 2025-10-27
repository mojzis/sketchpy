# JavaScript Tooling & Testing Infrastructure

**Status:** ✅ Prerequisites Complete - Ready for Phase 1
**Created:** 2025-10-27
**Updated:** 2025-10-27 (Browser tests fixed)
**Philosophy:** Add testing & quality tools WITHOUT sacrificing simplicity. Stay browser-first, avoid build complexity.

---

## Prerequisites ✅ COMPLETE

**Browser Tests Status:** ✅ All 11 tests passing (fixed 2025-10-27)

Before starting JS refactoring, browser tests were broken (9 of 11 failing) because they targeted the old `index.html` which is now a landing page. All tests have been updated to target `lessons/01-first-flower.html` where the actual editor lives.

**Test results:**
```
✅ test_page_loads_without_errors - Lesson page loads without errors
✅ test_pyodide_loads_successfully - Pyodide initializes in worker
✅ test_python_code_executes_without_errors - Python runs in worker
✅ test_canvas_renders_svg - Canvas renders SVG correctly
✅ test_color_class_available - Color class accessible
✅ test_canvas_class_available - Canvas class functional
✅ test_grid_method_works - Grid method renders correctly
✅ test_show_palette_method_works - Palette display works
✅ test_keyboard_shortcut_runs_code - Ctrl-Enter executes code
✅ test_lesson_page_editor_loads - CodeMirror editor loads
✅ test_lesson_page_run_button_visible - Run button present

Total: 11/11 passing in ~26 seconds
```

These tests will verify that JS refactoring doesn't break functionality.

---

## Problem Statement

sketchpy has grown from a Python library to a **real web application** with ~2,000 lines of JavaScript:

**Current JS footprint:**
- `errorHandler.js`: 596 lines (error formatting logic)
- `app.js`: 381 lines (Alpine state management - DEPRECATED, moved to template)
- `pyodide-worker.js`: 314 lines (Python execution, security)
- `security/executor.js`: 161 lines (timeout handling)
- `security/validator.js`: 90 lines (pre-validation)
- `security/config.js`: 52 lines (constants)
- **Embedded in templates**: ~385 lines (Alpine state, CodeMirror setup, API completions)

**Total:** ~2,000 lines of JavaScript

**Current gaps:**
- ❌ No unit tests for JS logic (only E2E browser tests)
- ❌ No linting or code quality checks
- ❌ No type checking (easy to introduce bugs)
- ❌ Large blocks of JS embedded in Jinja templates (hard to test)
- ❌ No IDE autocomplete for our own modules

**What we have:**
- ✅ Playwright E2E tests verify end-to-end functionality
- ✅ Python tests for build process
- ✅ CDN-based dependencies (Alpine, CodeMirror, Pyodide)

---

## Design Principles

### Core Values (MUST NOT VIOLATE)

1. **Browser-first simplicity** - No webpack/vite/babel complexity
2. **CDN dependencies** - Keep Alpine, CodeMirror, Pyodide from CDN
3. **Educational focus** - This is a teaching tool, not a production SaaS
4. **Python-primary** - JS is just the web interface, Python is the core
5. **Easy onboarding** - Contributors shouldn't need deep frontend knowledge

### Quality Goals (WHAT WE WANT)

1. **Testable** - Unit tests for critical logic (error formatting, validation)
2. **Type-safe** - Catch bugs before runtime with JSDoc type hints
3. **Linted** - Consistent code style, catch obvious errors
4. **Maintainable** - Separate concerns, no 385-line template scripts

---

## Three-Phase Implementation

### Phase 1: Extract & Lint (Week 1) - FOUNDATION
**Goal:** Separate JS from templates, add linting
**Effort:** ~4 hours
**Risk:** Low

#### Tasks

**1.1 Extract inline JavaScript from templates**

Currently `lesson.html.jinja` has ~385 lines of JS embedded in `<script>` tags:
- Lines 19-398: `appState()` function (Alpine state management)
- Lines 1119-1377: CodeMirror setup, API definitions, completions

**Action:**
```bash
# Create new organized structure
static/js/
  ├── core/
  │   ├── lessonState.js      # Alpine appState() (extracted from template)
  │   ├── editorSetup.js      # CodeMirror initialization
  │   └── apiDefinitions.js   # Canvas/Color API for autocomplete
  ├── errorHandler.js         # (existing, 596 lines)
  ├── pyodide-worker.js       # (existing, 314 lines)
  └── security/
      ├── config.js           # (existing, 52 lines)
      ├── validator.js        # (existing, 90 lines)
      └── executor.js         # (existing, 161 lines)
```

**Extract process:**
1. Copy `appState()` function → `static/js/core/lessonState.js`
   - Export as ES6 module: `export function createAppState() { ... }`
   - Keep Alpine integration logic

2. Copy CodeMirror setup → `static/js/core/editorSetup.js`
   - Export `initEditor(initialCode, onRun)` function
   - Import API definitions

3. Copy API definitions → `static/js/core/apiDefinitions.js`
   - Export `buildApiDefinitions(shapesCode)` function
   - Keep dynamic palette extraction logic

4. Update `lesson.html.jinja`:
   ```html
   <!-- BEFORE: 385 lines of inline JS -->

   <!-- AFTER: Clean imports -->
   <script type="module">
     import { createAppState } from '{{ base_path }}/static/js/core/lessonState.js';
     import { initEditor } from '{{ base_path }}/static/js/core/editorSetup.js';

     // Inject shapes code for modules to use
     window.SHAPES_CODE = `{{ shapes_code }}`;
     window.BASE_PATH = {{ base_path | tojson }};
     window.CURRENT_LESSON = {{ lesson | tojson }};
     window.ALL_LESSONS = {{ all_lessons | tojson }};

     // Initialize (15 lines instead of 385)
     window.appState = createAppState;
     window.editorView = initEditor(
       document.getElementById('editor').value,
       () => window.runCode()
     );
   </script>
   ```

**Benefits:**
- Template shrinks from 1,389 lines → ~1,020 lines
- JS modules become testable
- IDE provides autocomplete/navigation
- Easier to review changes (git diff)

**Testing impact:**
- E2E tests should pass unchanged (same runtime behavior)
- Module exports allow unit testing

---

**1.2 Add ESLint configuration**

```bash
# Initialize npm (if not exists)
npm init -y

# Install ESLint
npm install --save-dev eslint

# Initialize ESLint with recommended config
npx eslint --init
```

**ESLint choices:**
- How would you like to use ESLint? **To check syntax and find problems**
- What type of modules? **ES6 modules (import/export)**
- Which framework? **None** (we use Alpine from CDN)
- Does your project use TypeScript? **No** (JSDoc for types)
- Where does your code run? **Browser**
- Config file format? **JavaScript** (.eslintrc.js)

**Custom `.eslintrc.js`:**
```javascript
module.exports = {
  env: {
    browser: true,
    es2021: true,
    worker: true, // For pyodide-worker.js
  },
  extends: 'eslint:recommended',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  globals: {
    // CDN libraries
    Alpine: 'readonly',
    loadPyodide: 'readonly',

    // Template-injected globals
    SHAPES_CODE: 'readonly',
    BASE_PATH: 'readonly',
    CURRENT_LESSON: 'readonly',
    ALL_LESSONS: 'readonly',
    API_DEFINITIONS: 'writable',
  },
  rules: {
    'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
    'no-console': 'off', // Educational tool, console is fine
    'no-undef': 'error',
    'prefer-const': 'warn',
  },
};
```

**Add npm scripts to `package.json`:**
```json
{
  "scripts": {
    "lint": "eslint static/js/**/*.js",
    "lint:fix": "eslint --fix static/js/**/*.js",
    "lint:watch": "nodemon --watch static/js --exec 'npm run lint'"
  }
}
```

**Benefits:**
- Catch undefined variables
- Enforce consistent style
- IDE integration (VS Code, vim, etc.)
- Pre-commit hook potential

---

**1.3 Create documentation for JS modules**

Add JSDoc comments to all exported functions:

```javascript
/**
 * Creates Alpine.js application state for sketchpy lesson interface
 *
 * @returns {Object} Alpine reactive state object with methods:
 *   - init() - Initialize Pyodide worker and load saved state
 *   - runCode() - Execute Python code in worker
 *   - clearCanvas() - Reset canvas display
 *   - markComplete(lessonId) - Save lesson progress to localStorage
 *
 * @example
 * const state = createAppState();
 * Alpine.data('app', state);
 */
export function createAppState() {
  // ...
}
```

**Benefits:**
- Self-documenting code
- IDE shows parameter types and descriptions
- Easy onboarding for contributors

---

**Phase 1 Deliverables:**
- ✅ JS extracted into ES6 modules
- ✅ ESLint configured and passing
- ✅ npm scripts for linting
- ✅ JSDoc comments on public APIs
- ✅ Template reduced to ~1,020 lines
- ✅ E2E tests still passing

**Phase 1 Success Criteria:**
```bash
npm run lint           # ✅ No errors
uv run pytest          # ✅ All tests pass
uv run build && uv run srv  # ✅ App works identically
```

---

### Phase 2: Unit Testing (Week 2) - QUALITY
**Goal:** Test critical JS logic without browser overhead
**Effort:** ~6 hours
**Risk:** Low-Medium

#### Test Framework Choice: Vitest

**Why Vitest?**
- ✅ Runs ES modules natively (no Babel/webpack)
- ✅ Fast (Vite-based, but no Vite required)
- ✅ Jest-compatible API (familiar)
- ✅ Built-in coverage reporting
- ❌ NOT using for bundling (just testing)

**Installation:**
```bash
npm install --save-dev vitest @vitest/ui
```

**`vitest.config.js`:**
```javascript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom', // Simulate browser APIs
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      include: ['static/js/**/*.js'],
      exclude: ['static/js/**/*.test.js'],
    },
  },
});
```

---

#### Test Suite Structure

```
tests/js/
├── errorHandler.test.js    # High-value: 596 lines of logic
├── validator.test.js        # Medium-value: Security validation
├── apiDefinitions.test.js   # Medium-value: Autocomplete generation
├── lessonState.test.js      # Low-value: Mostly Alpine integration
└── fixtures/
    ├── sampleCode.py        # Valid Python snippets
    └── shapesCode.js        # Mock shapes_code for tests
```

---

#### 2.1 Test errorHandler.js (HIGHEST VALUE)

**Why test this?**
- Complex logic (596 lines)
- Transforms errors for beginners
- Easy to break during refactoring
- Pure functions (no DOM/worker dependencies)

**Test file: `tests/js/errorHandler.test.js`**

```javascript
import { describe, it, expect } from 'vitest';
import { PyodideErrorHandler } from '../../static/js/errorHandler.js';

describe('PyodideErrorHandler', () => {
  // Mock Pyodide instance (we don't need real Pyodide for tests)
  const mockPyodide = null;
  const handler = new PyodideErrorHandler(mockPyodide);

  describe('getTitle()', () => {
    it('returns friendly title for SyntaxError', () => {
      expect(handler.getTitle('SyntaxError')).toBe('Syntax Problem');
    });

    it('returns friendly title for NameError', () => {
      expect(handler.getTitle('NameError')).toBe('Variable Not Found');
    });

    it('returns generic title for unknown error', () => {
      expect(handler.getTitle('WeirdError')).toBe('Error');
    });
  });

  describe('getExplanation()', () => {
    it('explains NameError with variable name', () => {
      const explanation = handler.getExplanation(
        'NameError',
        "name 'x' is not defined"
      );
      expect(explanation).toContain('x');
      expect(explanation).toContain("haven't created it yet");
    });

    it('explains SyntaxError for unclosed quotes', () => {
      const explanation = handler.getExplanation(
        'SyntaxError',
        'EOL while scanning string literal'
      );
      expect(explanation).toContain('unclosed quote');
    });

    it('explains canvas size errors', () => {
      const explanation = handler.getExplanation(
        'ValueError',
        'Canvas width exceeds maximum (2000)'
      );
      expect(explanation).toContain('too wide');
      expect(explanation).toContain('2000 pixels');
    });
  });

  describe('getHint()', () => {
    it('provides actionable hint for NameError', () => {
      const hint = handler.getHint('NameError', "name 'speed' is not defined");
      expect(hint).toContain('speed = ...');
    });

    it('provides hint for indentation errors', () => {
      const hint = handler.getHint('IndentationError', 'unexpected indent');
      expect(hint).toContain('4 spaces');
    });

    it('returns null for errors without specific hints', () => {
      const hint = handler.getHint('RuntimeError', 'something broke');
      expect(hint).toBeNull();
    });
  });

  describe('getSnippet()', () => {
    it('extracts code snippet with context', () => {
      const code = 'line 1\nline 2\nline 3\nline 4\nline 5';
      const snippet = handler.getSnippet(code, 3);

      expect(snippet).toHaveLength(5); // 2 before, error, 2 after
      expect(snippet[2].number).toBe(3);
      expect(snippet[2].isError).toBe(true);
      expect(snippet[2].code).toBe('line 3');
    });

    it('handles error at start of file', () => {
      const code = 'line 1\nline 2\nline 3';
      const snippet = handler.getSnippet(code, 1);

      expect(snippet[0].number).toBe(1);
      expect(snippet[0].isError).toBe(true);
    });

    it('handles error at end of file', () => {
      const code = 'line 1\nline 2\nline 3';
      const snippet = handler.getSnippet(code, 3);

      const lastLine = snippet[snippet.length - 1];
      expect(lastLine.number).toBe(3);
      expect(lastLine.isError).toBe(true);
    });
  });

  describe('getCategory()', () => {
    it('categorizes security errors correctly', () => {
      expect(handler.getCategory('ImportError', 'import not allowed'))
        .toBe('security');
      expect(handler.getCategory('ValueError', 'Canvas width exceeds'))
        .toBe('security');
    });

    it('categorizes timeout errors', () => {
      expect(handler.getCategory('TimeoutError', 'took too long'))
        .toBe('timeout');
    });

    it('categorizes Python errors', () => {
      expect(handler.getCategory('SyntaxError', 'invalid syntax'))
        .toBe('python');
      expect(handler.getCategory('NameError', 'not defined'))
        .toBe('python');
    });
  });

  describe('formatForBeginners()', () => {
    it('creates complete formatted error object', () => {
      const errorData = {
        type: 'NameError',
        message: "name 'speed' is not defined",
        line: 5,
      };
      const code = 'can = Canvas(800, 600)\n...\nspeed = 100\n...\nprint(speeed)';

      const formatted = handler.formatForBeginners(errorData, code);

      expect(formatted).toMatchObject({
        title: 'Variable Not Found',
        category: 'python',
        line: 5,
      });
      expect(formatted.explanation).toBeTruthy();
      expect(formatted.hint).toBeTruthy();
      expect(formatted.snippet).toBeInstanceOf(Array);
    });
  });
});
```

**Coverage target:** 80%+ of errorHandler.js

---

#### 2.2 Test validator.js (SECURITY CRITICAL)

**Test file: `tests/js/validator.test.js`**

```javascript
import { describe, it, expect } from 'vitest';
import { validateCode } from '../../static/js/security/validator.js';

describe('Security Validator', () => {
  describe('Canvas size validation', () => {
    it('allows reasonable canvas sizes', () => {
      const code = 'can = Canvas(800, 600)';
      const result = validateCode(code);
      expect(result.valid).toBe(true);
    });

    it('blocks canvas width > 2000', () => {
      const code = 'can = Canvas(3000, 600)';
      const result = validateCode(code);
      expect(result.valid).toBe(false);
      expect(result.errors[0]).toContain('width');
    });

    it('blocks canvas height > 2000', () => {
      const code = 'can = Canvas(800, 3000)';
      const result = validateCode(code);
      expect(result.valid).toBe(false);
      expect(result.errors[0]).toContain('height');
    });
  });

  describe('Import blocking', () => {
    it('blocks "import os"', () => {
      const code = 'import os\ncan = Canvas(800, 600)';
      const result = validateCode(code);
      expect(result.valid).toBe(false);
      expect(result.errors[0]).toContain('Import');
    });

    it('blocks "from js import"', () => {
      const code = 'from js import document';
      const result = validateCode(code);
      expect(result.valid).toBe(false);
    });

    it('allows Canvas and Color (no import needed)', () => {
      const code = 'can = Canvas(800, 600)\ncan.rect(0, 0, 100, 100, fill=Color.RED)';
      const result = validateCode(code);
      expect(result.valid).toBe(true);
    });
  });

  describe('Forbidden pattern detection', () => {
    it('blocks eval()', () => {
      const code = 'x = eval("1 + 1")';
      const result = validateCode(code);
      expect(result.valid).toBe(false);
      expect(result.errors[0]).toContain('eval');
    });

    it('blocks open()', () => {
      const code = 'f = open("file.txt")';
      const result = validateCode(code);
      expect(result.valid).toBe(false);
    });

    it('allows compile() - used by Pyodide internally', () => {
      // Note: compile() is kept for Pyodide
      const code = 'can = Canvas(800, 600)';
      const result = validateCode(code);
      expect(result.valid).toBe(true);
    });
  });

  describe('Code length limits', () => {
    it('blocks code > 10,000 characters', () => {
      const code = 'x = 1\n'.repeat(3000); // > 10k chars
      const result = validateCode(code);
      expect(result.valid).toBe(false);
      expect(result.errors[0]).toContain('too long');
    });
  });
});
```

**Coverage target:** 90%+ (security-critical)

---

#### 2.3 Test API definitions extractor

**Test file: `tests/js/apiDefinitions.test.js`**

```javascript
import { describe, it, expect } from 'vitest';
import { buildApiDefinitions } from '../../static/js/core/apiDefinitions.js';

describe('API Definitions Builder', () => {
  const mockShapesCode = `
class Color:
    RED = "#FF0000"
    BLUE = "#0000FF"
    GREEN = "#00FF00"

class CreativeGardenPalette:
    PEACH_WHISPER = "#FFE5D9"
    ROSE_QUARTZ = "#FFCAD4"

class Canvas:
    def circle(self, x, y, radius, fill=None):
        pass
  `;

  it('extracts Color constants', () => {
    const api = buildApiDefinitions(mockShapesCode);

    expect(api.Color).toContainEqual({
      label: 'RED',
      type: 'constant',
      apply: 'RED',
      info: 'Color constant',
    });
    expect(api.Color).toHaveLength(3);
  });

  it('extracts CreativeGardenPalette constants', () => {
    const api = buildApiDefinitions(mockShapesCode);

    expect(api.CreativeGardenPalette).toContainEqual({
      label: 'PEACH_WHISPER',
      type: 'constant',
      apply: 'PEACH_WHISPER',
      info: 'CreativeGardenPalette color',
    });
  });

  it('includes Canvas methods', () => {
    const api = buildApiDefinitions(mockShapesCode);

    const circleMethod = api.can.find(m => m.label === 'circle');
    expect(circleMethod).toBeDefined();
    expect(circleMethod.type).toBe('method');
    expect(circleMethod.detail).toContain('radius');
  });
});
```

---

#### Phase 2 npm scripts

**Add to `package.json`:**
```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest run --coverage",
    "test:e2e": "cd .. && uv run pytest tests/test_browser.py"
  }
}
```

**Integration with Python test suite:**

Update `scripts/test.py`:
```python
#!/usr/bin/env python3
"""Run all tests (Python + JavaScript)"""
import subprocess
import sys

def main():
    print("🐍 Running Python tests...")
    result = subprocess.run(["pytest", "-v"], cwd=".")
    if result.returncode != 0:
        sys.exit(1)

    print("\n📦 Running JavaScript tests...")
    result = subprocess.run(["npm", "test"], cwd=".")
    if result.returncode != 0:
        sys.exit(1)

    print("\n✅ All tests passed!")

if __name__ == "__main__":
    main()
```

---

**Phase 2 Deliverables:**
- ✅ Vitest configured for ES modules
- ✅ Unit tests for errorHandler.js (20+ tests)
- ✅ Unit tests for validator.js (15+ tests)
- ✅ Unit tests for apiDefinitions.js (5+ tests)
- ✅ 80%+ code coverage on tested modules
- ✅ `npm test` runs unit tests
- ✅ Python test script runs both suites

**Phase 2 Success Criteria:**
```bash
npm test                    # ✅ All JS unit tests pass
npm run test:coverage       # ✅ 80%+ coverage
uv run pytest               # ✅ All Python/E2E tests pass
uv run python scripts/test.py  # ✅ Full suite passes
```

---

### Phase 3: Type Safety (Week 3) - OPTIONAL
**Goal:** Catch type errors before runtime using JSDoc
**Effort:** ~3 hours
**Risk:** Low

#### Why JSDoc instead of TypeScript?

**TypeScript pros:**
- ✅ Best type safety
- ✅ Industry standard
- ✅ Great tooling

**TypeScript cons:**
- ❌ Requires build step (tsc)
- ❌ Another language to learn
- ❌ Violates "browser-first simplicity"
- ❌ npm/build complexity

**JSDoc pros:**
- ✅ NO build step required
- ✅ Works in plain JavaScript
- ✅ TypeScript-level checking in VS Code
- ✅ Gradual adoption
- ✅ Still runnable without types

**JSDoc cons:**
- ❌ More verbose than TypeScript
- ❌ Less powerful type inference

**Decision:** Use JSDoc for type checking without build step.

---

#### 3.1 Add TypeScript for type checking only

```bash
# Install TypeScript CLI (for type checking only, NOT transpiling)
npm install --save-dev typescript

# Create tsconfig.json for checking JavaScript
```

**`tsconfig.json`:**
```json
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": true,
    "noEmit": true,  // Don't generate .js files
    "target": "ES2021",
    "module": "ES2022",
    "moduleResolution": "node",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "lib": ["ES2021", "DOM", "WebWorker"]
  },
  "include": ["static/js/**/*.js"],
  "exclude": ["node_modules", "output"]
}
```

**Add npm script:**
```json
{
  "scripts": {
    "typecheck": "tsc",
    "typecheck:watch": "tsc --watch"
  }
}
```

---

#### 3.2 Add JSDoc type annotations

**Example: `errorHandler.js`**

```javascript
/**
 * @typedef {Object} ErrorData
 * @property {string} type - Python error type (e.g., 'SyntaxError')
 * @property {string} message - Error message from Python
 * @property {number|null} line - Line number where error occurred
 */

/**
 * @typedef {Object} FormattedError
 * @property {string} title - Beginner-friendly title
 * @property {string} explanation - Clear explanation of the problem
 * @property {string|null} hint - Actionable suggestion
 * @property {number|null} line - Line number
 * @property {Array<SnippetLine>|null} snippet - Code context
 * @property {'python'|'security'|'timeout'|'system'} category - Error category
 */

/**
 * @typedef {Object} SnippetLine
 * @property {number} number - Line number (1-indexed)
 * @property {string} code - Line content
 * @property {boolean} isError - Whether this is the error line
 */

export class PyodideErrorHandler {
  /**
   * @param {any} pyodide - Pyodide instance (or null for testing)
   */
  constructor(pyodide) {
    this.pyodide = pyodide;
  }

  /**
   * Transforms Python error data into beginner-friendly format
   *
   * @param {ErrorData} errorData - Error data from Python
   * @param {string} code - User's code for extracting snippets
   * @returns {FormattedError} Formatted error object
   */
  formatForBeginners(errorData, code) {
    const { type, message, line } = errorData;

    return {
      title: this.getTitle(type),
      explanation: this.getExplanation(type, message),
      hint: this.getHint(type, message),
      line: line,
      snippet: this.getSnippet(code, line),
      category: this.getCategory(type, message)
    };
  }

  /**
   * Gets beginner-friendly error title
   *
   * @param {string} type - Python error type
   * @returns {string} Short, friendly title
   */
  getTitle(type) {
    // Implementation...
  }
}
```

**Benefits:**
- IDE autocomplete shows parameter types
- Catch type mismatches before runtime
- Documentation + types in one place
- Zero runtime overhead

---

#### 3.3 Gradual adoption strategy

**Priority order (highest value first):**

1. **errorHandler.js** - Complex logic, many functions
2. **validator.js** - Security-critical, easy to break
3. **core/apiDefinitions.js** - Returns structured data
4. **pyodide-worker.js** - Message passing (easy to mess up)
5. **core/lessonState.js** - Complex Alpine state object

**Don't annotate:**
- Simple getters/setters
- One-line utility functions
- Template glue code

---

**Phase 3 Deliverables:**
- ✅ TypeScript installed (check-only mode)
- ✅ `tsconfig.json` configured for JSDoc
- ✅ 3 core modules fully annotated (errorHandler, validator, apiDefinitions)
- ✅ `npm run typecheck` passes with 0 errors
- ✅ IDE shows type hints and errors

**Phase 3 Success Criteria:**
```bash
npm run typecheck          # ✅ No type errors
# In VS Code: Hover over function → see types
# In VS Code: Call function with wrong type → red squiggle
```

---

## Testing Strategy Summary

### Test Pyramid

```
        ╱╲
       ╱  ╲  E2E Tests (Playwright)
      ╱────╲  - Full browser integration
     ╱      ╲  - 3 tests (build, runtime, canvas)
    ╱────────╲
   ╱ Unit Tests ╲ (Vitest)
  ╱  (JS logic)  ╲ - errorHandler (~25 tests)
 ╱                ╲ - validator (~15 tests)
╱──────────────────╲ - apiDefinitions (~5 tests)
```

### What to test vs. skip

**✅ HIGH VALUE - Unit test:**
- Error formatting logic (errorHandler.js)
- Security validation (validator.js)
- API extraction (apiDefinitions.js)
- Pure functions with complex logic

**⚠️ MEDIUM VALUE - E2E test only:**
- Alpine state management (lessonState.js)
- CodeMirror integration (editorSetup.js)
- Worker message passing (pyodide-worker.js)

**❌ LOW VALUE - Skip:**
- Template rendering (Jinja2 + Python tests cover this)
- CDN library behavior (Alpine, CodeMirror, Pyodide)
- CSS styling
- Simple getters/setters

### Coverage targets

- **errorHandler.js:** 80%+ (high complexity)
- **validator.js:** 90%+ (security-critical)
- **apiDefinitions.js:** 70%+ (mostly regex)
- **Overall JS:** 60%+ (reasonable for educational project)

---

## Migration Plan

### Week 1: Phase 1 (Extract & Lint)
- **Monday:** Extract lessonState.js from template
- **Tuesday:** Extract editorSetup.js and apiDefinitions.js
- **Wednesday:** Configure ESLint, fix linting errors
- **Thursday:** Add JSDoc comments to public APIs
- **Friday:** Test E2E, verify no regressions

### Week 2: Phase 2 (Unit Tests)
- **Monday:** Install Vitest, configure, write errorHandler tests
- **Tuesday:** Finish errorHandler tests (~25 tests)
- **Wednesday:** Write validator tests (~15 tests)
- **Thursday:** Write apiDefinitions tests (~5 tests)
- **Friday:** Review coverage, add missing tests

### Week 3: Phase 3 (Type Safety) - OPTIONAL
- **Monday:** Configure TypeScript (check-only)
- **Tuesday:** Annotate errorHandler.js
- **Wednesday:** Annotate validator.js and apiDefinitions.js
- **Thursday:** Fix type errors
- **Friday:** Documentation, review

---

## Success Metrics

### Quantitative
- ✅ Template size: 1,389 lines → ~1,020 lines (-27%)
- ✅ Linting errors: 0
- ✅ Unit test coverage: 70%+
- ✅ Type errors: 0
- ✅ E2E test pass rate: 100%

### Qualitative
- ✅ JS modules are testable in isolation
- ✅ IDE provides autocomplete for our code
- ✅ Changes to errorHandler require tests
- ✅ Security validation is verified by tests
- ✅ Contributor onboarding easier (smaller template)

---

## What We're NOT Doing

### ❌ Build tooling (bundlers, transpilers)
**Why:** CDN approach works, no need for webpack/vite complexity

### ❌ Frontend frameworks (React, Vue, Svelte)
**Why:** Alpine.js from CDN is sufficient for our needs

### ❌ CSS tooling (PostCSS, Sass, Tailwind)
**Why:** Vanilla CSS is clean and simple (~600 lines)

### ❌ Minification/optimization
**Why:** Educational tool, size isn't critical

### ❌ TypeScript transpilation
**Why:** JSDoc gives us types without build step

### ❌ Aggressive modularization
**Why:** ~2,000 lines is manageable, don't over-engineer

---

## Risks & Mitigation

### Risk 1: Breaking E2E tests during extraction
**Likelihood:** Medium
**Impact:** High
**Mitigation:**
- Run E2E tests after each extraction step
- Keep git commits atomic (one module extraction per commit)
- Test in browser manually before committing

### Risk 2: ESLint finds hundreds of issues
**Likelihood:** Medium
**Impact:** Medium
**Mitigation:**
- Start with `eslint:recommended` only
- Use `--fix` for auto-fixable issues
- Add rules gradually
- Allow warnings initially, fix incrementally

### Risk 3: Vitest incompatible with ES modules
**Likelihood:** Low
**Impact:** Medium
**Mitigation:**
- Vitest is designed for ES modules
- Test setup with minimal example first
- Fallback: Use Jest with experimental ESM support

### Risk 4: JSDoc too verbose, reduces readability
**Likelihood:** Low
**Impact:** Low
**Mitigation:**
- Only annotate public APIs and complex functions
- Skip obvious types (getTitle returns string)
- Use `@typedef` to reduce repetition

---

## Alternatives Considered

### Alternative 1: Keep everything inline in templates
**Pros:** No change, works today
**Cons:** Not testable, hard to maintain as JS grows
**Verdict:** ❌ Rejected - already at 2,000 lines

### Alternative 2: Full TypeScript + Vite bundler
**Pros:** Best developer experience, type safety, hot reload
**Cons:** Major complexity increase, violates simplicity principle
**Verdict:** ❌ Rejected - too heavy for educational project

### Alternative 3: Just add ESLint, skip testing
**Pros:** Low effort, catches obvious bugs
**Cons:** No way to test error formatting logic
**Verdict:** ⚠️ Viable fallback if time-constrained

### Alternative 4: Use Python tests only (Playwright everywhere)
**Pros:** One test framework, already working
**Cons:** Slow, heavy, can't test pure JS logic
**Verdict:** ❌ Rejected - E2E tests complement but don't replace unit tests

---

## Dependencies Added

**Package.json additions:**
```json
{
  "devDependencies": {
    "eslint": "^9.0.0",
    "vitest": "^2.0.0",
    "@vitest/ui": "^2.0.0",
    "typescript": "^5.4.0",
    "jsdom": "^24.0.0"
  }
}
```

**Total size:** ~15 MB in node_modules (dev-only, not deployed)

---

## Documentation Updates

### Files to update:
1. **CLAUDE.md** - Add "JavaScript Testing" section
2. **README.md** - Add npm commands (`npm test`, `npm run lint`)
3. **CONTRIBUTING.md** (new) - Contributor guide for JS changes
4. **static/js/README.md** (new) - Architecture overview

---

## Future Enhancements (Post-Phase 3)

### Potential additions (evaluate later):
- **Pre-commit hooks** - Run lint + tests before commit
- **GitHub Actions** - Run tests on PRs
- **Coverage badges** - Show test coverage in README
- **Storybook** - Component playground (if UI grows)
- **Performance testing** - Benchmark error formatting speed

---

## Conclusion

This plan adds **testing & quality tools** without sacrificing the **browser-first simplicity** that makes sketchpy maintainable.

**Core trade-off:**
- ✅ Gain: Testable code, type safety, linting
- ❌ Cost: ~15 MB node_modules (dev-only), 3 new npm scripts

**Alignment with values:**
- ✅ Browser-first: No bundler, CDN dependencies unchanged
- ✅ Educational focus: Better error messages verified by tests
- ✅ Python-primary: JS testing complements, doesn't replace Python
- ✅ Easy onboarding: Smaller templates, documented modules

**Timeline:** 3 weeks, 13 hours total effort (low risk, high value)

---

## Next Steps

1. **Review this plan** - Discuss with team/self
2. **Phase 1 (Extract & Lint)** - Start with lessonState.js extraction
3. **Validate approach** - Run E2E tests, verify no regressions
4. **Phase 2 (Unit Tests)** - Add Vitest, write errorHandler tests
5. **Phase 3 (Types)** - Optional, only if Phase 1+2 succeed

**Decision point:** After Phase 1, evaluate if Phase 2 is worth effort.
