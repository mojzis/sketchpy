import js from '@eslint/js';

export default [
  js.configs.recommended,
  {
    files: ['static/js/**/*.js'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        // Browser globals
        window: 'readonly',
        document: 'readonly',
        console: 'readonly',
        localStorage: 'readonly',
        setTimeout: 'readonly',
        clearTimeout: 'readonly',
        Worker: 'readonly',
        location: 'readonly',
        confirm: 'readonly',
        alert: 'readonly',
        importScripts: 'readonly',

        // CDN libraries
        Alpine: 'readonly',
        loadPyodide: 'readonly',

        // Template-injected globals
        SHAPES_CODE: 'readonly',
        BASE_PATH: 'readonly',
        CURRENT_LESSON: 'readonly',
        ALL_LESSONS: 'readonly',
        API_DEFINITIONS: 'writable',
      },
    },
    rules: {
      'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
      'no-console': 'off', // Educational tool, console is fine
      'no-undef': 'error',
      'prefer-const': 'warn',
    },
  },
];
