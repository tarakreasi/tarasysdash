---
description: Create single-file atomic sprints derived from DOMAIN_CONTRACT.md
---
# 🧩 `/agent-microsprint` Workflow

Use this workflow to break down a Parent Sprint into **Atomic, Single-File Sprints**.

## 📋 Manifest
- **Input**: Parent Sprint & `DOMAIN_CONTRACT.md`
- **Output**: `sprintX_Y_Z.md` (Draft)
- **Next Step**: `/agent-detail`

---

## 🛑 CORE RULES

1.  **Atomic Integrity**: Each sprint MUST produce **ONLY ONE** logical file (plus its verification script).
    - *OK*: `TransactionController.php`
    - *NOT OK*: `TransactionController.php` + `TransactionRequest.php` + `api.php`
2.  **Contract Binding**: Every sprint MUST include a `CONTRACT & BLUEPRINT` block. 
3.  **Visual Precision** (Frontend): MUST include Tailwind classes definition for every element.
4.  **Interface Clarity** (Typescript/Go): MUST include Interface/Struct definition for dependencies.

---

## 📝 PROCESS

### 1. Read the Contract & Parent Sprint
Analyze the requirements and the Domain Contract.

### 2. Generate Atomic Sprint Files
For each file needed in the Parent Sprint, create a separate `.md` file:
`docs/dev/sprints/sprintX_Y_Z_filename.md`

### 3. Template Structure

**IMPORTANT**: Use the official template from `.agent/templates/microsprint_high_fidelity.md`.

**DO NOT** copy-paste old templates. Always reference the latest version:

```bash
cat .agent/templates/microsprint_high_fidelity.md
```

**Key sections that MUST be included** (from Template V2.1):
- `### 1. Architecture` (Dependencies, Imports, Interfaces)
- `### 2. Schema Reference` (For Backend/DB tasks - field names from DOMAIN_CONTRACT.md)
- `### 3. API Response Format` (For Frontend consuming API - exact JSON structure)
- `### 4. Visual Specification` (For Frontend - Tailwind classes)
- `### 5. Implementation Constraints` (CRITICAL: "SINGLE FILE" rule, NO child components unless explicit)
- `### 6. Logic Requirements` (Business rules)

**Template Location**: `.agent/templates/microsprint_high_fidelity.md`

---

## When to use?
- Whenever you are about to split a feature (e.g., "User Auth") into actionable code.
- Instead of creating one big sprint "Implement Auth", create:
  - Sprint 2.1.1: `User.php` Model
  - Sprint 2.1.2: `AuthController.php`
  - Sprint 2.1.3: `login.vue`
