import { SecurityConfig } from './config.js';

/**
 * Client-side validation before code execution
 * Fast-fail checks to prevent obviously malicious code
 */
export class CodeValidator {

    /**
     * Validate Python code before execution
     * @param {string} code - Python code to validate
     * @returns {{valid: boolean, errors: string[]}}
     */
    static validate(code) {
        const errors = [];

        // Check 1: Length limit
        if (code.length > SecurityConfig.MAX_CODE_LENGTH) {
            errors.push(
                `Code too long: ${code.length} chars ` +
                `(max ${SecurityConfig.MAX_CODE_LENGTH})`
            );
        }

        // Check 2: Empty code
        if (code.trim().length === 0) {
            errors.push('Code is empty');
        }

        // Check 3: Forbidden patterns
        for (const pattern of SecurityConfig.FORBIDDEN_PATTERNS) {
            if (pattern.test(code)) {
                errors.push(`Forbidden pattern detected: ${pattern.source}`);
            }
        }

        // Check 4: Import whitelist (simple regex check)
        const importRegex = /(?:from\s+(\w+)|import\s+(\w+))/g;
        let match;
        const foundImports = new Set();

        while ((match = importRegex.exec(code)) !== null) {
            const moduleName = match[1] || match[2];
            foundImports.add(moduleName);

            if (!SecurityConfig.ALLOWED_IMPORTS.has(moduleName)) {
                errors.push(`Import '${moduleName}' not allowed. ` +
                           `Allowed imports: ${Array.from(SecurityConfig.ALLOWED_IMPORTS).join(', ')}`);
            }
        }

        // Check 5: Suspicious large numbers (DoS prevention)
        const largeNumberRegex = /\b\d{7,}\b/; // 7+ digits
        if (largeNumberRegex.test(code)) {
            errors.push('Suspicious large number detected (possible DoS attempt)');
        }

        // Check 6: Canvas size check (simple pattern match)
        const canvasRegex = /Canvas\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)/g;
        while ((match = canvasRegex.exec(code)) !== null) {
            const width = parseInt(match[1]);
            const height = parseInt(match[2]);

            if (width > SecurityConfig.MAX_CANVAS_WIDTH) {
                errors.push(`Canvas width ${width} exceeds max ${SecurityConfig.MAX_CANVAS_WIDTH}`);
            }
            if (height > SecurityConfig.MAX_CANVAS_HEIGHT) {
                errors.push(`Canvas height ${height} exceeds max ${SecurityConfig.MAX_CANVAS_HEIGHT}`);
            }
            if (width * height > SecurityConfig.MAX_CANVAS_AREA) {
                errors.push(`Canvas area ${width * height} exceeds max ${SecurityConfig.MAX_CANVAS_AREA}`);
            }
        }

        return {
            valid: errors.length === 0,
            errors: errors
        };
    }

    /**
     * Get friendly error message for display
     */
    static formatErrors(errors) {
        if (errors.length === 0) return '';

        return '❌ Security Validation Failed:\n\n' +
               errors.map((e, i) => `${i + 1}. ${e}`).join('\n');
    }
}
