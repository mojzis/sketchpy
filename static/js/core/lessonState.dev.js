/**
 * Alpine.js application state for sketchpy lesson interface
 *
 * This module provides the reactive state and methods for the lesson page UI,
 * including Pyodide worker management, code execution, and progress tracking.
 *
 * @module lessonState
 */

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
 * import { createAppState } from './core/lessonState.js';
 * const state = createAppState();
 * Alpine.data('app', state);
 */
export function createAppState() {
    return {
        // UI visibility
        showSidebar: true,
        showInstructions: true,
        activeTab: 'canvas',

        // Execution state
        isRunning: false,
        output: '',
        error: null,  // Changed to null to store formatted error object
        errorText: '', // Plain text version for banner

        // Pyodide worker
        pyodideWorker: null,
        pyodideReady: false,
        editorReady: false,  // Track editor initialization

        // Error handler (initialized after Pyodide is ready)
        errorHandler: null,

        // Current lesson and all lessons
        lesson: window.CURRENT_LESSON || null,
        currentLessonId: window.CURRENT_LESSON?.id,
        selectedLessonId: null,  // Will be set in init() after Alpine renders

        // Theme support
        themes: window.ALL_THEMES || [],
        currentTheme: window.CURRENT_THEME || null,
        currentThemeId: null,  // Will be set in init() after Alpine renders

        // Get lessons for current theme
        get filteredLessons() {
            if (!this.themes || !Array.isArray(this.themes) || this.themes.length === 0) {
                return [];
            }
            const theme = this.themes.find(t => t.id === this.currentThemeId);
            return (theme && theme.lessons) ? theme.lessons : [];
        },

        // Initialization
        init() {
            console.log('Alpine initialized');
            console.log('Current lesson:', this.lesson?.id);
            this.loadSidebarState();

            // Defer dropdown initialization until after Alpine renders the options
            // This prevents the browser from defaulting to the first option
            this.$nextTick(() => {
                this.currentThemeId = window.CURRENT_THEME?.id || null;
                this.selectedLessonId = window.CURRENT_LESSON?.id || null;
                console.log('Dropdowns initialized:', this.currentThemeId, this.selectedLessonId);
            });

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

            // Use base path from configuration
            const basePath = window.BASE_PATH || '';
            const isInLessonsDir = window.location.pathname.includes('/lessons/');
            const workerPath = isInLessonsDir
                ? `${basePath}/static/js/pyodide-worker.dev.js`  // From lessons/ subdirectory
                : `${basePath}/static/js/pyodide-worker.dev.js`; // From root

            this.pyodideWorker = new Worker(workerPath);

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
        async handleWorkerMessage(event) {
            const { type, output, svg, error, errorData, code } = event.data;

            if (type === 'ready') {
                console.log('Pyodide worker ready!');
                this.pyodideReady = true;

                // Dynamically import error handler when Pyodide is ready
                try {
                    const basePath = window.BASE_PATH || '';
                    const { PyodideErrorHandler } = await import(`${basePath}/static/js/errorHandler.dev.js`);
                    this.errorHandler = new PyodideErrorHandler(null);
                    console.log('✓ Error handler ready');
                } catch (e) {
                    console.error('Failed to load error handler:', e);
                }

                document.getElementById('loading').style.display = 'none';
                document.getElementById('runBtn').disabled = false;
                document.getElementById('status').textContent = 'Ready! ✓';

                // Auto-run code only when BOTH Pyodide and editor are ready
                this.tryAutoRun();
            } else if (type === 'result') {
                this.isRunning = false;

                const canvasDiv = document.getElementById('canvas');
                const errorDiv = document.getElementById('error');
                const statusSpan = document.getElementById('status');

                if (error) {
                    // Error occurred - format it with errorHandler
                    let formattedError;

                    if (errorData && this.errorHandler) {
                        // Use structured error data to create friendly message
                        formattedError = this.errorHandler.formatForBeginners(errorData, code || window.editorView?.state.doc.toString());
                    } else if (this.errorHandler) {
                        // Try to extract error info from the message string
                        const parsedError = this.parseErrorMessage(error);
                        const currentCode = code || window.editorView?.state.doc.toString();

                        if (parsedError) {
                            formattedError = this.errorHandler.formatForBeginners(parsedError, currentCode);
                        } else {
                            // Fallback to simple format
                            const lineNum = this.extractLineFromMessage(error);
                            formattedError = {
                                title: 'Error',
                                explanation: error,
                                hint: this.getSimpleHint(error),
                                line: lineNum,
                                snippet: this.errorHandler && lineNum ?
                                    this.errorHandler.getSnippet(currentCode, lineNum) : null,
                                category: 'python'
                            };
                        }
                    } else {
                        // No error handler available
                        formattedError = {
                            title: 'Error',
                            explanation: error,
                            hint: null,
                            line: null,
                            snippet: null,
                            category: 'python'
                        };
                    }

                    // Store formatted error for UI
                    this.error = formattedError;
                    this.errorText = error; // Keep plain text for banner
                    this.activeTab = 'output';

                    // Update banner - just say to check output
                    errorDiv.innerHTML = '<span style="cursor: pointer;" @click="activeTab = \'output\'">⚠️ Error occurred - click to view details in Output tab</span>';
                    errorDiv.style.display = 'block';

                    statusSpan.textContent = 'Error';
                    statusSpan.style.color = '#f44336';

                    // Highlight error line in editor if available
                    if (formattedError.line && window.editorView) {
                        this.highlightErrorLine(formattedError.line);
                    }
                } else if (svg) {
                    // Success - got SVG
                    canvasDiv.innerHTML = svg;
                    this.activeTab = 'canvas';
                    statusSpan.textContent = 'Success! ✓';
                    statusSpan.style.color = '#4CAF50';
                    this.markComplete(this.currentLessonId);

                    // Clear any previous errors
                    this.error = null;
                    this.errorText = '';
                    errorDiv.style.display = 'none';
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

            const code = window.editorView?.state.doc.toString() || '';
            const errorDiv = document.getElementById('error');
            const statusSpan = document.getElementById('status');

            errorDiv.style.display = 'none';
            statusSpan.textContent = 'Running...';

            // Basic security validation (worker does deeper validation)
            // Check code length
            if (code.length > 10000) {
                this.isRunning = false;
                this.error = 'Code too long (max 10,000 characters)';
                errorDiv.textContent = '❌ ' + this.error;
                errorDiv.style.display = 'block';
                statusSpan.textContent = 'Error';
                return;
            }

            // Check for obviously forbidden patterns
            // Note: compile() is kept for Pyodide internal use
            const forbidden = [
                /\bimport\s+js\b/, /\bfrom\s+js\b/,
                /\beval\s*\(/, /\bexec\s*\(/, /\bopen\s*\(/
            ];
            for (const pattern of forbidden) {
                if (pattern.test(code)) {
                    this.isRunning = false;
                    this.error = `Forbidden pattern detected: ${pattern.source}`;
                    errorDiv.textContent = '❌ Security: ' + this.error;
                    errorDiv.style.display = 'block';
                    statusSpan.textContent = 'Error';
                    return;
                }
            }

            // Send code to worker (which will do full security validation)
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

        // Theme Navigation
        updateTheme() {
            // When theme changes, reset lesson selection and navigate to first lesson
            const theme = this.themes.find(t => t.id === this.currentThemeId);
            if (theme && theme.lessons.length > 0) {
                const firstLessonId = theme.lessons[0].id;
                this.selectedLessonId = firstLessonId;
                this.navigateToLesson(firstLessonId);
            }
        },

        navigateToLesson(lessonId) {
            const basePath = window.BASE_PATH || '';
            const theme = this.themes.find(t => t.id === this.currentThemeId);
            if (theme) {
                window.location.href = `${basePath}/lessons/${theme.id}/${lessonId}.html`;
            }
        },

        // Clear Canvas (moved from window.clearCanvas)
        clearCanvas() {
            document.getElementById('canvas').innerHTML = '<div style="color: #999;">Canvas cleared. Click "Run Code" to draw.</div>';
            document.getElementById('error').style.display = 'none';
            this.output = '';
            this.error = null;
            this.errorText = '';
        },

        // Get error icon based on category
        getErrorIcon(category) {
            const icons = {
                python: '⚠️',      // Learning opportunity
                security: 'ℹ️',    // Information
                timeout: '⏱️',     // Performance issue
                system: '⚙️'       // Technical problem
            };
            return icons[category] || '⚠️';
        },

        // Parse error message to extract structured info
        parseErrorMessage(errorMsg) {
            // Pyodide sends full traceback - we want only the last line (actual error)
            // Example full traceback:
            // Traceback (most recent call last):
            //   File "/lib/python311.zip/_pyodide/_base.py", line 573, in eval_code_async
            //   File "<exec>", line 20, in <module>
            // NameError: name 'hoho' is not defined

            if (!errorMsg) return null;

            // Split into lines and find the last line with an error type
            const lines = errorMsg.trim().split('\n');
            const errorLine = lines.reverse().find(line => /\w+Error:/.test(line));

            if (errorLine) {
                // Parse the error line: "NameError: name 'xx' is not defined"
                const match = errorLine.match(/(\w+Error):\s*(.+)/);
                if (match) {
                    return {
                        type: match[1],
                        message: match[2].trim(),
                        line: this.extractLineFromMessage(errorMsg)
                    };
                }
            }

            return null;
        },

        // Extract line number from error message
        extractLineFromMessage(errorMsg) {
            // Look for line number in <exec> frame (user's code), not Pyodide internals
            // Example: File "<exec>", line 20, in <module>
            const execMatch = errorMsg.match(/<exec>",\s*line\s+(\d+)/);
            if (execMatch) {
                return parseInt(execMatch[1]);
            }

            // Fallback: look for any line number (but this might be wrong)
            const match = errorMsg.match(/line (\d+)/i);
            return match ? parseInt(match[1]) : null;
        },

        // Get simple hint based on error message
        getSimpleHint(errorMsg) {
            if (errorMsg.includes('not defined')) {
                const match = errorMsg.match(/name '(\w+)' is not defined/);
                if (match) {
                    return `Define the variable first: ${match[1]} = ...`;
                }
                return 'Make sure to define variables before using them';
            }
            if (errorMsg.includes('Canvas') && errorMsg.includes('not found')) {
                return 'Create a canvas first: can = Canvas(800, 600)';
            }
            if (errorMsg.includes('SyntaxError')) {
                return 'Check for missing colons, quotes, or brackets';
            }
            if (errorMsg.includes('IndentationError')) {
                return 'Make sure all lines at the same level have the same spacing';
            }
            return null;
        },

        // Highlight error line in CodeMirror editor
        highlightErrorLine(lineNumber) {
            if (!window.editorView) return;

            try {
                const view = window.editorView;
                const doc = view.state.doc;

                // Get the line position
                if (lineNumber > 0 && lineNumber <= doc.lines) {
                    const line = doc.line(lineNumber);

                    // Scroll to the error line (simple scrolling without EditorView import)
                    view.dispatch({
                        selection: { anchor: line.from },
                        scrollIntoView: true
                    });

                    console.log(`Scrolled to error line ${lineNumber}`);
                }
            } catch (e) {
                console.error('Failed to highlight error line:', e);
            }
        },

        // Signal that editor is ready (called from editor initialization)
        setEditorReady() {
            console.log('Editor ready');
            this.editorReady = true;
            this.tryAutoRun();
        },

        // Try to auto-run code if both Pyodide and editor are ready
        tryAutoRun() {
            if (this.pyodideReady && this.editorReady) {
                console.log('Both Pyodide and editor ready - auto-running code');
                this.runCode();
            } else {
                console.log(`Waiting for initialization - Pyodide: ${this.pyodideReady}, Editor: ${this.editorReady}`);
            }
        }
    };
}
