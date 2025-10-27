import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      include: ['static/js/**/*.js'],
      exclude: ['static/js/**/*.test.js', 'static/js/pyodide-worker.js'],
    },
  },
});
