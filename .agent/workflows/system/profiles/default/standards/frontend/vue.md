# Vue Framework Standards

## Core Stack
- **Version**: Vue 3.5+.
- **Language**: TypeScript (`.ts`, `.vue`).
- **API Style**: Composition API with `<script setup lang="ts">`.

## Vapor Mode
- **Status**: Enabled/Experimental.
- **Config**: Vite Plugin `vue()` configured with optimization enabled.
- **Fallback**: Maintain standard Vue DOM compatibility if Vapor features fail.

## Typing
- **Explicit Types**: Use `defineProps<{ ... }>()` and `defineEmits<{ ... }>()`.
- **Global Types**: Define shared types in `resources/js/types/`.
- **Check**: `vue-tsc` must pass.

## Linting
- **Engine**: ESLint + Prettier.
- **Rules**:
    - `vue/multi-word-component-names`: Disabled for `Pages/`.
    - Strict TS checks enabled.
