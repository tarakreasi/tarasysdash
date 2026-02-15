# Laravel Backend Standards

## Core
- **Framework**: Laravel 11.x (or latest stable).
- **PHP Version**: 8.3+ (Strict Types `declare(strict_types=1);` required in new classes).
- **API Structure**:
    - Use Resource Controllers (`php artisan make:controller Api/V1/UserController --api`).
    - Use FormRequests for validation (`php artisan make:request StoreUserRequest`).
    - Return JSON responses via Resources (`php artisan make:resource UserResource`).

## Static Analysis (PHPStan)
- **Level**: 5 (Minimum).
- **Config**: `phpstan.neon` in root.
- **Execution**: `php artisan phpstan:analyse` or `./vendor/bin/phpstan analyse`.
- **CI Gate**: Must pass before merge.

## Directory Structure
- `app/Models`: Eloquent models.
- `app/Http/Controllers/Api/V1`: API Controllers.
- `app/Traits`: Shared logic (e.g., `BelongsToTenant`).
