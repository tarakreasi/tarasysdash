# Inertia.js Standards

## Architecture
- **Adapter**: `@inertiajs/vue3`.
- **Backend Adapter**: `inertiajs/inertia-laravel`.

## Pages
- Directory: `resources/js/Pages/`.
- Convention: PascalCase (e.g., `Login.vue`, `Dashboard/Index.vue`).
- Route Mapping: `Route::get(...)` -> `inertia('PageName')`.

## Shared Data
- **Middleware**: `HandleInertiaRequests.php`.
- **Usage**: Use `share()` to pass global data (User, flash messages) to all views.
- **Frontend Access**: Use `usePage().props` to access shared data.
