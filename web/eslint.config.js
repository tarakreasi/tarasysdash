
import js from '@eslint/js';
import globals from 'globals';
import tseslint from 'typescript-eslint';
import pluginVue from 'eslint-plugin-vue';

export default [
    {
        ignores: ["dist/**", "node_modules/**", "coverage/**", "*.config.js", "*.config.ts"]
    },
    {
        files: ['src/**/*.{js,mjs,cjs,ts,vue}']
    },
    { languageOptions: { globals: { ...globals.browser, ...globals.node } } },
    js.configs.recommended,
    ...tseslint.configs.recommended,
    ...pluginVue.configs['flat/essential'],
    { files: ["**/*.vue"], languageOptions: { parserOptions: { parser: tseslint.parser } } },
    {
        rules: {
            'vue/multi-word-component-names': 'off',
            '@typescript-eslint/no-explicit-any': 'off',
            'no-console': 'warn',
            'no-debugger': 'warn'
        }
    }
];
