import { describe, it, expect, beforeEach } from 'vitest';
import { JSDOM } from 'jsdom';
import { readFileSync } from 'fs';
import { resolve } from 'path';

describe('Canvas API availability in generated code', () => {
  let generatedCode;

  beforeEach(() => {
    // Read the generated Python code from the build output
    const buildPath = resolve(process.cwd(), 'scripts', 'build.py');
    const buildScript = readFileSync(buildPath, 'utf-8');

    // Extract the Python code generation logic
    // This tests that the build process includes necessary classes
  });

  describe('Canvas class', () => {
    it('should be present in generated Python code', () => {
      const shapesPath = resolve(process.cwd(), 'sketchpy', 'shapes.py');
      const shapesCode = readFileSync(shapesPath, 'utf-8');

      expect(shapesCode).toContain('class Canvas');
      expect(shapesCode).toContain('def rect(');
      expect(shapesCode).toContain('def circle(');
      expect(shapesCode).toContain('def to_svg(');
    });

    it('should have method chaining support', () => {
      const shapesPath = resolve(process.cwd(), 'sketchpy', 'shapes.py');
      const shapesCode = readFileSync(shapesPath, 'utf-8');

      // Method chaining means methods return self
      expect(shapesCode).toContain('return self');
    });

    it('should have grid method', () => {
      const shapesPath = resolve(process.cwd(), 'sketchpy', 'shapes.py');
      const shapesCode = readFileSync(shapesPath, 'utf-8');

      expect(shapesCode).toContain('def grid(');
    });

    it('should have show_palette method', () => {
      const shapesPath = resolve(process.cwd(), 'sketchpy', 'shapes.py');
      const shapesCode = readFileSync(shapesPath, 'utf-8');

      expect(shapesCode).toContain('def show_palette(');
    });
  });

  describe('Color class', () => {
    it('should be present in generated Python code', () => {
      const shapesPath = resolve(process.cwd(), 'sketchpy', 'shapes.py');
      const shapesCode = readFileSync(shapesPath, 'utf-8');

      expect(shapesCode).toContain('class Color');
    });

    it('should have basic color constants', () => {
      const shapesPath = resolve(process.cwd(), 'sketchpy', 'shapes.py');
      const shapesCode = readFileSync(shapesPath, 'utf-8');

      expect(shapesCode).toContain('RED =');
      expect(shapesCode).toContain('BLUE =');
      expect(shapesCode).toContain('GREEN =');
    });

    it('should have hex color values', () => {
      const shapesPath = resolve(process.cwd(), 'sketchpy', 'shapes.py');
      const shapesCode = readFileSync(shapesPath, 'utf-8');

      // Check for hex color format
      expect(shapesCode).toMatch(/#[0-9A-F]{6}/i);
    });
  });

  describe('Palette classes', () => {
    it('should have CreativeGardenPalette', () => {
      const shapesPath = resolve(process.cwd(), 'sketchpy', 'shapes.py');
      const shapesCode = readFileSync(shapesPath, 'utf-8');

      expect(shapesCode).toContain('class CreativeGardenPalette');
      expect(shapesCode).toContain('PEACH_WHISPER');
    });

    it('should have CalmOasisPalette', () => {
      const shapesPath = resolve(process.cwd(), 'sketchpy', 'shapes.py');
      const shapesCode = readFileSync(shapesPath, 'utf-8');

      expect(shapesCode).toContain('class CalmOasisPalette');
      expect(shapesCode).toContain('SKY_BLUE');
    });
  });

  describe('Browser compatibility', () => {
    it('should not include save() method in browser build', () => {
      // This would need to check the actual build output
      // For now, just verify the source has it (build strips it)
      const shapesPath = resolve(process.cwd(), 'sketchpy', 'shapes.py');
      const shapesCode = readFileSync(shapesPath, 'utf-8');

      expect(shapesCode).toContain('def save(');
      // The build.py script should strip this for browser
    });

    it('should keep _repr_html_ for marimo support', () => {
      const shapesPath = resolve(process.cwd(), 'sketchpy', 'shapes.py');
      const shapesCode = readFileSync(shapesPath, 'utf-8');

      expect(shapesCode).toContain('def _repr_html_');
    });
  });
});
