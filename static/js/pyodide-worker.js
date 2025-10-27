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
