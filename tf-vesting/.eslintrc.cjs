module.exports = {
  parser: '@typescript-eslint/parser',
  plugins: [ '@typescript-eslint', 'svelte3' ],
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier',
  ],
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: 'module',
  },
  env: {
    browser: true,
    node: true,
  },
  overrides: [
    {
      files: [ '*.svelte' ],
      processor: 'svelte3/svelte3',
    },
  ],
  settings: {
    'svelte3/typescript': true,
  },
  'rules': {
    // enforce the use of semicolons
    'semi': [ 'error', 'always' ],
    // enforce the use of single quotes
    'quotes': [ 'error', 'single' ],
    // disallow the use of alert, prompt and confirm
    'no-alert': 'error',
    // enforce a maximum line length
    'max-len': [ 'error', { 'code': 120, 'ignoreRegExpLiterals': true } ],
    // enforce consistent indentation
    'indent': [ 'error', 2 ],
    // disallow the use of var
    'no-var': 'error',
    // enforce the use of const and let
    'prefer-const': 'error',
    'no-explicit-any': 'off'
  }
};
