# TDD Microsprint Example: Test File First

> **⚠️ THIS IS A TEMPLATE/EXAMPLE - Do not execute**
> 
> This shows the TDD pattern: Create test FIRST, then implementation.

---

## Example: Authentication Module

### Sprint 5.2.1: Create test_auth.py (TEST FIRST)

**Parent Sprint**: @[Sprint 5.0: Auth System](./sprint5_0_auth.md)
**Objective**: Create comprehensive tests for authentication module
**Status**: PLANNING
**Type**: TEST

---

#### 📁 FILES

| # | Action | Path | Description |
|---|--------|------|-------------|
| 1 | CREATE | `tests/test_auth.py` | Auth unit tests |

---

#### 📋 TASKS

##### Task 1: Create Test File

**File**: `tests/test_auth.py`

**Content**:
```python
import pytest
from src.auth import AuthService, AuthError

class TestAuthService:
    """Test suite for AuthService"""
    
    def test_login_with_valid_credentials(self):
        """User can login with correct email/password"""
        # Arrange
        auth = AuthService()
        
        # Act
        result = auth.login("user@example.com", "correct_password")
        
        # Assert
        assert result["success"] is True
        assert "token" in result
        assert len(result["token"]) > 0
    
    def test_login_with_invalid_password(self):
        """Login fails with wrong password"""
        auth = AuthService()
        
        with pytest.raises(AuthError) as exc_info:
            auth.login("user@example.com", "wrong_password")
        
        assert "Invalid credentials" in str(exc_info.value)
    
    def test_login_with_unknown_user(self):
        """Login fails for non-existent user"""
        auth = AuthService()
        
        with pytest.raises(AuthError) as exc_info:
            auth.login("unknown@example.com", "any_password")
        
        assert "User not found" in str(exc_info.value)
    
    def test_token_expiry(self):
        """Token should have expiry time"""
        auth = AuthService()
        result = auth.login("user@example.com", "correct_password")
        
        assert "expires_at" in result
        assert result["expires_at"] > 0
```

**Verify**:
```bash
test -f tests/test_auth.py && echo "✅ EXISTS" || echo "❌ MISSING"
python -m py_compile tests/test_auth.py && echo "✅ SYNTAX OK" || echo "❌ SYNTAX ERROR"
```

---

#### ✅ COMPLETION CRITERIA

- [ ] File `tests/test_auth.py` exists
- [ ] Contains 4 test cases (login success, wrong password, unknown user, token expiry)
- [ ] Syntax valid: `python -m py_compile tests/test_auth.py` exits 0

---

#### 🔗 DEPENDENCIES

**Requires**: Sprint 5.1 (Setup) completed
**Produces**: Test file for Sprint 5.2.2

---

### Sprint 5.2.2: Create auth.py (IMPLEMENTATION)

**Parent Sprint**: @[Sprint 5.0: Auth System](./sprint5_0_auth.md)
**Objective**: Implement AuthService to pass all tests from Sprint 5.2.1
**Status**: PLANNING
**Type**: IMPLEMENTATION

---

#### 📁 FILES

| # | Action | Path | Description |
|---|--------|------|-------------|
| 1 | CREATE | `src/auth.py` | Auth service implementation |

---

#### 📋 TASKS

##### Task 1: Create Implementation

**File**: `src/auth.py`

**Guardrail**: Do NOT modify `tests/test_auth.py`. Modify implementation to fit tests.

**Content**:
```python
"""
Authentication Service
Implements login functionality with token generation
"""
from datetime import datetime, timedelta
import hashlib
import secrets

class AuthError(Exception):
    """Authentication related errors"""
    pass

class AuthService:
    """Handle user authentication"""
    
    # Mock user database (replace with real DB in production)
    _users = {
        "user@example.com": {
            "password_hash": hashlib.sha256("correct_password".encode()).hexdigest(),
            "user_id": 1
        }
    }
    
    def login(self, email: str, password: str) -> dict:
        """
        Authenticate user and return token
        
        Args:
            email: User email
            password: Plain text password
            
        Returns:
            dict with success, token, user_id, expires_at
            
        Raises:
            AuthError: If authentication fails
        """
        # Check if user exists
        if email not in self._users:
            raise AuthError("User not found")
        
        user = self._users[email]
        
        # Verify password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_hash != user["password_hash"]:
            raise AuthError("Invalid credentials")
        
        # Generate token
        token = secrets.token_urlsafe(32)
        expires_at = int((datetime.now() + timedelta(hours=24)).timestamp())
        
        return {
            "success": True,
            "token": token,
            "user_id": user["user_id"],
            "expires_at": expires_at
        }
```

**Verify**:
```bash
test -f src/auth.py && echo "✅ EXISTS" || echo "❌ MISSING"
```

---

##### Task 2: Run Tests (MUST PASS)

**Command**:
```bash
pytest tests/test_auth.py -v
```

**Expected Output** (contains):
```
test_login_with_valid_credentials PASSED
test_login_with_invalid_password PASSED
test_login_with_unknown_user PASSED
test_token_expiry PASSED
```

**If Failed**:
```
1. Read test file to understand expected behavior
2. Check implementation matches test expectations
3. Fix implementation until all 4 tests pass
```

---

#### ✅ COMPLETION CRITERIA

- [ ] File `src/auth.py` exists
- [ ] Contains `AuthService` class with `login` method
- [ ] Contains `AuthError` exception
- [ ] **All tests pass**: `pytest tests/test_auth.py` returns 4 passed

---

#### 🔗 DEPENDENCIES

**Requires**: Sprint 5.2.1 (test_auth.py) COMPLETED
**Produces**: Working auth module for Sprint 5.3

---

## Summary: TDD Sprint Pair

| Sprint | Type | File | Purpose |
|--------|------|------|---------|
| 5.2.1 | TEST | `tests/test_auth.py` | Define expected behavior |
| 5.2.2 | IMPL | `src/auth.py` | Implement to pass tests |

**Total Lines**: ~80 per sprint (within 120 limit)

---

## Key Patterns Demonstrated

1. **Test First**: 5.2.1 creates tests before 5.2.2 creates implementation
2. **Granular**: Each sprint does one thing (test OR implement)
3. **Explicit Verification**: `pytest` command with expected output
4. **Clear Dependencies**: 5.2.2 requires 5.2.1 to be complete
5. **Error Handling Tested**: Both success and failure cases
