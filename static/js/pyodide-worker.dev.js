// Import Pyodide from CDN
importScripts('https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js');

// Import error handler (can't use ES6 import in worker, so we'll load it differently)
// For now, we'll implement the error handler inline in the worker
// TODO: Find a way to share the errorHandler code or duplicate key functionality here

let pyodide = null;
let shapesCode = null; // Will be populated with embedded Canvas API
let errorHandler = null; // Will be initialized after Pyodide is ready

/**
 * Initialize Pyodide and lock down dangerous functionality
 */
async function initPyodide() {
    if (pyodide) return;

    console.log('Initializing Pyodide in worker...');

    pyodide = await loadPyodide({
        indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/'
    });

    console.log('Pyodide loaded, applying initial security...');

    // Remove immediately dangerous builtins first
    await pyodide.runPythonAsync(`
import sys
import builtins

# === REMOVE TRULY DANGEROUS BUILTINS ===
# Keep eval/exec/compile for Pyodide, block via AST
dangerous_builtins = [
    'open',   # File I/O
    'input',  # User input (would hang)
]

for name in dangerous_builtins:
    if hasattr(builtins, name):
        delattr(builtins, name)
        print(f"✓ Removed builtins.{name}")

# === BLOCK JS MODULE ===
if 'js' in sys.modules:
    del sys.modules['js']
sys.modules['js'] = None

print("✓ Initial security applied")
    `);

    // Load shapes code (Canvas API) from shapesCode variable
    // This is set by the 'init' message from the main thread
    if (shapesCode) {
        await pyodide.runPythonAsync(shapesCode);
        console.log('✓ Canvas API loaded');

        // Import ast module BEFORE we block imports (needed for validation)
        // Pre-import everything ast.walk() needs to avoid blocking stdlib internals
        await pyodide.runPythonAsync(`
import builtins
import ast
import collections  # ast.walk() needs this internally
import sys

# Store original __import__ for stdlib use
_original_import = builtins.__import__

# Set of modules that are safe/needed for validation
_allowed_modules = {
    'collections', 'collections.abc', '_collections_abc',
    'ast', 'sys', 'builtins', 'typing', 're'
}

def block_user_imports(name, globals=None, locals=None, fromlist=(), level=0):
    """Block user code imports while allowing stdlib internals"""
    # Allow pre-approved stdlib modules needed for validation
    if name in _allowed_modules:
        return _original_import(name, globals, locals, fromlist, level)

    # Block everything else
    raise ImportError(
        f"Import '{name}' is not allowed.\\n\\n"
        f"You have everything you need:\\n"
        f"  • Canvas, Color (for drawing)\\n"
        f"  • CreativeGardenPalette, CalmOasisPalette (color palettes)\\n\\n"
        f"No imports needed for the lessons!"
    )

# Replace import with selective blocking function
builtins.__import__ = block_user_imports

print("✓ Imports restricted for user code (stdlib validation modules allowed)")
print("✓ ast module and dependencies pre-loaded")
        `);
    } else {
        console.warn('No shapes code provided yet, waiting for init message');
    }

    // Signal ready
    self.postMessage({ type: 'ready' });
}

/**
 * Additional AST-based validation in Python
 */
async function validateCode(code) {
    const validationScript = `
# ast module already imported globally during initialization - don't import again

def validate_ast(code_string):
    """Deep validation using Python AST"""
    try:
        tree = ast.parse(code_string)
    except SyntaxError as e:
        return {'valid': False, 'error': f'Syntax error: {e}'}

    # Check for forbidden AST nodes
    # Note: compile() kept for Pyodide internal use
    forbidden_names = {
        'eval', 'exec', '__import__',
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

        # Check imports - block ALL imports for maximum security
        if isinstance(node, ast.Import):
            return {
                'valid': False,
                'error': 'Imports are not allowed. You have Canvas, Color, and palettes already loaded!'
            }

        if isinstance(node, ast.ImportFrom):
            return {
                'valid': False,
                'error': 'Imports are not allowed. You have Canvas, Color, and palettes already loaded!'
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
    const { id, type, code, shapes } = event.data;

    try {
        // Handle init message (from app.js)
        if (type === 'init') {
            shapesCode = shapes;
            await initPyodide();
            return;
        }

        // Handle run message (from app.js - old protocol)
        if (type === 'run') {
            if (!pyodide) {
                await initPyodide();
            }

            // Validate and execute code
            const validation = await validateCode(code);
            if (!validation.valid) {
                self.postMessage({
                    type: 'result',
                    error: validation.error
                });
                return;
            }

            // Execute the code
            await pyodide.runPythonAsync(code);

            // Check if canvas was created
            const canvasExists = await pyodide.runPythonAsync(`
'can' in dir() and hasattr(can, 'to_svg')
            `);

            if (!canvasExists) {
                self.postMessage({
                    type: 'result',
                    error: 'No canvas found!\n\nMake sure your code creates a Canvas object named "can":\ncan = Canvas(800, 600)'
                });
                return;
            }

            // Get SVG output
            const svg = await pyodide.runPythonAsync('can.to_svg()');

            self.postMessage({
                type: 'result',
                svg: svg
            });
            return;
        }

        // Handle execute message (from executor - new security protocol)
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
        // Extract structured error information from Python if possible
        let errorData = null;
        if (pyodide && type === 'run') {
            try {
                // Use the get_error_info function we set up during initialization
                const getErrorInfo = pyodide.globals.get('get_error_info');
                if (getErrorInfo) {
                    const info = getErrorInfo();
                    if (info) {
                        errorData = info.toJs({ dict_converter: Object.fromEntries });
                        console.log('Extracted error data:', errorData);
                    }
                }
            } catch (e) {
                // If error extraction fails, just use the original error
                console.warn('Failed to extract Python error info:', e);
            }
        }

        // Send error with structured data
        if (type === 'run') {
            self.postMessage({
                type: 'result',
                error: error.message,
                errorData: errorData,  // Structured error info for formatting
                code: code  // Send code back for snippet extraction
            });
        } else {
            self.postMessage({
                id,
                type: 'result',
                success: false,
                error: error.message
            });
        }
    }
};

// Error handling
self.onerror = (error) => {
    console.error('Worker uncaught error:', error);
};
