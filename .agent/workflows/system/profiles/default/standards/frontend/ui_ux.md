# UI/UX & Styling Standards

## Styling Engine
- **Framework**: Tailwind CSS v4 (Oxide Engine).
- **Configuration**: CSS-first approach (`@import "tailwindcss";`).
- **Plugin**: `@tailwindcss/vite`.
- **Legacy**: Do NOT use `postcss.config.js` or `tailwind.config.js` (unless strictly necessary).

## Atomic Design
Directory: `resources/js/Components/`

1.  **Atoms (Base)**:
    - Prefix: `Base` (e.g., `BaseButton.vue`, `BaseInput.vue`).
    - Focus: Single responsibility, highly reusable, no business logic.

2.  **Molecules & Organisms**:
    - Directory: `Components/` (Root or grouped by feature).
    - Composition of Atoms.

## Icons & Assets
- Use SVG icons directly or via a wrapper component.
- Public assets in `public/` directory.
