# 🎨 `/agent-design` Workflow (Design OS)

Use this workflow to generate **Visual Specifications** and **Frontend Code** before writing the full functional spec. This acts as the "Designer" in the team.

---

## 🎯 Goal
Transform abstract requirements into concrete **UI Designs** and **Component Code**.

## 📋 Manifest
- **Input**: `docs/product/mission.md` (& `ARCHITECTURE.md`)
- **Output**: `product/sections/[feature]/spec.md` & `data.json`
- **Next Step**: `/agent-research` OR `/agent-spec`

## 🛠️ Phases

### 1. Shape (`/shape-section`)
Define the user flow and layout requirements.
- **Input**: Product Mission or Feature Request.
- **Action**: Interactive interview about the UI.
- **Output**: `product/sections/[feature]/spec.md` (Visual Spec).

### 2. Mock (`/sample-data`)
Create realistic data to see how the UI handles content.
- **Action**: Generate JSON data based on the Visual Spec.
- **Output**: `product/sections/[feature]/data.json`.

### 3. Build (`/design-screen`)
Generate the actual React/Vue components.
- **Input**: Visual Spec + Mock Data.
- **Action**: Write code using Tailwind CSS.
- **Output**: `src/sections/[feature]/components/*.tsx`.

---

## 🔄 Integration Rules

### When to run?
**AFTER** `/product-planner` (You know *what* to build).
**BEFORE** `/agent-spec` (You need to know *how* it looks).

### Handoff to Engineer (`/agent-spec`)
When running `/agent-spec`, explicitly reference the Design OS output:

> "Base the functional spec on the UI Design located at `product/sections/[feature]/spec.md` and the data model in `product/sections/[feature]/data.json`."

---

## 📂 Location
The core engine lives in: `.agent/workflows/tools/design-engine/`
Refer to `docs/dev/DesignOS_GUIDE.md` for advanced usage.
