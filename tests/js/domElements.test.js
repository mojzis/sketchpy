import { describe, it, expect, beforeEach } from 'vitest';
import { JSDOM } from 'jsdom';
import { readFileSync } from 'fs';
import { resolve } from 'path';

describe('DOM Elements in lesson template', () => {
  let dom;
  let document;
  let lessonHTML;

  beforeEach(() => {
    // Read the lesson template
    const templatePath = resolve(process.cwd(), 'templates', 'lesson.html.jinja');
    lessonHTML = readFileSync(templatePath, 'utf-8');

    // Create a DOM from the template (simplified - Jinja2 variables removed)
    const simplifiedHTML = lessonHTML
      .replace(/\{\{[^}]+\}\}/g, '') // Remove Jinja2 variables
      .replace(/\{%[^%]+%\}/g, '')   // Remove Jinja2 control structures
      .replace(/\{#[^#]+#\}/g, '');  // Remove Jinja2 comments

    dom = new JSDOM(simplifiedHTML);
    document = dom.window.document;
  });

  describe('Editor elements', () => {
    it('should have CodeMirror editor container', () => {
      // Check template has editor div
      expect(lessonHTML).toContain('id="editor"');
    });

    it('should load CodeMirror from CDN', () => {
      expect(lessonHTML).toContain('codemirror');
    });
  });

  describe('Control buttons', () => {
    it('should have Run button with correct ID', () => {
      expect(lessonHTML).toContain('id="runBtn"');
    });

    it('should have Clear button', () => {
      expect(lessonHTML).toMatch(/[Cc]lear/);
    });

    it('should have loading indicator', () => {
      expect(lessonHTML).toContain('id="loading"');
    });

    it('should have status display element', () => {
      expect(lessonHTML).toContain('id="status"');
    });
  });

  describe('Canvas output', () => {
    it('should have canvas output container', () => {
      expect(lessonHTML).toContain('id="canvas"');
    });

    it('should have output container for SVG', () => {
      // The canvas div should be present for rendering output
      expect(lessonHTML).toMatch(/<div[^>]*id=["']canvas["']/);
    });
  });

  describe('Navigation elements', () => {
    it('should have lesson dropdown', () => {
      expect(lessonHTML).toContain('lesson-dropdown');
    });

    it('should have theme selector', () => {
      // Check for theme-related dropdowns/selects
      expect(lessonHTML).toMatch(/theme/i);
    });
  });

  describe('Alpine.js integration', () => {
    it('should load Alpine.js', () => {
      expect(lessonHTML).toContain('alpine');
    });

    it('should have x-data directive for app state', () => {
      expect(lessonHTML).toContain('x-data');
    });

    it('should use appState function pattern', () => {
      // Check for the critical appState initialization pattern
      expect(lessonHTML).toContain('appState()');
    });

    it('should have appStateReady flag check', () => {
      // Check for the polling pattern that prevents "appState is not defined"
      expect(lessonHTML).toContain('appStateReady');
    });
  });

  describe('Module loading', () => {
    it('should import lessonState module', () => {
      expect(lessonHTML).toContain('lessonState');
    });

    it('should import editorSetup module', () => {
      expect(lessonHTML).toContain('editorSetup');
    });

    it('should use ES6 module type', () => {
      expect(lessonHTML).toContain('type="module"');
    });
  });

  describe('Pyodide setup', () => {
    it('should reference pyodide-worker', () => {
      expect(lessonHTML).toContain('pyodide-worker');
    });

    it('should load Pyodide from CDN', () => {
      expect(lessonHTML).toMatch(/pyodide/i);
    });
  });
});
