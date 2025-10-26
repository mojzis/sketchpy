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

        // Pyodide worker
        pyodideWorker: null,
        pyodideReady: false,

        // Current lesson and all lessons
        lesson: window.CURRENT_LESSON || null,
        lessons: window.ALL_LESSONS || [],
        currentLessonId: window.CURRENT_LESSON?.id,

        // Initialization
        init() {
            console.log('Alpine initialized');
            console.log('Current lesson:', this.lesson?.id);
            this.loadSidebarState();
            this.initPyodideWorker();
        },

        // Sidebar Management
        loadSidebarState() {
            const saved = localStorage.getItem('showSidebar');
            if (saved !== null) {
                this.showSidebar = saved === 'true';
            }
        },

        // Initialize Pyodide Worker
        initPyodideWorker() {
            console.log('Initializing Pyodide worker...');

            this.pyodideWorker = new Worker('/static/js/pyodide-worker.js');

            this.pyodideWorker.onmessage = (event) => {
                this.handleWorkerMessage(event);
            };

            this.pyodideWorker.onerror = (error) => {
                console.error('Worker error:', error);
                this.error = 'Worker initialization failed: ' + error.message;
            };

            // Send shapes code to worker
            // Note: shapes_code is injected via template as window.SHAPES_CODE
            this.pyodideWorker.postMessage({
                type: 'init',
                shapes: window.SHAPES_CODE
            });
        },

        // Handle messages from worker
        handleWorkerMessage(event) {
            const { type, output, svg, error } = event.data;

            if (type === 'ready') {
                console.log('Pyodide worker ready!');
                this.pyodideReady = true;
                document.getElementById('loading').style.display = 'none';
                document.getElementById('runBtn').disabled = false;
                document.getElementById('status').textContent = 'Ready! ✓';

                // Auto-run code on load
                this.runCode();
            } else if (type === 'result') {
                this.isRunning = false;

                const canvasDiv = document.getElementById('canvas');
                const errorDiv = document.getElementById('error');
                const statusSpan = document.getElementById('status');

                if (error) {
                    // Error occurred
                    this.error = error;
                    this.activeTab = 'output';
                    errorDiv.textContent = '❌ Error: ' + error;
                    errorDiv.style.display = 'block';
                    statusSpan.textContent = 'Error';
                    statusSpan.style.color = '#f44336';
                } else if (svg) {
                    // Success - got SVG
                    canvasDiv.innerHTML = svg;
                    this.activeTab = 'canvas';
                    statusSpan.textContent = 'Success! ✓';
                    statusSpan.style.color = '#4CAF50';
                    this.markComplete(this.currentLessonId);
                } else {
                    // No SVG returned
                    canvasDiv.innerHTML = '<div style="color: #999;">Make sure your code ends with "can" to display the canvas.</div>';
                    statusSpan.textContent = '';
                }

                // Store output
                this.output = output || '';
            }
        },

        // Run code (updated to use worker)
        async runCode() {
            if (this.isRunning || !this.pyodideReady) return;

            this.isRunning = true;
            this.output = '';
            this.error = '';
            this.activeTab = 'canvas';

            const code = window.editorView.state.doc.toString();
            const errorDiv = document.getElementById('error');
            const statusSpan = document.getElementById('status');

            errorDiv.style.display = 'none';
            statusSpan.textContent = 'Running...';

            // Send code to worker
            this.pyodideWorker.postMessage({
                type: 'run',
                code: code
            });
        },

        // Progress Tracking
        isCompleted(lessonId) {
            const progress = JSON.parse(localStorage.getItem('lessonProgress') || '{}');
            return !!progress[lessonId];
        },

        markComplete(lessonId) {
            const progress = JSON.parse(localStorage.getItem('lessonProgress') || '{}');
            progress[lessonId] = {
                completed: true,
                timestamp: new Date().toISOString()
            };
            localStorage.setItem('lessonProgress', JSON.stringify(progress));
            console.log(`Marked lesson ${lessonId} as complete`);
        },

        resetProgress() {
            if (confirm('Reset all progress? This cannot be undone.')) {
                localStorage.removeItem('lessonProgress');
                location.reload();
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
