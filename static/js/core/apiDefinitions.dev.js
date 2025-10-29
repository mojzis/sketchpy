/**
 * API definitions builder for CodeMirror autocomplete
 *
 * This module dynamically extracts API information from the embedded Python shapes code
 * and builds autocomplete definitions for the CodeMirror editor.
 *
 * @module apiDefinitions
 */

/**
 * Builds API definitions from embedded Python shapes code
 *
 * Extracts:
 * - Canvas methods (circle, rect, ellipse, etc.)
 * - Color palette constants (RED, BLUE, GREEN, etc.)
 * - CreativeGardenPalette constants
 * - CalmOasisPalette constants
 * - MathDoodlingPalette constants
 *
 * @param {string} shapesCode - Python source code containing Canvas and Color classes
 * @returns {Object} API definitions object with keys: 'can', 'Color', 'CreativeGardenPalette', 'CalmOasisPalette', 'MathDoodlingPalette'
 *
 * @example
 * const api = buildApiDefinitions(window.SHAPES_CODE);
 * console.log(api.Color); // [{ label: 'RED', type: 'constant', ... }, ...]
 */
export function buildApiDefinitions(shapesCode) {
    const api = {};

    // Canvas methods with working example code (includes parameter names)
    api['can'] = [
        {
            label: "circle",
            type: "method",
            apply: "circle(x=100, y=100, radius=50, fill=Color.RED, opacity=1.0)",
            detail: "(x, y, radius, fill=Color.BLACK, stroke=Color.BLACK, stroke_width=1, opacity=1.0)",
            info: "Draw a circle at position (x, y) with given radius. Use opacity (0.0-1.0) for transparency."
        },
        {
            label: "rect",
            type: "method",
            apply: "rect(x=100, y=100, width=200, height=150, fill=Color.BLUE)",
            detail: "(x, y, width, height, fill=None, outline=None)",
            info: "Draw a rectangle"
        },
        {
            label: "ellipse",
            type: "method",
            apply: "ellipse(x=200, y=150, width=100, height=60, fill=Color.GREEN)",
            detail: "(x, y, width, height, fill=None, outline=None)",
            info: "Draw an ellipse"
        },
        {
            label: "line",
            type: "method",
            apply: "line(x1=50, y1=50, x2=200, y2=200, color=Color.BLACK, width=2)",
            detail: "(x1, y1, x2, y2, color=None, width=1)",
            info: "Draw a line between two points"
        },
        {
            label: "polygon",
            type: "method",
            apply: "polygon(points=[(100, 100), (200, 100), (150, 200)], fill=Color.PURPLE)",
            detail: "(points, fill=None, outline=None)",
            info: "Draw a polygon from a list of points"
        },
        {
            label: "text",
            type: "method",
            apply: "text(x=100, y=100, text=\"Hello!\", font_size=24, color=Color.BLACK)",
            detail: "(x, y, text, font_size=12, color=None)",
            info: "Draw text at position (x, y)"
        },
        {
            label: "rounded_rect",
            type: "method",
            apply: "rounded_rect(x=100, y=100, width=200, height=150, radius=15, fill=Color.ORANGE)",
            detail: "(x, y, width, height, radius, fill=None, outline=None)",
            info: "Draw a rectangle with rounded corners"
        },
        {
            label: "grid",
            type: "method",
            apply: "grid(spacing=50, show_coords=True)",
            detail: "(spacing=50, color='#E8E8E8', show_coords=False)",
            info: "Draw a coordinate grid with optional labels"
        },
        {
            label: "show_palette",
            type: "method",
            apply: "show_palette(palette_class=CreativeGardenPalette)",
            detail: "(palette_class, columns=4, rect_width=120, rect_height=40, padding=10)",
            info: "Display all colors from a palette class"
        },
        { label: "to_svg", type: "method", apply: "to_svg()", detail: "()", info: "Return SVG string representation" },
        { label: "clear", type: "method", apply: "clear()", detail: "()", info: "Clear the canvas" }
    ];

    let match;

    // Extract Color class constants
    const colorRegex = /class\s+Color:[\s\S]*?(?=\n(?:class|def|$))/;
    const colorMatch = shapesCode.match(colorRegex);
    if (colorMatch) {
        const colorCode = colorMatch[0];
        const colorConstRegex = /(\w+)\s*=\s*["']#[0-9A-Fa-f]{6}["']/g;
        const colors = [];
        while ((match = colorConstRegex.exec(colorCode)) !== null) {
            colors.push({
                label: match[1],
                type: "constant",
                apply: match[1],
                info: `Color constant`
            });
        }
        api['Color'] = colors;
    }

    // Extract CreativeGardenPalette constants
    const gardenRegex = /class\s+CreativeGardenPalette:[\s\S]*?(?=\n(?:class|def|$))/;
    const gardenMatch = shapesCode.match(gardenRegex);
    if (gardenMatch) {
        const gardenCode = gardenMatch[0];
        const gardenConstRegex = /(\w+)\s*=\s*["']#[0-9A-Fa-f]{6}["']/g;
        const gardenColors = [];
        while ((match = gardenConstRegex.exec(gardenCode)) !== null) {
            gardenColors.push({
                label: match[1],
                type: "constant",
                apply: match[1],
                info: `CreativeGardenPalette color`
            });
        }
        api['CreativeGardenPalette'] = gardenColors;
    }

    // Extract CalmOasisPalette constants
    const oasisRegex = /class\s+CalmOasisPalette:[\s\S]*?(?=\n(?:class|def|$))/;
    const oasisMatch = shapesCode.match(oasisRegex);
    if (oasisMatch) {
        const oasisCode = oasisMatch[0];
        const oasisConstRegex = /(\w+)\s*=\s*["']#[0-9A-Fa-f]{6}["']/g;
        const oasisColors = [];
        while ((match = oasisConstRegex.exec(oasisCode)) !== null) {
            oasisColors.push({
                label: match[1],
                type: "constant",
                apply: match[1],
                info: `CalmOasisPalette color`
            });
        }
        api['CalmOasisPalette'] = oasisColors;
    }

    // Extract MathDoodlingPalette constants
    const mathDoodlingRegex = /class\s+MathDoodlingPalette:[\s\S]*?(?=\n(?:class|def|@dataclass|$))/;
    const mathDoodlingMatch = shapesCode.match(mathDoodlingRegex);
    if (mathDoodlingMatch) {
        const mathDoodlingCode = mathDoodlingMatch[0];
        const mathDoodlingConstRegex = /(\w+)\s*=\s*["']#[0-9A-Fa-f]{6}["']/g;
        const mathDoodlingColors = [];
        while ((match = mathDoodlingConstRegex.exec(mathDoodlingCode)) !== null) {
            mathDoodlingColors.push({
                label: match[1],
                type: "constant",
                apply: match[1],
                info: `MathDoodlingPalette color`
            });
        }
        api['MathDoodlingPalette'] = mathDoodlingColors;
    }

    return api;
}

/**
 * General keywords (classes) with working examples
 */
export const GENERAL_KEYWORDS = [
    {
        label: "Canvas",
        type: "class",
        apply: "Canvas(width=800, height=600)",
        detail: "(width, height)",
        info: "Create a new drawing canvas"
    },
    {
        label: "Color",
        type: "class",
        apply: "Color.",
        info: "Basic color palette class"
    },
    {
        label: "CreativeGardenPalette",
        type: "class",
        apply: "CreativeGardenPalette.",
        info: "Pastel color palette for creative projects"
    },
    {
        label: "CalmOasisPalette",
        type: "class",
        apply: "CalmOasisPalette.",
        info: "Calming blues and greens color palette"
    },
    {
        label: "MathDoodlingPalette",
        type: "class",
        apply: "MathDoodlingPalette.",
        info: "Triadic palette for abstract geometric patterns with transparency"
    }
];
