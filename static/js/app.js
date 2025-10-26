/**
 * Alpine.js app state for sketchpy learning platform
 */

function appState() {
    return {
        // UI visibility
        showSidebar: true,
        showInstructions: true,
        activeTab: 'canvas',

        // Execution state
        isRunning: false,
        output: '',
        error: '',

        // Current lesson
        lesson: window.CURRENT_LESSON || null,

        // Initialization
        init() {
            console.log('Alpine initialized');
            console.log('Current lesson:', this.lesson?.id);
            this.loadSidebarState();
            this.initPyodide();
        },

        // Sidebar Management
        loadSidebarState() {
            const saved = localStorage.getItem('showSidebar');
            if (saved !== null) {
                this.showSidebar = saved === 'true';
            }
        },

        // Pyodide initialization (moved from inline script)
        async initPyodide() {
            // Wait for Pyodide to load
            window.pyodide = await loadPyodide();

            // Load shapes library (injected by template as window.SHAPES_CODE)
            if (window.SHAPES_CODE) {
                await window.pyodide.runPythonAsync(window.SHAPES_CODE);
            }

            document.getElementById('loading').style.display = 'none';
            document.getElementById('runBtn').disabled = false;
            document.getElementById('status').textContent = 'Ready! ✓';

            console.log('Pyodide ready');
        },

        // Code Execution (moved from window.runCode)
        async runCode() {
            if (this.isRunning) return;

            this.isRunning = true;
            this.output = '';
            this.error = '';
            this.activeTab = 'canvas';

            const code = window.editorView.state.doc.toString();
            const errorDiv = document.getElementById('error');
            const canvasDiv = document.getElementById('canvas');
            const statusSpan = document.getElementById('status');

            errorDiv.style.display = 'none';
            statusSpan.textContent = 'Running...';

            try {
                // Run the code
                await window.pyodide.runPythonAsync(code);

                // Get the canvas result
                const result = window.pyodide.globals.get('can');

                if (result && typeof result.to_svg === 'function') {
                    const svg = result.to_svg();
                    canvasDiv.innerHTML = svg;
                    statusSpan.textContent = 'Success! ✓';
                    statusSpan.style.color = '#4CAF50';
                } else {
                    canvasDiv.innerHTML = '<div style="color: #999;">Make sure your code ends with "can" to display the canvas.</div>';
                    statusSpan.textContent = '';
                }
            } catch (err) {
                this.error = err.message;
                this.activeTab = 'output';
                errorDiv.textContent = '❌ Error: ' + err.message;
                errorDiv.style.display = 'block';
                statusSpan.textContent = 'Error';
                statusSpan.style.color = '#f44336';
                console.error(err);
            } finally {
                this.isRunning = false;
            }
        },

        // Clear Canvas (moved from window.clearCanvas)
        clearCanvas() {
            document.getElementById('canvas').innerHTML = '<div style="color: #999;">Canvas cleared. Click "Run Code" to draw.</div>';
            document.getElementById('error').style.display = 'none';
            this.output = '';
            this.error = '';
        }
    }
}

// Make globally available
window.appState = appState;

// Keep these for backward compatibility with HTML onclick
window.runCode = function() {
    const app = Alpine.$data(document.querySelector('[x-data]'));
    if (app) app.runCode();
};

window.clearCanvas = function() {
    const app = Alpine.$data(document.querySelector('[x-data]'));
    if (app) app.clearCanvas();
};
