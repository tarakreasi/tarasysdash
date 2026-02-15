# Automation DNA: Coding Standards (Jan 2026 Edition)

## 📅 Context & Versions
**Current Date**: January 17, 2026
**Current Stack**: Laravel 12.x + Vue 3.5+
- **PHP**: 8.4+ (Standard for 2026)
- **Laravel**: 12.x (Use simplified directory structure, no Kernel.php)
- **Node.js**: 22.x (LTS)
- **Vue**: 3.5+ (Standard reactivity)
- **Vite**: 6.x
- **Tailwind**: 4.x (Standard in late 2025/2026)

---

## 🎯 Core Philosophy
This file governs how the AI Executor generates code.
**Stack**: Laravel 10 (PHP) + Vue 3 (JS)

---

## 🐘 Backend Guidelines (Laravel/PHP)

### 1. File Structure
- **Controllers**: `app/Http/Controllers/Api/V1/*Controller.php`
- **Models**: `app/Models/*`
- **Requests**: `app/Http/Requests/*` (Always use FormRequests for validation)
- **Resources**: `app/Http/Resources/*` (Always use API Resources for JSON response)

### 2. Syntax Rules
- **Strict Types**: Always start file with `declare(strict_types=1);`
- **Return Types**: All methods must declare return types.
  ```php
  public function index(): AnonymousResourceCollection
  ```
- **Code Style**: PSR-12.

### 3. API Response Pattern
Return content using Resources, never raw arrays.
```php
return TransactionResource::collection($transactions);
```

### 4. Error Handling
- Use `try-catch` in Services, but let global Handler catch Controller exceptions.
- Return standard JSON error: `{"message": "Error", "errors": [...]}`.

---

### Anti-Hallucination & Tech Stack Guardrails (CRITICAL)

#### Laravel Backend
1. **Field Naming**: DO NOT assume standard field names (like `description`). ALWAYS check the `DOMAIN_CONTRACT.md`. For this project, the primary text field is `title`.
2. **Factories**: Do not use `factory()` in tests unless a factory file has been explicitly created in the current or previous sprints. Use manual `Model::create()` if no factory exists.
3. **Response Wrappers**: Always wrap JSON responses in a `['data' => ...]` envelope.

#### Vue 3 Frontend
1. **Reactivity**: Never format static values in `script setup` directly. Use `computed()` for currency formatting or any data-derived strings to ensure reactivity.
2. **API Interaction**: Use the standard `fetch` API relative to root `/api/v1/`.
3. **Composition API**: Use `<script setup>` and `ref/reactive` exclusively. No Options API.

---

## 🖼️ Frontend Guidelines (Vue 3)

### 1. Component Style
- **Script Setup**: MUST use `<script setup>`.
- **Composition API**: No Options API allowed.
- **Naming**: PascalCase for files (`TransactionList.vue`).

### 2. State Management (Pinia)
- Use "Setup Stores" pattern (function returning object), not Option Stores.
  ```js
  export const useTransactionStore = defineStore('transaction', () => { ... })
  ```

### 3. Tailwind Usage
- No raw CSS in `<style>`. Use utility classes.
- Use configured theme colors: `bg-primary`, `text-accent`.

### 4. API Consumption
- Use a central `http.js` wrapper around Axios (configured with baseURL).
- Async/Await pattern for all fetches.

---

## 🤖 General Rules for Executor
1. **No Placeholders**: Never write `// ... rest of code`. Write the FULL function.
2. **Path Accuracy**: Always use relative paths from project root.
3. **Safety**: Do not overwrite `env` or config files unless explicitly instructed.
