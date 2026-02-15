### 2. Tenant Isolation (Mandatory)
All models dealing with Tenant Data **MUST** use the `App\Traits\BelongsToTenant` trait.
- prevents accidental data leaks at the application layer.
- **Compliance Link**: See `standards/global/compliance.md`.

```php
use App\Traits\BelongsToTenant;

class Product extends Model
{
    use BelongsToTenant;
}
```

### 3. Base Model best practices

- **Clear Naming**: Use singular names for models and plural for tables following your framework's conventions
- **Timestamps**: Include created and updated timestamps on all tables for auditing and debugging
- **Data Integrity**: Use database constraints (NOT NULL, UNIQUE, foreign keys) to enforce data rules at the database level
- **Appropriate Data Types**: Choose data types that match the data's purpose and size requirements
- **Indexes on Foreign Keys**: Index foreign key columns and other frequently queried fields for performance
- **Validation at Multiple Layers**: Implement validation at both model and database levels for defense in depth
- **Relationship Clarity**: Define relationships clearly with appropriate cascade behaviors and naming conventions
- **Avoid Over-Normalization**: Balance normalization with practical query performance needs
