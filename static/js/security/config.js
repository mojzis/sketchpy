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
    WORKER_PATH: '/static/js/pyodide-worker.js',  // Will be adjusted at runtime
    PYODIDE_VERSION: '0.25.0',
    PYODIDE_CDN: 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/',
};
