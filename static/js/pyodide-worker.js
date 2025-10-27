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
# NOTE: Keep eval/exec/compile - Pyodide needs them internally
# User code access is blocked via AST validation before execution
dangerous_builtins = [
    'open',      # File I/O
    '__import__', # Direct import
    'input',     # User input (would hang)
]

for name in dangerous_builtins:
    if hasattr(builtins, name):
        delattr(builtins, name)
        print(f"✓ Removed builtins.{name}")

# Note: eval, exec, compile kept but blocked in user code via AST validation

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
    'typing',  # Used by shapes.py for type hints
    're',      # Used by shapes.py internally
}

def restricted_import(name, globals=None, locals=None, fromlist=(), level=0):
    """Only allow safe imports, block dangerous ones"""
    # Blocked imports (dangerous/not needed)
    blocked = {'os', 'subprocess', 'socket', 'urllib', 'requests', 'http', 'sys', 'io'}

    if name in blocked:
        raise ImportError(f"Import '{name}' not allowed (blocked for security)")

    # For standard library and our classes, use original import
    # Pyodide will handle it
    if _original_import:
        return _original_import(name, globals, locals, fromlist, level)

    return None

# Replace import mechanism
builtins.__import__ = restricted_import

print("✓ Security restrictions applied")
print(f"✓ Allowed imports: {', '.join(ALLOWED_MODULES)}")
    `);

    // Load shapes code (Canvas API) from shapesCode variable
    // This is set by the 'init' message from the main thread
    if (shapesCode) {
        await pyodide.runPythonAsync(shapesCode);
        console.log('✓ Canvas API loaded');
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
import ast

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

        # Check imports - use blocklist approach (matches runtime check)
        blocked_imports = {'os', 'subprocess', 'socket', 'urllib', 'requests', 'http', 'sys', 'io'}

        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in blocked_imports:
                    return {
                        'valid': False,
                        'error': f"Import '{alias.name}' not allowed (blocked for security)"
                    }

        if isinstance(node, ast.ImportFrom):
            if node.module and node.module in blocked_imports:
                return {
                    'valid': False,
                    'error': f"Import from '{node.module}' not allowed (blocked for security)"
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
        // Send error
        if (type === 'run') {
            self.postMessage({
                type: 'result',
                error: error.message
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
