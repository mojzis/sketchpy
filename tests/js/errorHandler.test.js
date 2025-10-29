import { describe, it, expect } from 'vitest';
import { PyodideErrorHandler } from '../../static/js/errorHandler.dev.js';

describe('PyodideErrorHandler', () => {
  // Mock Pyodide instance (we don't need real Pyodide for these tests)
  const mockPyodide = null;
  const handler = new PyodideErrorHandler(mockPyodide);

  describe('getTitle()', () => {
    it('returns friendly title for SyntaxError', () => {
      expect(handler.getTitle('SyntaxError')).toBe('Syntax Problem');
    });

    it('returns friendly title for NameError', () => {
      expect(handler.getTitle('NameError')).toBe('Variable Not Found');
    });

    it('returns friendly title for TypeError', () => {
      expect(handler.getTitle('TypeError')).toBe('Wrong Type');
    });

    it('returns generic title for unknown error', () => {
      expect(handler.getTitle('WeirdUnknownError')).toBe('Error');
    });
  });

  describe('getExplanation()', () => {
    it('explains NameError with variable name', () => {
      const explanation = handler.getExplanation(
        'NameError',
        "name 'speed' is not defined"
      );
      expect(explanation).toContain('speed');
      expect(explanation).toContain("haven't created it yet");
    });

    it('explains SyntaxError for unclosed quotes', () => {
      const explanation = handler.getExplanation(
        'SyntaxError',
        'EOL while scanning string literal'
      );
      expect(explanation).toContain('unclosed quote');
    });

    it('explains canvas size errors', () => {
      const explanation = handler.getExplanation(
        'ValueError',
        'Canvas width exceeds maximum (2000)'
      );
      expect(explanation).toContain('too wide');
      expect(explanation).toContain('2000 pixels');
    });

    it('explains shape limit errors', () => {
      const explanation = handler.getExplanation(
        'RuntimeError',
        'Shape limit exceeded (10000)'
      );
      expect(explanation).toContain('10000'); // No comma formatting
      expect(explanation).toContain('too many shapes');
    });

    it('explains IndentationError', () => {
      const explanation = handler.getExplanation(
        'IndentationError',
        'unexpected indent'
      );
      expect(explanation).toContain('spacing');
      expect(explanation).toContain('indented');
    });
  });

  describe('getHint()', () => {
    it('provides actionable hint for NameError', () => {
      const hint = handler.getHint('NameError', "name 'speed' is not defined");
      expect(hint).toContain('speed = ...');
    });

    it('provides hint for indentation errors', () => {
      const hint = handler.getHint('IndentationError', 'unexpected indent');
      expect(hint).toContain('4 spaces');
    });

    it('provides hint for SyntaxError with missing colon', () => {
      const hint = handler.getHint('SyntaxError', "expected ':'");
      expect(hint).toContain('colon');
    });

    it('provides hint for canvas size errors', () => {
      const hint = handler.getHint('ValueError', 'Canvas width exceeds maximum');
      expect(hint).toContain('Canvas(800, 600)');
    });

    it('returns null for errors without specific hints', () => {
      const hint = handler.getHint('RuntimeError', 'something weird happened');
      expect(hint).toBeNull();
    });
  });

  describe('getSnippet()', () => {
    it('extracts code snippet with context', () => {
      const code = 'line 1\nline 2\nline 3\nline 4\nline 5';
      const snippet = handler.getSnippet(code, 3);

      expect(snippet).toHaveLength(5); // 2 before, error, 2 after
      expect(snippet[2].number).toBe(3);
      expect(snippet[2].isError).toBe(true);
      expect(snippet[2].code).toBe('line 3');
    });

    it('handles error at start of file', () => {
      const code = 'line 1\nline 2\nline 3';
      const snippet = handler.getSnippet(code, 1);

      expect(snippet[0].number).toBe(1);
      expect(snippet[0].isError).toBe(true);
    });

    it('handles error at end of file', () => {
      const code = 'line 1\nline 2\nline 3';
      const snippet = handler.getSnippet(code, 3);

      const lastLine = snippet[snippet.length - 1];
      expect(lastLine.number).toBe(3);
      expect(lastLine.isError).toBe(true);
    });

    it('returns null for invalid input', () => {
      expect(handler.getSnippet(null, 5)).toBeNull();
      expect(handler.getSnippet('code', null)).toBeNull();
    });
  });

  describe('getCategory()', () => {
    it('categorizes security errors correctly', () => {
      expect(handler.getCategory('ImportError', 'import not allowed'))
        .toBe('security');
      expect(handler.getCategory('ValueError', 'Canvas width exceeds'))
        .toBe('security');
      expect(handler.getCategory('RuntimeError', 'Shape limit exceeded'))
        .toBe('security');
    });

    it('categorizes timeout errors', () => {
      expect(handler.getCategory('TimeoutError', 'took too long'))
        .toBe('timeout');
      expect(handler.getCategory('RuntimeError', 'timeout occurred'))
        .toBe('timeout');
    });

    it('categorizes Python errors', () => {
      expect(handler.getCategory('SyntaxError', 'invalid syntax'))
        .toBe('python');
      expect(handler.getCategory('NameError', 'not defined'))
        .toBe('python');
      expect(handler.getCategory('TypeError', 'wrong type'))
        .toBe('python');
    });

    it('categorizes system errors', () => {
      expect(handler.getCategory('WorkerError', 'worker crashed'))
        .toBe('system');
    });
  });

  describe('formatForBeginners()', () => {
    it('creates complete formatted error object', () => {
      const errorData = {
        type: 'NameError',
        message: "name 'speed' is not defined",
        line: 5,
      };
      const code = 'can = Canvas(800, 600)\n# line 2\n# line 3\n# line 4\nprint(speed)';

      const formatted = handler.formatForBeginners(errorData, code);

      expect(formatted).toMatchObject({
        title: 'Variable Not Found',
        category: 'python',
        line: 5,
      });
      expect(formatted.explanation).toBeTruthy();
      expect(formatted.hint).toBeTruthy();
      expect(formatted.snippet).toBeInstanceOf(Array);
    });

    it('handles errors without line numbers', () => {
      const errorData = {
        type: 'RuntimeError',
        message: 'Something went wrong',
        line: null,
      };
      const code = 'can = Canvas(800, 600)';

      const formatted = handler.formatForBeginners(errorData, code);

      expect(formatted.line).toBeNull();
      expect(formatted.snippet).toBeNull();
    });
  });

  describe('extractLineNumber()', () => {
    it('extracts line number from error message', () => {
      const msg = 'Error on line 42';
      expect(handler.extractLineNumber(msg)).toBe(42);
    });

    it('returns null when no line number found', () => {
      const msg = 'Error occurred';
      expect(handler.extractLineNumber(msg)).toBeNull();
    });
  });
});
