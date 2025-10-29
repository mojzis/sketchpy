/**
 * PyodideErrorHandler - Transforms technical Python errors into beginner-friendly messages
 *
 * This module is part of the sketchpy educational Python graphics library's error handling
 * system. It transforms technical Python tracebacks and system errors into clear, friendly
 * messages that guide students toward solutions.
 *
 * ARCHITECTURE:
 * This error handler is Layer 4 in the security architecture:
 *
 * Layer 1: Pre-Validation (validator.js) → formatValidationError()
 * Layer 2: Execution Timeout (executor.js) → formatTimeoutError()
 * Layer 3: Python Execution (pyodide-worker.js) → handleError()
 * Layer 4: Error Handler (this module) → Friendly message display
 *
 * ERROR CATEGORIES:
 * - python: Learning opportunities (SyntaxError, NameError, etc.) → Orange/Yellow theme
 * - security: Informative limits (imports, canvas size) → Blue theme
 * - timeout: Performance issues (infinite loops) → Purple theme
 * - system: Technical problems (worker crashes) → Gray theme
 *
 * INTEGRATION POINTS:
 * - app.js: Main application initializes handler and displays formatted errors
 * - pyodide-worker.js: Provides Pyodide instance and executes Python error formatting
 * - executor.js: Catches timeouts and worker crashes
 * - validator.js: Pre-validates code and provides validation errors
 *
 * DESIGN PRINCIPLES:
 * 1. Never use punishment language for security errors
 * 2. Frame restrictions as helpful limits
 * 3. Always suggest alternatives or fixes
 * 4. Show code context when possible
 * 5. Match curriculum level (beginner-friendly vocabulary)
 *
 * @module errorHandler
 * @see /home/jonas/git/sketchpy/plans/errors.md - Complete implementation plan
 */

export class PyodideErrorHandler {
    /**
     * Creates a new error handler
     *
     * @param {Object} pyodide - Pyodide instance from the web worker
     */
    constructor(pyodide) {
        this.pyodide = pyodide;
    }

    /**
     * Initializes Python error formatting functions
     *
     * Sets up Python code in Pyodide to extract error information from tracebacks.
     * Filters out internal Pyodide frames to show only user code errors.
     *
     * Call this once after Pyodide is loaded and before running any user code.
     *
     * @returns {Promise<void>}
     *
     * @example
     * const handler = new PyodideErrorHandler(pyodide);
     * await handler.init();
     */
    async init() {
        await this.pyodide.runPythonAsync(`
            import sys
            from traceback import extract_tb

            def get_error_info():
                """Extract user-friendly error information from Python exceptions"""
                if not hasattr(sys, 'last_type'):
                    return None

                exc_type = sys.last_type
                exc_value = sys.last_value
                exc_tb = sys.last_traceback

                # Get all frames from traceback
                tb_list = extract_tb(exc_tb) if exc_tb else []

                # For beginners: ONLY show errors in user code (<exec>), hide all Pyodide internals
                # User code appears as '<exec>' in the traceback
                user_frames = [f for f in tb_list if '<exec>' in f.filename]

                # Take the LAST <exec> frame (where error actually occurred in user code)
                # This is almost always the last item for beginners unless they create functions
                line_no = user_frames[-1].lineno if user_frames else None

                return {
                    'type': exc_type.__name__,
                    'message': str(exc_value),
                    'line': line_no
                }
        `);
    }

    /**
     * Main entry point for handling Python execution errors
     *
     * Extracts error information from Python and transforms it into a beginner-friendly format.
     *
     * @param {Error} error - The JavaScript error object from Pyodide
     * @param {string} userCode - The code that caused the error (for context snippets)
     * @returns {Promise<Object>} Formatted error object
     *
     * @example
     * try {
     *   await pyodide.runPythonAsync(userCode);
     * } catch (error) {
     *   const friendly = await handler.handleError(error, userCode);
     *   displayError(friendly);
     * }
     */
    async handleError(error, userCode) {
        try {
            const info = this.pyodide.globals.get("get_error_info")();
            if (!info) return this.formatGenericError(error);

            const data = info.toJs();
            return this.formatForBeginners(data, userCode);
        } catch (e) {
            // If error extraction fails, fall back to generic error
            return this.formatGenericError(error);
        }
    }

    /**
     * Transforms Python error data into beginner-friendly format
     *
     * Takes raw error information and creates a structured error object with:
     * - Friendly title
     * - Clear explanation
     * - Actionable hint
     * - Code snippet showing the problem
     * - Category for styling
     *
     * @param {Object} errorData - Error data from Python (type, message, line)
     * @param {string} code - User's code for extracting snippets
     * @returns {Object} Formatted error with title, explanation, hint, line, snippet, category
     *
     * @example
     * // Input: { type: 'NameError', message: "name 'x' is not defined", line: 3 }
     * // Output: {
     * //   title: 'Variable Not Found',
     * //   explanation: "You used x but haven't created it yet.",
     * //   hint: 'Try adding: x = ... before using it',
     * //   line: 3,
     * //   snippet: [...],
     * //   category: 'python'
     * // }
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
     * Gets beginner-friendly error title based on error type
     *
     * @param {string} type - Python error type (e.g., 'SyntaxError', 'NameError')
     * @returns {string} Short, friendly title
     */
    getTitle(type) {
        const titles = {
            // Python errors
            'SyntaxError': 'Syntax Problem',
            'NameError': 'Variable Not Found',
            'TypeError': 'Wrong Type',
            'IndentationError': 'Indentation Problem',
            'IndexError': 'List Index Problem',
            'AttributeError': 'Attribute Not Found',
            'ZeroDivisionError': 'Division by Zero',
            'KeyError': 'Dictionary Key Not Found',

            // Security errors
            'ValidationError': 'Code Not Allowed',
            'TimeoutError': 'Code Taking Too Long',
            'ImportError': 'Import Not Allowed',
            'ValueError': 'Invalid Value',

            // System errors
            'WorkerError': 'System Problem'
        };
        return titles[type] || 'Error';
    }

    /**
     * Gets clear explanation of what went wrong
     *
     * Uses pattern matching on error messages to provide context-specific explanations.
     * Avoids technical jargon and uses beginner-friendly language.
     *
     * @param {string} type - Python error type
     * @param {string} message - Error message from Python
     * @returns {string} Clear explanation of the problem
     */
    getExplanation(type, message) {
        // Python errors
        if (type === 'SyntaxError') {
            if (message.includes('EOL') || message.includes('EOF')) {
                return 'Python doesn\'t understand this code. You might have an unclosed quote or bracket.';
            }
            if (message.includes('invalid syntax')) {
                return 'Python doesn\'t understand this code. Check for missing colons, quotes, or brackets.';
            }
            return 'Python doesn\'t understand this code. Check your syntax carefully.';
        }

        if (type === 'NameError') {
            const match = message.match(/name '(\w+)' is not defined/);
            const varName = match ? match[1] : 'this variable';
            return `You used ${varName} but haven't created it yet.`;
        }

        if (type === 'TypeError') {
            if (message.includes('argument')) {
                return 'You\'re calling a function with the wrong number or type of arguments.';
            }
            if (message.includes('unsupported operand')) {
                return 'You\'re trying to use values in a way that doesn\'t work together (like adding text to a number).';
            }
            return 'You\'re trying to use values in a way that doesn\'t work together.';
        }

        if (type === 'IndentationError') {
            return 'The spacing at the start of this line is wrong. Code in loops and functions must be indented.';
        }

        if (type === 'IndexError') {
            return 'You tried to access an item that doesn\'t exist in your list.';
        }

        if (type === 'AttributeError') {
            return 'You tried to use a method or property that doesn\'t exist on this object.';
        }

        if (type === 'ZeroDivisionError') {
            return 'You tried to divide by zero, which isn\'t allowed in math.';
        }

        if (type === 'KeyError') {
            return 'You tried to access a dictionary key that doesn\'t exist.';
        }

        // Security errors
        if (type === 'TimeoutError' || message.includes('timeout')) {
            return 'Your code is taking too long to run. It might have an infinite loop or too many shapes.';
        }

        if (type === 'ImportError' && message.includes('not allowed')) {
            return 'This import is not available in the drawing environment.';
        }

        if (type === 'ValidationError') {
            return 'This code uses features that aren\'t allowed for safety reasons.';
        }

        // Canvas size errors
        if (type === 'ValueError' && message.includes('Canvas')) {
            if (message.includes('width') && message.includes('exceeds maximum')) {
                return 'Your canvas is too wide. The maximum width is 2000 pixels.';
            }
            if (message.includes('height') && message.includes('exceeds maximum')) {
                return 'Your canvas is too tall. The maximum height is 2000 pixels.';
            }
            if (message.includes('area') && message.includes('exceeds maximum')) {
                return 'Your canvas is too large overall. Try smaller dimensions.';
            }
            return 'Your canvas size is too large. Try using smaller dimensions.';
        }

        // Shape limit errors
        if (message.includes('Shape limit exceeded')) {
            const match = message.match(/\((\d+)\)/);
            const limit = match ? match[1] : '10,000';
            return `You're trying to draw too many shapes (limit is ${limit.toLocaleString()}). This can crash the browser.`;
        }

        // Default to original message if no specific explanation
        return message;
    }

    /**
     * Gets actionable hint for fixing the error
     *
     * Provides specific suggestions based on the error type and message.
     * Returns null if no specific hint is available.
     *
     * @param {string} type - Python error type
     * @param {string} message - Error message from Python
     * @returns {string|null} Actionable hint or null
     */
    getHint(type, message) {
        // Python error hints
        if (type === 'NameError') {
            const match = message.match(/name '(\w+)' is not defined/);
            if (match) {
                return `Try adding: ${match[1]} = ... before using it`;
            }
            return 'Make sure to define your variables before using them';
        }

        if (type === 'SyntaxError') {
            if (message.includes('EOL')) {
                return 'Did you forget to close a quote?';
            }
            if (message.includes('EOF')) {
                return 'Did you forget to close a bracket or parenthesis?';
            }
            if (message.includes('expected \':\'')) {
                return 'Did you forget a colon (:) at the end of the line?';
            }
            return 'Check for missing colons, quotes, or brackets';
        }

        if (type === 'IndentationError') {
            return 'Make sure all lines at the same level have the same spacing (usually 4 spaces)';
        }

        if (type === 'IndexError') {
            return 'Remember: lists start counting at 0. Check if your index is too large.';
        }

        if (type === 'TypeError' && message.includes('argument')) {
            return 'Check that you\'re passing the right number of values to the function';
        }

        if (type === 'ZeroDivisionError') {
            return 'Make sure the number you\'re dividing by is not zero';
        }

        // Security error hints
        if (type === 'TimeoutError' || message.includes('timeout')) {
            return 'Try: Use smaller numbers in range(), reduce loop iterations, or simplify your drawing';
        }

        if (type === 'ImportError' && message.includes('not allowed')) {
            const match = message.match(/Import '(\w+)' not allowed/);
            if (match) {
                return `Only Canvas and Color can be imported. Remove: import ${match[1]}`;
            }
            return 'Only Canvas and Color imports are available in this environment';
        }

        if (message.includes('Canvas width') || message.includes('Canvas height')) {
            return 'Try: Canvas(800, 600) - Maximum size is 2000×2000 pixels';
        }

        if (message.includes('Canvas area')) {
            return 'Try using smaller dimensions like Canvas(800, 600)';
        }

        if (message.includes('Shape limit')) {
            return 'Try: Reduce your range() number or use fewer drawing commands';
        }

        if (message.includes('Forbidden pattern')) {
            return 'This code uses advanced features not available in the learning environment';
        }

        return null;
    }

    /**
     * Extracts code snippet showing the problem line and context
     *
     * Returns an array of line objects with line numbers, code, and error flag.
     * Shows a few lines before and after the error for context.
     *
     * @param {string} code - The full user code
     * @param {number} lineNumber - Line number where error occurred (1-indexed)
     * @param {number} context - Number of lines to show before/after (default: 2)
     * @returns {Array|null} Array of {number, code, isError} objects or null
     *
     * @example
     * // For error on line 3 in:
     * // 1: can = Canvas(800, 600)
     * // 2: for i in range(5):
     * // 3:     can.rect(x, y, 50, 50)
     * //
     * // Returns:
     * // [
     * //   { number: 1, code: 'can = Canvas(800, 600)', isError: false },
     * //   { number: 2, code: 'for i in range(5):', isError: false },
     * //   { number: 3, code: '    can.rect(x, y, 50, 50)', isError: true }
     * // ]
     */
    getSnippet(code, lineNumber, context = 2) {
        if (!code || !lineNumber) return null;

        const lines = code.split('\n');
        const start = Math.max(0, lineNumber - context - 1);
        const end = Math.min(lines.length, lineNumber + context);

        return lines.slice(start, end).map((line, idx) => ({
            number: start + idx + 1,
            code: line,
            isError: start + idx + 1 === lineNumber
        }));
    }

    /**
     * Determines error category for styling purposes
     *
     * Categories determine the color theme in the UI:
     * - python: Orange/Yellow theme (learning opportunity)
     * - security: Blue theme (informative, not punitive)
     * - timeout: Purple theme (performance issue)
     * - system: Gray theme (technical problem)
     *
     * @param {string} type - Python error type
     * @param {string} message - Error message
     * @returns {string} Category name
     */
    getCategory(type, message) {
        // Security and validation errors
        if (type === 'ValidationError' ||
            type === 'ImportError' ||
            message.includes('not allowed') ||
            message.includes('Canvas width') ||
            message.includes('Canvas height') ||
            message.includes('Canvas area') ||
            message.includes('Shape limit')) {
            return 'security';
        }

        // Timeout errors
        if (type === 'TimeoutError' || message.includes('timeout')) {
            return 'timeout';
        }

        // System errors
        if (type === 'WorkerError') {
            return 'system';
        }

        // Default to python error
        return 'python';
    }

    /**
     * Formats pre-validation errors from validator.js
     *
     * These errors are caught BEFORE code execution by the client-side validator.
     * Includes: forbidden imports, canvas size checks, suspicious patterns.
     *
     * @param {Array<string>} errors - Array of validation error messages
     * @returns {Object} Formatted error object
     *
     * @example
     * // Input: ['Import "os" not allowed']
     * // Output: {
     * //   title: 'Code Not Allowed',
     * //   explanation: 'Only Canvas and Color can be imported...',
     * //   hint: 'Remove the import line...',
     * //   category: 'security'
     * // }
     */
    formatValidationError(errors) {
        const firstError = errors[0];

        return {
            title: 'Code Not Allowed',
            explanation: this.getSecurityExplanation(firstError),
            hint: this.getSecurityHint(firstError),
            line: this.extractLineNumber(firstError),
            snippet: null,
            category: 'security'
        };
    }

    /**
     * Formats timeout errors from executor.js
     *
     * Timeout errors occur when code runs longer than 5 seconds.
     * Common causes: infinite loops, too many iterations.
     *
     * @param {Error} error - Timeout error from executor
     * @returns {Object} Formatted error object
     */
    formatTimeoutError(error) {
        return {
            title: 'Code Taking Too Long',
            explanation: 'Your code ran for more than 5 seconds. It might have an infinite loop or be drawing too many shapes.',
            hint: 'Try: Reduce range() numbers, simplify your loops, or draw fewer shapes',
            line: null,
            snippet: null,
            category: 'timeout'
        };
    }

    /**
     * Formats system errors (worker crashes, etc.)
     *
     * System errors indicate problems with the execution environment,
     * not the student's code.
     *
     * @param {Error} error - System error
     * @returns {Object} Formatted error object
     */
    formatSystemError(error) {
        return {
            title: 'System Problem',
            explanation: 'Something went wrong with the code runner. Try running your code again.',
            hint: 'If this keeps happening, try refreshing the page',
            line: null,
            snippet: null,
            category: 'system'
        };
    }

    /**
     * Gets security-specific explanation for validation errors
     *
     * Uses friendly, informative language. Frames restrictions as helpful limits,
     * not punishment.
     *
     * @param {string} errorMessage - Validation error message
     * @returns {string} Beginner-friendly explanation
     */
    getSecurityExplanation(errorMessage) {
        if (errorMessage.includes('Import')) {
            return 'Only Canvas and Color can be imported in this environment.';
        }
        if (errorMessage.includes('Canvas')) {
            return 'Canvas size is too large. Maximum size is 2000×2000 pixels.';
        }
        if (errorMessage.includes('large number')) {
            return 'You\'re using very large numbers that might slow down or crash the browser.';
        }
        if (errorMessage.includes('Forbidden pattern')) {
            return 'This code uses features that aren\'t available for safety reasons.';
        }
        return 'This code cannot be run in the learning environment.';
    }

    /**
     * Gets security-specific hint for validation errors
     *
     * Suggests alternatives and provides concrete examples.
     *
     * @param {string} errorMessage - Validation error message
     * @returns {string|null} Actionable hint or null
     */
    getSecurityHint(errorMessage) {
        if (errorMessage.includes('Canvas width') || errorMessage.includes('Canvas height')) {
            return 'Try: Canvas(800, 600) instead';
        }
        if (errorMessage.includes('Import') && errorMessage.includes('not allowed')) {
            return 'Remove the import line - Canvas and Color are already available';
        }
        if (errorMessage.includes('large number')) {
            return 'Use smaller numbers in range() - try range(100) instead of range(1000000)';
        }
        return null;
    }

    /**
     * Extracts line number from error message
     *
     * Tries to find line number in validation error messages.
     *
     * @param {string} errorMessage - Error message that might contain line number
     * @returns {number|null} Line number or null
     */
    extractLineNumber(errorMessage) {
        const match = errorMessage.match(/line (\d+)/i);
        return match ? parseInt(match[1]) : null;
    }

    /**
     * Fallback formatter for unexpected errors
     *
     * Used when error extraction fails or error type is unknown.
     *
     * @param {Error} error - Generic error object
     * @returns {Object} Basic formatted error object
     */
    formatGenericError(error) {
        return {
            title: 'Something Went Wrong',
            explanation: error.message || 'An unexpected error occurred.',
            hint: 'Try refreshing the page or simplifying your code',
            line: null,
            snippet: null,
            category: 'system'
        };
    }
}
