# Multi-Tenancy Standards

## Architecture
- **Package**: `stancl/tenancy` v3.x.
- **Strategy**: Single Database with `tenant_id` column (Row-Level Isolation).
    - **Pros**: Cost-effective, easier migration management for MVP.
    - **Cons**: Requires strict global scope application.

## Models
1.  **Tenant Model**:
    - Class: `App\Models\Tenant`
    - Extends: `Stancl\Tenancy\Database\Models\Tenant`
    - Table: `tenants` (Central DB)

2.  **Tenant-Aware Models**:
    - Must use `App\Traits\BelongsToTenant`.
    - Must have `tenant_id` column (foreign key to `tenants.id`).

## Isolation Rules
- **Global Scope**: The `BelongsToTenant` trait automatically applies `where('tenant_id', $currentTenant->id)`.
- **Bypass**: Use `withoutGlobalScope(TenantScope::class)` ONLY for Admin/Superuser actions.
- **Middleware**: Routes requiring isolation must utilize tenancy middleware detection.
