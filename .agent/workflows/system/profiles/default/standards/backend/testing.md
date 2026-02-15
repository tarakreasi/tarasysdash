# Backend Testing Standards

## Framework
- **Tools**: PHPUnit (default) or Pest.
- **Trait**: `RefreshDatabase` must be used for DB tests.

## Test Suites
1.  **Feature Tests** (`tests/Feature/`):
    - Focus on End-to-End flows (HTTP Request -> Controller -> DB -> Response).
    - **Tenant Tests**: Must verify behavior *with* and *without* tenant context.
    - Example: `TenantTest.php` checks creation and persistence.

2.  **Unit Tests** (`tests/Unit/`):
    - Focus on isolated logic (Service classes, Helpers).

## Definition of Done
- A feature is not done until it has a passing Feature Test.
- `php artisan test` must return GREEN.
