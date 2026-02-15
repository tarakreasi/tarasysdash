# Sprint 0.0: Frontend Recovery (Parent)

**Spec**: `docs/planning/RECOVERY_PLAN.md` & `docs/specs/DOMAIN_CONTRACT.md`
**Objective**: Stabilize the frontend architecture, refactor the "God Component", and enforce coding standards.
**Status**: PLANNING

---

## 📊 Sprint Overview

| Metric | Target |
|--------|--------|
| Micro-Sprints | 4 |
| Files to Create | ~8 |
| Test Coverage | N/A (Frontend Focus - Linting/Types) |

---

## 🧪 Test Strategy

**Approach**:
1.  **Static Analysis**: Enforce strict ESLint + Prettier rules.
2.  **Type Safety**: Ensure zero `any` usage in new `services/`.
3.  **Manual Verification**: Verify Dashboard still loads and displays data after refactoring.

---

## 📋 Micro-Sprint Breakdown

### Phase 1: Foundation & DNA
| Sprint | Description | Files | Type |
|--------|-------------|-------|------|
| 0.1 | **Standards & Config**<br>- Configure ESLint/Prettier<br>- Extract `API_BASE` to `.env` | `.eslintrc`, `.env` | Setup |

### Phase 2: Architecture Refactor
| Sprint | Description | Files | Type |
|--------|-------------|-------|------|
| 0.2 | **API Layer Extraction**<br>- Create `src/services/api.ts`<br>- Define TypeScript Interfaces from Domain Contract | `services/api.ts`, `types/index.ts` | Refactor |
| 0.3 | **Component Deconstruction**<br>- Extract Charts from `DashboardView.vue`<br>- Create `components/charts/*.vue` | `DashboardView.vue`, `components/charts/` | Refactor |

### Phase 3: State & Logic
| Sprint | Description | Files | Type |
|--------|-------------|-------|------|
| 0.4 | **Logic Composition**<br>- Extract fetching logic to `composables/useServerMetrics.ts` | `composables/useServerMetrics.ts` | Refactor |

---

## ✅ Parent Completion Criteria

- [x] `API_BASE` is configurable via `.env`.
- [x] `DashboardView.vue` is < 400 lines (currently > 1000).
- [x] No raw Axios calls in components.
- [x] `npm run build` passes with no type errors.

---

## 🔗 Dependencies

**Requires**:
- Valid `RECOVERY_PLAN.md`

**Produces**:
- A clean, architectural base for future features.
