# Security Implementation Plan for sketchpy

**Target**: Secure Python code execution in browser via Pyodide
**Context**: Educational drawing app currently runs user code directly in main thread without restrictions
**Goal**: Multi-layer security preventing DoS, malicious imports, resource exhaustion, and unauthorized access

---

## Current Security Gaps (Critical)

Based on PROJECT_STATE.md - Phase 4 (Web Worker already implemented):

✅ **Web Worker isolation EXISTS** - Code runs in `static/js/pyodide-worker.js`
✅ **Non-blocking UI** - Worker communication via postMessage

Still missing:
1. ❌ **No execution timeout** - Infinite loops will freeze worker (but not UI)
2. ❌ **No import whitelist** - Can import any Pyodide module including `js`
3. ❌ **No memory limits** - Can create massive data structures
4. ❌ **No canvas size limits** - Can attempt 100000x100000 canvas
5. ❌ **No pre-validation** - Malicious patterns not caught before execution
6. ❌ **Direct access to JavaScript** - Can manipulate DOM via `js` module in worker

---

## Security Architecture

### Defense Layers

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: Client-Side Pre-Validation (Fast Fail)        │
│ - Regex pattern matching for forbidden keywords         │
│ - Length checks, AST parsing if possible                │
│ - Happens before any execution                          │
└────────────────────┬────────────────────────────────────┘
                     │ Pass
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Layer 2: Web Worker Isolation                           │
│ - Separate thread (can't freeze main UI)                │
│ - Terminable via postMessage                            │
│ - No DOM access by design                               │
└────────────────────┬────────────────────────────────────┘
                     │ Isolated
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Layer 3: Execution Timeout Wrapper                      │
│ - 5-second hard limit via setTimeout                    │
│ - Kills worker if exceeded                              │
│ - Recreates worker for next execution                   │
└────────────────────┬────────────────────────────────────┘
                     │ Time-boxed
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Layer 4: Pyodide Import Restrictions                    │
│ - Remove dangerous builtins (eval, exec, open, etc.)    │
│ - Block js module access                                │
│ - Whitelist only: Canvas, Color, palette classes        │
│ - AST validation for imports                            │
└────────────────────┬────────────────────────────────────┘
                     │ Sanitized
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Layer 5: Canvas API Constraints                         │
│ - Max canvas size: 2000x2000                            │
│ - Max shape count tracking                              │
│ - Memory-efficient SVG generation                       │
└─────────────────────────────────────────────────────────┘
```

---

## File Changes Required

### New Files to Create

```
static/
├── js/
│   ├── security/
│   │   ├── validator.js        # NEW: Pre-execution validation
│   │   ├── executor.js          # NEW: Worker management & timeout
│   │   └── config.js            # NEW: Security configuration
│   └── pyodide-worker.js        # EXISTS: Will be enhanced with security
│
sketchpy/
└── shapes.py                     # MODIFY: Add canvas size limits
```

### Files to Modify

```
static/
└── js/
    ├── pyodide-worker.js         # ENHANCE: Add security restrictions
    └── app.js                    # MODIFY: Use executor wrapper

templates/
└── lesson.html.jinja             # MODIFY: Import security modules

scripts/
└── build.py                      # MODIFY: Copy new JS files to output/
```

---

## Implementation Plan

### Phase 1: Security Configuration (30 min)

**File**: `static/js/security/config.js`

```javascript
/**
 * Security configuration for sketchpy code execution
 * All security limits defined in one place
 */
export const SecurityConfig = {
    // Execution Limits
    TIMEOUT_MS: 5000,                    // 5 second hard limit
    MAX_CODE_LENGTH: 10000,              // 10k characters max
    
    // Canvas Limits
    MAX_CANVAS_WIDTH: 2000,
    MAX_CANVAS_HEIGHT: 2000,
    MAX_CANVAS_AREA: 4000000,            // 2000 * 2000
    MAX_SHAPE_COUNT: 10000,              // Prevent render bombs
    
    // Import Whitelist
    ALLOWED_IMPORTS: new Set([
        'Canvas',
        'Color',
        'CreativeGardenPalette',
        'CalmOasisPalette',
    ]),
    
    // Forbidden Patterns (regex)
    FORBIDDEN_PATTERNS: [
        /\bimport\s+js\b/,               // import js
        /\bfrom\s+js\b/,                 // from js import
        /__import__\s*\(/,               // __import__(
        /\beval\s*\(/,                   // eval(
        /\bexec\s*\(/,                   // exec(
        /\bcompile\s*\(/,                // compile(
        /\bopen\s*\(/,                   // open(
        /__builtins__/,                  // __builtins__
        /\bglobals\s*\(/,                // globals(
        /\blocals\s*\(/,                 // locals(
        /\bvars\s*\(/,                   // vars(
        /\bdir\s*\(/,                    // dir(
        /\bgetattr\s*\(/,                // getattr(
        /\bsetattr\s*\(/,                // setattr(
        /\bdelattr\s*\(/,                // delattr(
        /\b__dict__\b/,                  // __dict__
        /\b__class__\b/,                 // __class__
    ],
    
    // Suspicious Large Values
    MAX_NUMERIC_VALUE: 1000000,          // Catch DoS attempts like range(10**9)
    
    // Worker Config
    WORKER_PATH: '/static/js/pyodide-worker.js',  // Existing worker location
    PYODIDE_VERSION: '0.25.0',
    PYODIDE_CDN: 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/',
};
```

**Action for Claude Code:**
- Create this file with the exact content above
- This is the single source of truth for all security limits

---

### Phase 2: Pre-Validation Layer (1 hour)

**File**: `static/js/security/validator.js`

```javascript
import { SecurityConfig } from './config.js';

/**
 * Client-side validation before code execution
 * Fast-fail checks to prevent obviously malicious code
 */
export class CodeValidator {
    
    /**
     * Validate Python code before execution
     * @param {string} code - Python code to validate
     * @returns {{valid: boolean, errors: string[]}}
     */
    static validate(code) {
        const errors = [];
        
        // Check 1: Length limit
        if (code.length > SecurityConfig.MAX_CODE_LENGTH) {
            errors.push(
                `Code too long: ${code.length} chars ` +
                `(max ${SecurityConfig.MAX_CODE_LENGTH})`
            );
        }
        
        // Check 2: Empty code
        if (code.trim().length === 0) {
            errors.push('Code is empty');
        }
        
        // Check 3: Forbidden patterns
        for (const pattern of SecurityConfig.FORBIDDEN_PATTERNS) {
            if (pattern.test(code)) {
                errors.push(`Forbidden pattern detected: ${pattern.source}`);
            }
        }
        
        // Check 4: Import whitelist (simple regex check)
        const importRegex = /(?:from\s+(\w+)|import\s+(\w+))/g;
        let match;
        const foundImports = new Set();
        
        while ((match = importRegex.exec(code)) !== null) {
            const moduleName = match[1] || match[2];
            foundImports.add(moduleName);
            
            if (!SecurityConfig.ALLOWED_IMPORTS.has(moduleName)) {
                errors.push(`Import '${moduleName}' not allowed. ` +
                           `Allowed imports: ${Array.from(SecurityConfig.ALLOWED_IMPORTS).join(', ')}`);
            }
        }
        
        // Check 5: Suspicious large numbers (DoS prevention)
        const largeNumberRegex = /\b\d{7,}\b/; // 7+ digits
        if (largeNumberRegex.test(code)) {
            errors.push('Suspicious large number detected (possible DoS attempt)');
        }
        
        // Check 6: Canvas size check (simple pattern match)
        const canvasRegex = /Canvas\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)/g;
        while ((match = canvasRegex.exec(code)) !== null) {
            const width = parseInt(match[1]);
            const height = parseInt(match[2]);
            
            if (width > SecurityConfig.MAX_CANVAS_WIDTH) {
                errors.push(`Canvas width ${width} exceeds max ${SecurityConfig.MAX_CANVAS_WIDTH}`);
            }
            if (height > SecurityConfig.MAX_CANVAS_HEIGHT) {
                errors.push(`Canvas height ${height} exceeds max ${SecurityConfig.MAX_CANVAS_HEIGHT}`);
            }
            if (width * height > SecurityConfig.MAX_CANVAS_AREA) {
                errors.push(`Canvas area ${width * height} exceeds max ${SecurityConfig.MAX_CANVAS_AREA}`);
            }
        }
        
        return {
            valid: errors.length === 0,
            errors: errors
        };
    }
    
    /**
     * Get friendly error message for display
     */
    static formatErrors(errors) {
        if (errors.length === 0) return '';
        
        return '❌ Security Validation Failed:\n\n' + 
               errors.map((e, i) => `${i + 1}. ${e}`).join('\n');
    }
}
```

**Action for Claude Code:**
- Create this file
- This runs BEFORE any Pyodide execution
- Fast regex-based checks, no Python parsing needed

---

### Phase 3: Timeout Wrapper for Existing Worker (1 hour)

**File**: `static/js/security/executor.js`

Note: `static/js/pyodide-worker.js` already exists and handles Pyodide loading. This new executor wraps it with timeout enforcement.

```javascript
import { SecurityConfig } from './config.js';

/**
 * Manages code execution in isolated Web Worker with timeout
 * Each execution gets a fresh worker if previous timed out
 */
export class CodeExecutor {
    constructor() {
        this.worker = null;
        this.pendingExecutions = new Map();
        this.executionId = 0;
        this.isWorkerReady = false;
        
        this.initWorker();
    }
    
    /**
     * Initialize or reinitialize worker
     */
    initWorker() {
        // Clean up old worker if exists
        if (this.worker) {
            this.worker.terminate();
        }
        
        this.worker = new Worker(SecurityConfig.WORKER_PATH);
        this.isWorkerReady = false;
        
        // Handle worker messages
        this.worker.onmessage = (event) => {
            const { id, type, success, data, error } = event.data;
            
            if (type === 'ready') {
                this.isWorkerReady = true;
                console.log('✓ Pyodide worker ready');
                return;
            }
            
            if (type === 'result') {
                const pending = this.pendingExecutions.get(id);
                
                if (pending) {
                    clearTimeout(pending.timeout);
                    
                    if (success) {
                        pending.resolve(data);
                    } else {
                        pending.reject(new Error(error));
                    }
                    
                    this.pendingExecutions.delete(id);
                }
            }
        };
        
        // Handle worker errors
        this.worker.onerror = (error) => {
            console.error('Worker error:', error);
            // Reject all pending executions
            for (const [id, pending] of this.pendingExecutions) {
                clearTimeout(pending.timeout);
                pending.reject(new Error('Worker crashed: ' + error.message));
            }
            this.pendingExecutions.clear();
            
            // Reinitialize worker
            this.initWorker();
        };
    }
    
    /**
     * Execute Python code with timeout protection
     * @param {string} code - Python code to execute
     * @param {number} timeoutMs - Timeout in milliseconds (default from config)
     * @returns {Promise<string>} SVG output from canvas
     */
    async execute(code, timeoutMs = SecurityConfig.TIMEOUT_MS) {
        // Wait for worker to be ready
        if (!this.isWorkerReady) {
            await this.waitForReady();
        }
        
        return new Promise((resolve, reject) => {
            const id = this.executionId++;
            
            // Create timeout that terminates worker
            const timeout = setTimeout(() => {
                this.pendingExecutions.delete(id);
                
                // Kill the worker (it's frozen)
                this.worker.terminate();
                
                // Create new worker for next execution
                this.initWorker();
                
                reject(new Error(
                    `⏱️ Execution timeout (${timeoutMs / 1000}s limit)\n\n` +
                    'Your code took too long to run. Possible causes:\n' +
                    '• Infinite loop (while True, etc.)\n' +
                    '• Too many shapes (try fewer iterations)\n' +
                    '• Complex calculations'
                ));
            }, timeoutMs);
            
            // Store pending execution
            this.pendingExecutions.set(id, { 
                resolve, 
                reject, 
                timeout,
                startTime: Date.now()
            });
            
            // Send to worker
            this.worker.postMessage({ 
                id, 
                type: 'execute',
                code 
            });
        });
    }
    
    /**
     * Wait for worker to initialize
     */
    async waitForReady(maxWaitMs = 30000) {
        const startTime = Date.now();
        
        while (!this.isWorkerReady) {
            if (Date.now() - startTime > maxWaitMs) {
                throw new Error('Worker initialization timeout');
            }
            await new Promise(resolve => setTimeout(resolve, 100));
        }
    }
    
    /**
     * Terminate worker and clean up
     */
    destroy() {
        if (this.worker) {
            this.worker.terminate();
            this.worker = null;
        }
        
        // Reject all pending
        for (const [id, pending] of this.pendingExecutions) {
            clearTimeout(pending.timeout);
            pending.reject(new Error('Executor destroyed'));
        }
        this.pendingExecutions.clear();
    }
}

// Global singleton instance
export const executor = new CodeExecutor();
```

**Action for Claude Code:**
- Create this file
- This manages the worker lifecycle and timeout enforcement
- Key feature: Terminates frozen workers and creates fresh ones

---

### Phase 4: Enhance Existing Pyodide Worker with Security (2 hours)

**File**: `static/js/pyodide-worker.js` (MODIFY EXISTING)

Note: This worker already exists and loads Pyodide. We're ADDING security restrictions to it.

```javascript
// Import Pyodide from CDN
importScripts('https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js');

let pyodide = null;
let shapesCode = null; // Will be populated with embedded Canvas API

/**
 * Initialize Pyodide and lock down dangerous functionality
 */
async function initPyodide() {
    if (pyodide) return;
    
    console.log('Initializing Pyodide in worker...');
    
    pyodide = await loadPyodide({
        indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/'
    });
    
    console.log('Pyodide loaded, applying security restrictions...');
    
    // Execute security lockdown
    await pyodide.runPythonAsync(`
import sys
import builtins

# === REMOVE DANGEROUS BUILTINS ===
dangerous_builtins = [
    'open',      # File I/O
    'eval',      # Code execution
    'exec',      # Code execution
    'compile',   # Code compilation
    '__import__', # Direct import
    'input',     # User input (would hang)
]

for name in dangerous_builtins:
    if hasattr(builtins, name):
        delattr(builtins, name)
        print(f"✓ Removed builtins.{name}")

# === BLOCK JS MODULE ===
# Prevent access to JavaScript bridge
if 'js' in sys.modules:
    del sys.modules['js']
sys.modules['js'] = None  # Block future imports

# === RESTRICT IMPORTS ===
# Store original __import__ before we deleted it
_original_import = builtins.__dict__.get('__import__')

# Whitelist of allowed modules
ALLOWED_MODULES = {
    'Canvas',
    'Color', 
    'CreativeGardenPalette',
    'CalmOasisPalette',
}

def restricted_import(name, globals=None, locals=None, fromlist=(), level=0):
    """Only allow whitelisted imports"""
    if name not in ALLOWED_MODULES:
        raise ImportError(f"Import '{name}' not allowed. Allowed: {', '.join(ALLOWED_MODULES)}")
    
    # These will be available from shapes_code
    return None

# Replace import mechanism
builtins.__import__ = restricted_import

print("✓ Security restrictions applied")
print(f"✓ Allowed imports: {', '.join(ALLOWED_MODULES)}")
    `);
    
    // Load shapes code (Canvas API) - we'll inject this
    // For now, fetch from server (build process will handle this)
    try {
        const response = await fetch('/static/shapes_embedded.py');
        shapesCode = await response.text();
        await pyodide.runPythonAsync(shapesCode);
        console.log('✓ Canvas API loaded');
    } catch (error) {
        console.error('Failed to load Canvas API:', error);
        throw error;
    }
    
    // Signal ready
    self.postMessage({ type: 'ready' });
}

/**
 * Additional AST-based validation in Python
 */
async function validateCode(code) {
    const validationScript = `
import ast

def validate_ast(code_string):
    """Deep validation using Python AST"""
    try:
        tree = ast.parse(code_string)
    except SyntaxError as e:
        return {'valid': False, 'error': f'Syntax error: {e}'}
    
    # Check for forbidden AST nodes
    forbidden_names = {
        'eval', 'exec', 'compile', '__import__',
        'open', 'input', 'globals', 'locals',
        'vars', 'dir', 'getattr', 'setattr', 'delattr'
    }
    
    for node in ast.walk(tree):
        # Check function calls
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in forbidden_names:
                    return {
                        'valid': False, 
                        'error': f"Function '{node.func.id}' is not allowed"
                    }
        
        # Check attribute access to __dict__, __class__, etc.
        if isinstance(node, ast.Attribute):
            if node.attr.startswith('__') and node.attr.endswith('__'):
                return {
                    'valid': False,
                    'error': f"Access to '{node.attr}' is not allowed"
                }
        
        # Check imports (should be caught by restricted_import, but double-check)
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name not in ['Canvas', 'Color', 'CreativeGardenPalette', 'CalmOasisPalette']:
                    return {
                        'valid': False,
                        'error': f"Import '{alias.name}' not allowed"
                    }
        
        if isinstance(node, ast.ImportFrom):
            if node.module and node.module not in ['Canvas', 'Color', 'CreativeGardenPalette', 'CalmOasisPalette']:
                return {
                    'valid': False,
                    'error': f"Import from '{node.module}' not allowed"
                }
    
    return {'valid': True}

# Run validation
validate_ast(${JSON.stringify(code)})
    `;
    
    const result = await pyodide.runPythonAsync(validationScript);
    return result.toJs({ dict_converter: Object.fromEntries });
}

/**
 * Execute user code and extract canvas output
 */
async function executeCode(code) {
    // Validate with AST
    const validation = await validateCode(code);
    if (!validation.valid) {
        throw new Error(validation.error);
    }
    
    // Execute the code
    await pyodide.runPythonAsync(code);
    
    // Check if canvas was created
    const canvasExists = await pyodide.runPythonAsync(`
'can' in dir() and hasattr(can, 'to_svg')
    `);
    
    if (!canvasExists) {
        throw new Error(
            'No canvas found!\n\n' +
            'Make sure your code creates a Canvas object named "can":\n' +
            'can = Canvas(800, 600)'
        );
    }
    
    // Get SVG output
    const svg = await pyodide.runPythonAsync('can.to_svg()');
    
    return svg;
}

/**
 * Handle messages from main thread
 */
self.onmessage = async (event) => {
    const { id, type, code } = event.data;
    
    try {
        if (type === 'execute') {
            // Initialize on first execution
            if (!pyodide) {
                await initPyodide();
            }
            
            // Execute code
            const svg = await executeCode(code);
            
            // Send success
            self.postMessage({
                id,
                type: 'result',
                success: true,
                data: svg
            });
        }
    } catch (error) {
        // Send error
        self.postMessage({
            id,
            type: 'result',
            success: false,
            error: error.message
        });
    }
};

// Error handling
self.onerror = (error) => {
    console.error('Worker uncaught error:', error);
};
```

**Action for Claude Code:**
- Create this file
- This is the most critical security component
- Runs in isolated Web Worker thread
- Removes dangerous builtins and blocks imports
- Uses AST validation for deep code inspection

---

### Phase 5: Canvas API Size Limits (30 min)

**File**: `sketchpy/shapes.py` (modifications)

Add size validation to Canvas constructor:

```python
class Canvas:
    """Canvas for drawing shapes with SVG output"""
    
    # Class constants for limits
    MAX_WIDTH = 2000
    MAX_HEIGHT = 2000
    MAX_AREA = 4_000_000  # 2000 * 2000
    MAX_SHAPES = 10_000
    
    def __init__(self, width: int, height: int):
        """
        Create a canvas with specified dimensions.
        
        Args:
            width: Canvas width in pixels (max 2000)
            height: Canvas height in pixels (max 2000)
        
        Raises:
            ValueError: If dimensions exceed limits
        """
        # Security: Enforce size limits
        if width > self.MAX_WIDTH:
            raise ValueError(
                f"Canvas width {width} exceeds maximum {self.MAX_WIDTH}"
            )
        if height > self.MAX_HEIGHT:
            raise ValueError(
                f"Canvas height {height} exceeds maximum {self.MAX_HEIGHT}"
            )
        if width * height > self.MAX_AREA:
            raise ValueError(
                f"Canvas area {width * height} exceeds maximum {self.MAX_AREA}"
            )
        
        if width <= 0 or height <= 0:
            raise ValueError("Canvas dimensions must be positive")
        
        self.width = width
        self.height = height
        self.shapes = []
    
    def _check_shape_limit(self):
        """Prevent too many shapes (render bomb protection)"""
        if len(self.shapes) >= self.MAX_SHAPES:
            raise ValueError(
                f"Shape limit exceeded ({self.MAX_SHAPES}). "
                "Too many shapes can crash the browser."
            )
    
    def rect(self, x, y, width, height, **kwargs):
        """Draw rectangle with shape limit check"""
        self._check_shape_limit()
        # ... rest of existing code
        
    def circle(self, x, y, radius, **kwargs):
        """Draw circle with shape limit check"""
        self._check_shape_limit()
        # ... rest of existing code
    
    # Add _check_shape_limit() to ALL drawing methods:
    # ellipse, line, polygon, text, rounded_rect, etc.
```

**Action for Claude Code:**
- Modify `sketchpy/shapes.py`
- Add MAX_WIDTH, MAX_HEIGHT, MAX_AREA, MAX_SHAPES constants
- Add validation in `__init__`
- Add `_check_shape_limit()` method
- Call `_check_shape_limit()` at start of EVERY drawing method

---

### Phase 6: Update Main App (1 hour)

**File**: `static/app.js` (modifications)

Replace direct Pyodide execution with secure executor:

```javascript
// OLD CODE (remove this):
// async function runCode() {
//     const code = editor.state.doc.toString();
//     await pyodide.runPythonAsync(code);
// }

// NEW CODE:
import { CodeValidator } from './js/security/validator.js';
import { executor } from './js/security/executor.js';

async function runCode() {
    const code = editor.state.doc.toString();
    
    // Show running indicator
    Alpine.store('app').status = 'running';
    Alpine.store('app').output = '';
    Alpine.store('app').error = '';
    
    try {
        // Step 1: Client-side validation
        const validation = CodeValidator.validate(code);
        if (!validation.valid) {
            Alpine.store('app').error = CodeValidator.formatErrors(validation.errors);
            Alpine.store('app').status = 'error';
            return;
        }
        
        // Step 2: Execute in worker with timeout
        const svg = await executor.execute(code);
        
        // Step 3: Display result
        Alpine.store('app').output = svg;
        Alpine.store('app').status = 'success';
        
    } catch (error) {
        Alpine.store('app').error = error.message;
        Alpine.store('app').status = 'error';
    }
}

// Also update keyboard shortcut handler
// ... existing runKeymap code ...
```

**Action for Claude Code:**
- Modify `static/app.js`
- Replace direct Pyodide calls with executor
- Add validation before execution
- Update error handling

---

### Phase 7: Update Build Process (30 min)

**File**: `scripts/build.py` (modifications)

Add copying of new security JS files (worker already being copied):

```python
def copy_static_files(output_dir):
    """Copy static files to output directory"""
    static_src = Path('static')
    static_dst = output_dir / 'static'
    
    # Create security directory
    (static_dst / 'js' / 'security').mkdir(parents=True, exist_ok=True)
    
    # Copy files (app.js and pyodide-worker.js already copied)
    files_to_copy = [
        'app.js',                        # Already being copied
        'js/pyodide-worker.js',          # Already being copied
        'js/security/config.js',         # NEW
        'js/security/validator.js',      # NEW
        'js/security/executor.js',       # NEW
    ]
    
    for file in files_to_copy:
        src = static_src / file
        dst = static_dst / file
        if src.exists():
            shutil.copy2(src, dst)
            print(f"✓ Copied {file}")
        else:
            print(f"⚠ Missing: {file}")
```

**Action for Claude Code:**
- Modify `scripts/build.py`
- Add copying of NEW security JS files (config, validator, executor)
- Worker and app.js likely already handled by existing build process

---

### Phase 8: Update HTML Template (30 min)

**File**: `templates/lesson.html.jinja`

Update to load new modules:

```html
<!-- Add after existing script tags -->
<script type="module">
    import { SecurityConfig } from '/static/js/security/config.js';
    import { CodeValidator } from '/static/js/security/validator.js';
    import { executor } from '/static/js/security/executor.js';
    
    // Make available to app.js
    window.SecurityConfig = SecurityConfig;
    window.CodeValidator = CodeValidator;
    window.executor = executor;
</script>

<!-- Then load app.js -->
<script type="module" src="/static/app.js"></script>
```

**Action for Claude Code:**
- Modify `templates/lesson.html.jinja`
- Add script imports for security modules
- Ensure correct load order

---

## Testing Strategy

### Security Test Cases

Create `tests/security_test.py`:

```python
"""Test security restrictions"""

def test_infinite_loop_timeout():
    """Should timeout and terminate worker"""
    code = "while True: pass"
    # Expect: Timeout error after 5 seconds

def test_forbidden_import_js():
    """Should reject js module import"""
    code = "import js\njs.document"
    # Expect: Validation error before execution

def test_forbidden_import_os():
    """Should reject os module import"""
    code = "import os"
    # Expect: Validation error

def test_large_canvas_rejected():
    """Should reject oversized canvas"""
    code = "can = Canvas(10000, 10000)"
    # Expect: Validation error (canvas size)

def test_eval_forbidden():
    """Should reject eval"""
    code = "eval('print(1)')"
    # Expect: Validation error

def test_open_forbidden():
    """Should reject file operations"""
    code = "open('file.txt', 'r')"
    # Expect: Validation error or runtime error

def test_shape_limit():
    """Should reject too many shapes"""
    code = """
can = Canvas(800, 600)
for i in range(20000):
    can.circle(100, 100, 10)
"""
    # Expect: Runtime error at 10,000 shapes

def test_large_range_timeout():
    """Should timeout on huge range"""
    code = """
can = Canvas(800, 600)
for i in range(10**9):
    can.circle(i, i, 1)
"""
    # Expect: Timeout after 5 seconds

def test_valid_code_works():
    """Should execute normal code successfully"""
    code = """
can = Canvas(800, 600)
can.rect(100, 100, 200, 150, fill=Color.RED)
"""
    # Expect: Success, SVG output returned
```

### Manual Testing Checklist

```
□ Run infinite loop → Should timeout after 5s
□ Import js module → Should reject with clear error
□ Create 100x100 canvas → Should work
□ Create 3000x3000 canvas → Should reject
□ Draw 100 shapes → Should work
□ Draw 15,000 shapes → Should reject at 10,000
□ Use eval() → Should reject
□ Use open() → Should reject
□ Normal lesson code → Should work perfectly
□ Switch lessons during execution → Should not crash
□ Run code while previous running → Should queue or reject
```

---

## Security Guarantees

After implementation, sketchpy will provide:

✅ **DoS Protection**
- 5-second execution timeout
- Canvas size limits (2000x2000)
- Shape count limits (10,000)
- Large number detection

✅ **Import Restrictions**
- Only whitelisted modules (Canvas, Color, palettes)
- JS module blocked
- Dangerous builtins removed (eval, exec, open, etc.)

✅ **Isolation**
- Web Worker execution (separate thread)
- No DOM access from Python
- No file system access
- No network access (except what Pyodide needs)

✅ **User Experience**
- Clear error messages
- UI doesn't freeze on bad code
- Fast validation feedback
- Works offline after initial load

---

## Implementation Order

**Day 1: Foundation (3-4 hours)**
1. Phase 1: Config file (30 min)
2. Phase 2: Validator (1 hour)
3. Phase 5: Canvas limits (30 min)
4. Phase 3: Executor wrapper (1 hour) - simpler since worker exists

**Day 2: Integration (3-4 hours)**
5. Phase 4: Enhance existing worker (2 hours) - adding security to existing code
6. Phase 6: Update app.js (1 hour)
7. Phase 7: Build process (30 min)
8. Phase 8: Template updates (30 min)

**Day 3: Testing (2-3 hours)**
9. Write security tests
10. Manual testing with malicious code
11. Test all lesson examples still work
12. Performance testing

**Total: ~10 hours for complete implementation** (reduced from 12 since worker infrastructure exists)

---

## Rollback Plan

If issues arise:

1. Keep old app.js as app.js.backup
2. Create feature flag in config: `SECURITY_ENABLED: true`
3. Can quickly disable by toggling flag
4. Old code path still available for emergency

---

## Future Enhancements

After core security is working:

1. **Memory limits**: Track pyodide memory usage
2. **Rate limiting**: Prevent spam execution
3. **Code signing**: Hash lesson starter code, detect modifications
4. **Telemetry**: Log security events (anonymized)
5. **Progressive timeout**: Warn at 3s, kill at 5s
6. **Code complexity analysis**: Estimate execution time before running

---

## Questions to Resolve

1. **Worker location**: Should worker be in `/static/js/workers/` or `/workers/`?
   - Recommendation: `/static/js/workers/` for consistency

2. **Shapes code loading**: Should worker fetch shapes.py or should it be embedded?
   - Recommendation: Embed in worker during build (faster, offline-capable)

3. **Error messages**: How verbose should security errors be?
   - Recommendation: Educational (explain WHY it's blocked, suggest alternatives)

4. **Shape limit**: Is 10,000 shapes reasonable for lessons?
   - Recommendation: Test with lesson 8-9 nested loops, adjust if needed

---

## Success Criteria

✅ Security implementation complete when:

1. All malicious code tests pass (timeout, import blocks, etc.)
2. All existing lesson examples still work
3. Browser tests pass with new architecture
4. No performance regression on normal code (<1s execution)
5. Clear error messages for security violations
6. Documentation updated with security features

---

## Notes for Claude Code

- **Priority**: Security over features
- **Error messages**: Must be educational, not scary
- **Testing**: Test each phase independently before integrating
- **Performance**: Worker initialization happens once, should be fast after
- **Offline**: Worker needs embedded shapes code, not fetched
- **Debugging**: Add console.log for security events during development

---

## File Change Summary

| File | Change Type | Lines Changed |
|------|-------------|---------------|
| `static/js/security/config.js` | NEW | ~60 |
| `static/js/security/validator.js` | NEW | ~120 |
| `static/js/security/executor.js` | NEW | ~150 |
| `static/js/pyodide-worker.js` | ENHANCE (exists) | ~150 additions |
| `sketchpy/shapes.py` | MODIFY | ~50 |
| `static/app.js` | MODIFY | ~30 |
| `scripts/build.py` | MODIFY | ~20 |
| `templates/lesson.html.jinja` | MODIFY | ~10 |
| `tests/security_test.py` | NEW | ~150 |
| **TOTAL** | | **~740 lines** |

---

**Ready for implementation. Begin with Phase 1.**