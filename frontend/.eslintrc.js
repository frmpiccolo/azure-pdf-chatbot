module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
  },
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  plugins: ['react', '@typescript-eslint', 'prettier'],
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:prettier/recommended',
    'prettier',
  ],
  rules: {
    'react/react-in-jsx-scope': 'off',
    quotes: ['error', 'single'], // ⬅️ Reforça aspas simples
    'prettier/prettier': [
      'error',
      {
        singleQuote: true, // ⬅️ Essencial para Prettier seguir o padrão
        trailingComma: 'es5',
        tabWidth: 2,
        semi: false, // opcional: remove ponto e vírgula
      },
    ],
    '@typescript-eslint/no-unused-vars': [
      'error',
      {
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_',
      },
    ],
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
}
