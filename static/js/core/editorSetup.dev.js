/**
 * CodeMirror 6 editor initialization and configuration
 *
 * This module sets up the Python code editor with:
 * - Syntax highlighting
 * - Autocomplete for Canvas/Color API
 * - Keyboard shortcuts (Ctrl/Cmd-Enter to run)
 * - Dark theme
 *
 * @module editorSetup
 */

import { buildApiDefinitions, GENERAL_KEYWORDS } from './apiDefinitions.dev.js';

/**
 * Smart completion function that detects object.method patterns
 *
 * Provides context-aware autocomplete:
 * - After "can." → Canvas methods (circle, rect, etc.)
 * - After "Color." → Color constants (RED, BLUE, etc.)
 * - After "CreativeGardenPalette." → Palette colors
 * - After "CalmOasisPalette." → Palette colors
 * - Otherwise → General keywords (Canvas, Color, palette classes)
 *
 * @param {Object} context - CodeMirror completion context
 * @param {Object} apiDefinitions - API definitions from buildApiDefinitions()
 * @returns {Object|null} Completion result with options array
 */
function smartPythonCompletions(context, apiDefinitions) {
    // Get text before cursor
    const before = context.matchBefore(/\w+\.\w*/);

    // Check if we're typing after a dot (e.g., "can.circle")
    if (before) {
        const text = before.text;
        const dotIndex = text.lastIndexOf('.');

        if (dotIndex > 0) {
            // Extract object name
            const objectName = text.substring(0, dotIndex);

            // Look up methods for this object
            if (apiDefinitions[objectName]) {
                const methods = apiDefinitions[objectName];

                return {
                    from: before.from + dotIndex + 1,
                    options: methods,
                    validFor: /^\w*$/
                };
            }
        }
    }

    // Otherwise, check for regular word completion
    const word = context.matchBefore(/\w*/);
    if (!word || (word.from == word.to && !context.explicit))
        return null;

    return {
        from: word.from,
        options: GENERAL_KEYWORDS,
        validFor: /^\w*$/
    };
}

/**
 * Initialize CodeMirror 6 editor
 *
 * Creates and configures the code editor with Python support, autocomplete,
 * and keyboard shortcuts.
 *
 * @param {string} initialCode - Initial code to display in the editor
 * @param {Function} onRun - Callback to run when Ctrl/Cmd-Enter is pressed
 * @returns {Object} EditorView instance
 *
 * @example
 * import { initEditor } from './core/editorSetup.js';
 *
 * const editor = initEditor(
 *   'can = Canvas(800, 600)\ncan',
 *   () => window.runCode()
 * );
 */
export async function initEditor(initialCode, onRun) {
    // Import CodeMirror from CDN (using import maps defined in template)
    const { EditorView, basicSetup } = await import("codemirror");
    const { python } = await import("@codemirror/lang-python");
    const { oneDark } = await import("@codemirror/theme-one-dark");
    const { autocompletion } = await import("@codemirror/autocomplete");
    const { keymap } = await import("@codemirror/view");
    const { Prec } = await import("@codemirror/state");

    // Build API definitions from embedded shapes code
    const apiDefinitions = buildApiDefinitions(window.SHAPES_CODE);

    // Store globally for access by other modules if needed
    window.API_DEFINITIONS = apiDefinitions;

    // Create editor with all extensions
    const editor = new EditorView({
        doc: initialCode,
        extensions: [
            basicSetup,
            python(),
            oneDark,

            // Autocompletion with custom source
            autocompletion({
                override: [(context) => smartPythonCompletions(context, apiDefinitions)],
                defaultKeymap: true
            }),

            EditorView.lineWrapping,

            // Add keyboard shortcuts with highest precedence (Mod-Enter = Cmd-Enter on Mac, Ctrl-Enter on Windows/Linux)
            Prec.highest(keymap.of([
                {
                    key: 'Mod-Enter',
                    run: () => {
                        onRun();
                        return true;
                    }
                }
            ]))
        ],
        parent: document.querySelector('.editor-container')
    });

    return editor;
}
