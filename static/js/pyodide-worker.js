/**
 * Web Worker for running Python code with Pyodide
 * Keeps UI thread responsive during code execution
 */

importScripts('https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js');

let pyodide = null;
let shapesCode = null;

// Initialize Pyodide
async function loadPyodideAndPackages() {
    console.log('[Worker] Loading Pyodide...');
    pyodide = await loadPyodide();
    console.log('[Worker] Pyodide loaded');

    // Load shapes library if available
    if (shapesCode) {
        await pyodide.runPythonAsync(shapesCode);
        console.log('[Worker] Shapes library loaded');
    }

    self.postMessage({ type: 'ready' });
}

// Handle messages from main thread
self.onmessage = async (event) => {
    const { type, code, shapes } = event.data;

    // Initialize Pyodide if needed
    if (!pyodide) {
        if (shapes) {
            shapesCode = shapes;
        }
        await loadPyodideAndPackages();
    }

    if (type === 'init') {
        // Already initialized above
        return;
    }

    if (type === 'run') {
        try {
            // Capture stdout
            let output = '';
            pyodide.setStdout({
                batched: (msg) => {
                    output += msg + '\n';
                }
            });

            // Run the code
            await pyodide.runPythonAsync(code);

            // Get canvas result
            const can = pyodide.globals.get('can');
            const svg = can && typeof can.to_svg === 'function' ? can.to_svg() : null;

            self.postMessage({
                type: 'result',
                output: output,
                svg: svg,
                error: null
            });
        } catch (error) {
            self.postMessage({
                type: 'result',
                output: '',
                svg: null,
                error: error.message
            });
        }
    }
};

// Start loading immediately
loadPyodideAndPackages();
