# Sprint EXAMPLE: Qwen-Optimized Microsprint

> **⚠️ THIS IS A TEMPLATE/EXAMPLE - Do not execute**
> 
> Use this as reference when creating new micro-sprints.
> Copy and adapt for your actual sprints.

**Parent Sprint**: @[Sprint X.Y: Parent Name](./sprintX_Y_parent.md)
**Objective**: Create a REST API endpoint for user authentication.
**Status**: PLANNING

---

## 📁 FILES (Create/Modify)

| # | Action | Path | Description |
|---|--------|------|-------------|
| 1 | CREATE | `src/api/auth.py` | Authentication endpoint handlers |
| 2 | CREATE | `src/models/user.py` | User model with password hashing |
| 3 | MODIFY | `src/main.py` | Register auth router |
| 4 | CREATE | `tests/test_auth.py` | Unit tests for auth |

---

## 📋 TASKS

### Task 1: Create User Model

**File**: `src/models/user.py`

**Content**:
```python
from dataclasses import dataclass
from hashlib import sha256

@dataclass
class User:
    id: int
    email: str
    password_hash: str
    
    @staticmethod
    def hash_password(password: str) -> str:
        return sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str) -> bool:
        return self.password_hash == self.hash_password(password)
```

**Verify**:
```bash
test -f src/models/user.py && echo "✅ EXISTS" || echo "❌ MISSING"
```

---

### Task 2: Create Auth Endpoint

**File**: `src/api/auth.py`

**Content**:
```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    token: str
    user_id: int

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    # TODO: Implement actual auth logic
    if request.email == "test@example.com" and request.password == "password":
        return LoginResponse(token="dummy_token", user_id=1)
    raise HTTPException(status_code=401, detail="Invalid credentials")
```

**Verify**:
```bash
grep -q "router = APIRouter" src/api/auth.py && echo "✅ ROUTER DEFINED" || echo "❌ MISSING"
```

---

### Task 3: Register Router in Main

**File**: `src/main.py`

**Find**:
```python
app = FastAPI()
```

**Replace With**:
```python
app = FastAPI()

# Import and register auth router
from src.api.auth import router as auth_router
app.include_router(auth_router)
```

**Verify**:
```bash
grep -q "include_router(auth_router)" src/main.py && echo "✅ ROUTER REGISTERED" || echo "❌ NOT FOUND"
```

---

### Task 4: Create Unit Tests

**File**: `tests/test_auth.py`

**Content**:
```python
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_login_success():
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password"
    })
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_failure():
    response = client.post("/auth/login", json={
        "email": "wrong@example.com",
        "password": "wrong"
    })
    assert response.status_code == 401
```

**Verify**:
```bash
test -f tests/test_auth.py && echo "✅ EXISTS" || echo "❌ MISSING"
```

---

### Task 5: Run Tests

**Working Directory**: Project root

**Command**:
```bash
pytest tests/test_auth.py -v
```

**Expected Output** (contains):
```
test_login_success PASSED
test_login_failure PASSED
```

**If Failed**:
```
1. Check: pytest is installed - `pip install pytest`
2. Check: FastAPI testclient - `pip install httpx`
3. Check: Import errors in test file
```

---

## ✅ COMPLETION CRITERIA

All must be TRUE for sprint to be COMPLETED:

- [ ] File `src/models/user.py` exists and contains `class User`
- [ ] File `src/api/auth.py` exists and contains `router = APIRouter`
- [ ] File `src/main.py` contains `include_router(auth_router)`
- [ ] File `tests/test_auth.py` exists
- [ ] Command `pytest tests/test_auth.py` exits with code 0

---

## 🔗 DEPENDENCIES

**Requires Before Start**:
- Sprint X.Y.0 (Project Setup) must be COMPLETED
- File `src/main.py` must exist with FastAPI app
- `pytest` and `fastapi` installed in environment

**Produces For Next Sprint**:
- `/auth/login` endpoint ready for Sprint X.Y.2 (Token Validation)
- `User` model ready for Sprint X.Y.3 (User Registration)

---

## 📝 NOTES FOR AI

**DO**:
- Create files exactly as specified in Content blocks
- Run verification after each task
- Use exact paths (case-sensitive)

**DO NOT**:
- Add extra dependencies not listed
- Modify files outside FILES table
- Skip test task (Task 5)

**ERROR RECOVERY**:
- If `ModuleNotFoundError`: Check if `src/__init__.py` exists
- If `pytest not found`: Run `pip install pytest`
- If test fails: Check endpoint implementation matches test expectations
