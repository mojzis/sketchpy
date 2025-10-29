import { describe, it, expect } from 'vitest';
import { buildApiDefinitions, GENERAL_KEYWORDS } from '../../static/js/core/apiDefinitions.dev.js';

describe('API Definitions Builder', () => {
  const mockShapesCode = `
class Color:
    RED = "#FF0000"
    BLUE = "#0000FF"
    GREEN = "#00FF00"

class CreativeGardenPalette:
    PEACH_WHISPER = "#FFDAC1"
    ROSE_QUARTZ = "#FFCAD4"

class CalmOasisPalette:
    SKY_BLUE = "#87CEEB"
    MINT_FRESH = "#98FF98"

class Canvas:
    def circle(self, x, y, radius, fill=None):
        pass
  `;

  describe('buildApiDefinitions()', () => {
    it('extracts Color constants', () => {
      const api = buildApiDefinitions(mockShapesCode);

      expect(api.Color).toBeDefined();
      expect(api.Color).toContainEqual({
        label: 'RED',
        type: 'constant',
        apply: 'RED',
        info: 'Color constant',
      });
      expect(api.Color).toHaveLength(3);
    });

    it('extracts CreativeGardenPalette constants', () => {
      const api = buildApiDefinitions(mockShapesCode);

      expect(api.CreativeGardenPalette).toBeDefined();
      expect(api.CreativeGardenPalette).toContainEqual({
        label: 'PEACH_WHISPER',
        type: 'constant',
        apply: 'PEACH_WHISPER',
        info: 'CreativeGardenPalette color',
      });
      expect(api.CreativeGardenPalette).toHaveLength(2);
    });

    it('extracts CalmOasisPalette constants', () => {
      const api = buildApiDefinitions(mockShapesCode);

      expect(api.CalmOasisPalette).toBeDefined();
      expect(api.CalmOasisPalette).toContainEqual({
        label: 'SKY_BLUE',
        type: 'constant',
        apply: 'SKY_BLUE',
        info: 'CalmOasisPalette color',
      });
      expect(api.CalmOasisPalette).toHaveLength(2);
    });

    it('includes Canvas methods', () => {
      const api = buildApiDefinitions(mockShapesCode);

      expect(api.can).toBeDefined();
      const circleMethod = api.can.find(m => m.label === 'circle');
      expect(circleMethod).toBeDefined();
      expect(circleMethod.type).toBe('method');
      expect(circleMethod.detail).toContain('radius');
    });

    it('handles empty shapes code', () => {
      const api = buildApiDefinitions('');

      expect(api.can).toBeDefined(); // Canvas methods always included
      expect(api.Color).toBeUndefined(); // No Color class found
    });

    it('includes all standard Canvas methods', () => {
      const api = buildApiDefinitions('');

      const methodNames = api.can.map(m => m.label);
      expect(methodNames).toContain('circle');
      expect(methodNames).toContain('rect');
      expect(methodNames).toContain('ellipse');
      expect(methodNames).toContain('line');
      expect(methodNames).toContain('polygon');
      expect(methodNames).toContain('text');
      expect(methodNames).toContain('rounded_rect');
      expect(methodNames).toContain('grid');
      expect(methodNames).toContain('show_palette');
      expect(methodNames).toContain('to_svg');
      expect(methodNames).toContain('clear');
    });
  });

  describe('GENERAL_KEYWORDS', () => {
    it('includes Canvas class', () => {
      const canvas = GENERAL_KEYWORDS.find(k => k.label === 'Canvas');
      expect(canvas).toBeDefined();
      expect(canvas.type).toBe('class');
      expect(canvas.apply).toContain('Canvas(');
    });

    it('includes Color class', () => {
      const color = GENERAL_KEYWORDS.find(k => k.label === 'Color');
      expect(color).toBeDefined();
      expect(color.type).toBe('class');
    });

    it('includes palette classes', () => {
      const garden = GENERAL_KEYWORDS.find(k => k.label === 'CreativeGardenPalette');
      const oasis = GENERAL_KEYWORDS.find(k => k.label === 'CalmOasisPalette');

      expect(garden).toBeDefined();
      expect(oasis).toBeDefined();
      expect(garden.type).toBe('class');
      expect(oasis.type).toBe('class');
    });

    it('has correct number of keywords', () => {
      expect(GENERAL_KEYWORDS).toHaveLength(5); // Canvas, Color, CreativeGardenPalette, CalmOasisPalette, MathDoodlingPalette
    });
  });
});
